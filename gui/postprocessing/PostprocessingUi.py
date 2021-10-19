

"""
Results
---------

This module implements the *Results* tab the *AsterStudy* application.
See `Results` class for more details.

"""
import os
from PyQt5 import Qt as Q

from ...common import (wait_cursor, CFG, translate,connect)

from ..post.navigator import OverlayBar

from ..post import (ResultFile, PlotWindow,
                    ColorRep, WarpRep, ModesRep, BaseRep,
                    pvcontrol, show_min_max, selection_probe, selection_plot,
                    get_active_selection, get_pv_mem_use, dbg_print,
                    RESULTS_PV_LAYOUT_NAME, RESULTS_PV_VIEW_NAME)

# from . import get_icon
import pvsimple as pvs
from ..post.pvsidebar import SideBar

__all__ = ["Results"]

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions

# pragma pylint: disable=too-many-instance-attributes


class Results(Q.QWidget):
    """Class that controls the behavior of the Results tab of the
     *AsterStudy* application.
    利用Paraview实现后处理标签页    
    daizijian 2020/3/10
    """

    # GUI related objects
    # ===================
    # >> pv_view: salome (view) of type ParaView (initializes paraview)
    # >> res_splitter: results tab main widget, based on a vertical splitter
    # >> pv_widget : the paraview widget

    # Paraview internals
    # ==================
    # >> pv_layout: paraview layout, specific for asterstudy
    # >> ren_view: paraview RenderView added inside pv_layout

    # Paraview key pipeline objects
    # =============================
    # >> current: currently active paraview reader source
    # >> previous: a dictionnary of all reader sources (for optimized access)
    # >> min_max_src: sources for displaying minimum and maximum values

    # Representation objects
    # ======================
    # >> shown: representation currently (related to source "current") at display

    _loader = res_splitter = pv_widget = pv_view = pv_layout = None
    ren_view = pv_overlay = toolbuttons = current = previous = None
    pv_widget_children = play_btn = pause_btn = outline_btn = None
    minmax_btn = infobar_label = shown = filename_label = None

    min_max_src = []
    probing = True

    def __init__(self, astergui, parent=None):
        """
        Create/intialize the results tab.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        Q.QWidget.__init__(self, parent)

        # 后处理所需的视窗数目
        self.windows = 1

        self.setSizePolicy(Q.QSizePolicy.Expanding,
                           Q.QSizePolicy.Expanding)

        self.astergui = astergui
        self.previous = {}

        # font = Q.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(10)
        # self.setFont(font)

        # Set up the main GUI layout that expands over the whole view
        hlayout = Q.QHBoxLayout(self)
        self.res_splitter = Q.QSplitter(Q.Qt.Horizontal, self)
        self.res_splitter.setSizePolicy(Q.QSizePolicy.Expanding,
                                        Q.QSizePolicy.Expanding)
        hlayout.addWidget(self.res_splitter)

        #创建左侧边栏
        left_container = Q.QWidget(self)
        self.sidebar = SideBar()
        self.sidebar.setupUi(left_container)
        self.sidebar.pushButton_3.clicked.connect(self.load_ofccx_result_call)
        # self.sidebar.tabWidget.currentChanged['int'].connect(self.changeview)

        self.filename_label = Q.QLabel()
        self.filename_label.hide()

        self.loadbutton = Q.QPushButton('载入后处理结果')
        # fname = '/home/export/online1/systest/swrh/dzj/test666/para-case/Solid/tank.pvd'
        # self.loadbutton.clicked.connect(self.load_ofccx_result_call)
        self.loadbutton.hide()

        # Add the 4 widgets to the sidebar
        # 在左边的res_splitter加入内容
        self.res_splitter.addWidget(left_container)
        # self.res_splitter.addWidget(self.loadbutton)
        # self.res_splitter.addWidget(self.filename_label)
        self.res_splitter.setMinimumWidth(1500)
        self.threshold1 = None
        self.colorobject = {}
        self.clip1 = None
        self.clip2 = None
        self.currentdisplay = None
        self.currentdisplay1 = None
        self.solidpvd = None
        self.fluidfoam = None

    def changeview(self,i):
        if i == 0:
            pvs.SetActiveView(self.ren_view)
        elif i == 1:
            pvs.SetActiveView(self.ren_view1)

    # def set_as_working_tab(self):
    #     """
    #     Shows the results tab in the astergui workspace
    #     """
    #     from . import WorkingMode
    #     self.astergui.workSpace().main.setTabEnabled(WorkingMode.ResultsMode, True)
    #     self.astergui.workSpace().setWorkingMode(WorkingMode.ResultsMode)

    def detach(self, keep_pipeline=True):
        """
        Function called upon deactivating asterstudy, allows to properly
        remove all layouts and view from the ParaView View (salome View)
        """
        from .salomegui import get_salome_pyqt
        import pvsimple as pvs

        # Clears the PV widget and removes the event filter (right click
        # behavior) from all of its children.
        if self.pv_widget:
            for child in self.pv_widget_children:
                if child:
                    try:
                        child.removeEventFilter(self)
                    except BaseException: # pragma pylint: disable=broad-except
                        pass
            self.pv_widget_children = []
            self.pv_widget = None

        # This forces the creation of new overlay buttons upon restarting
        # the AsterStudy results tab
        self.pv_overlay = None
        self.toolbuttons = None

        # Deletes the active view and layout from paraview
        # Close the (salome) view corresponding to 'ParaView'
        get_salome_pyqt().closeView(self.pv_view)
        # get_salome_pyqt().closeView(self.ren_view)
        # get_salome_pyqt().closeView(self.ren_view1)
        
        self.ren_view = None
        self.ren_view1 = None
        pvs.RemoveLayout(self.pv_layout)
        self.pv_layout = None
        self.pv_view = None

        # Optional: clear all sources and proxies, leaving no trace!
        if not keep_pipeline:
            self.previous = {}
            self.current = None
            self.shown = None
            pxm = pvs.servermanager.ProxyManager()
            pxm.UnRegisterProxies()
            del pxm
            pvs.Disconnect()
            pvs.Connect()

    def init_paraview(self, full_load_pv=True):
        """
        Initializes, if necessary, paraview and creates a dedicated pvsimple
        view in the results tab.
        """
        from ..salomegui import (get_salome_pyqt, get_salome_gui)

        if not self.pv_view:
            import time
            dbg_print(">> Initializing PV view for the results tab...")
            start = time.time()

            # A Paraview (view) already exists ?
            views = get_salome_pyqt().findViews('ParaView')
            if not views:
                get_salome_pyqt().createView('ParaView', True, 0, 0, True)
                views = get_salome_pyqt().findViews('ParaView')

            self.pv_view = views[-1]
            get_salome_pyqt().activateViewManagerAndView(self.pv_view)
            self.update_pv_layout_view()
            end = time.time()
            dbg_print("  Finished in %d seconds..." % int(end - start))

            self._finalize_pv_widget()
        else:
            self.update_pv_layout_view()
            self._finalize_pv_widget()

        if self.current:
            self.redraw()

    def _finalize_pv_widget(self):
        """
        References toolbuttons (for interactive selection) and updates the
        overlay widget if needed
        """
        if self.pv_widget:
            if not self.toolbuttons:
                self._add_toolbuttons()
            if not self.pv_overlay:
                self._add_overlay()

    def _add_toolbuttons(self):
        """
        Shortcut for referencing the toolbuttons that may need to be
        automatically activated for point and cell selections

        requires : self.pv_widget
        """
        self.toolbuttons = {'Interactive Select Cells On': None,
                            'Interactive Select Points On': None,
                            'Select Points On (d)': None,
                            'Select Cells On (s)': None,
                            }
        to_find = list(self.toolbuttons.keys())
        # Backward search since AsterStudy PV Layout is added after
        # the default one! ==>                              [::-1]
        for tbutt in self.pv_widget.findChildren(Q.QToolButton)[::-1]:
            if not to_find:
                break
            for tooltip in to_find:
                if tooltip in tbutt.toolTip():
                    self.toolbuttons[tooltip] = tbutt
                    to_find.remove(tooltip)
                    break

    def _add_overlay(self):
        """
        Add an overlay widget to the main pv_widget with a few buttons
        to control the view, save screenshots, etc.

        requires : self.pv_widget
        """

        # START
        # ol_height = 56 # Overlay height in pixels
        ol_height = 50  # Overlay height in pixels
        self.pv_overlay = OverlayBar(self.pv_widget, height=ol_height,
                                     botline=(0, 0, 255, 2)
                                     )

        # >> Buttons toolbar items
        #    Start with an empty shell widget, used for parenting toolbar buttons
        #    and enforcing a simple horizontal layout with a right spacer
        hlayo = Q.QHBoxLayout()
        hlayo.setContentsMargins(5, 5, 5, 5)
        hlayo.setSpacing(5)
        # add_button(hlayo, tooltip='Refresh view',
        #            icon='PVC Refresh',
        #            callback=self.redraw)
        # add_separator(hlayo)

        # Camera controls
        add_button(hlayo, tooltip='Project view to X (YZ-plane)',
                   icon='PVC XProj',
                   callback=lambda: pvcontrol(self, 'xproj'))
        add_button(hlayo, tooltip='Project view to Y (XZ-plane)',
                   icon='PVC YProj',
                   callback=lambda: pvcontrol(self, 'yproj'))
        add_button(hlayo, tooltip='Project view to Z (XY-plane)',
                   icon='PVC ZProj',
                   callback=lambda: pvcontrol(self, 'zproj'))
        # add_separator(hlayo)

        # Time and animation controls
        add_button(hlayo, tooltip='First time step',
                   icon='PVC TFirst',
                   callback=lambda: pvcontrol(self, 'first'))
        add_button(hlayo, tooltip='Previous time step',
                   icon='PVC TPrev',
                   callback=lambda: pvcontrol(self, 'tprev'))
        self.play_btn = add_button(hlayo, tooltip='Play',
                                   icon='PVC Play',
                                   callback=lambda: pvcontrol(self, 'play'))
        self.pause_btn = add_button(hlayo, tooltip='Pause',
                                    icon='PVC Pause',
                                    callback=lambda: pvcontrol(self, 'pause'))
        self.pause_btn.setVisible(False)
        self.play_btn.hide()
        self.pause_btn.hide()
        add_button(hlayo, tooltip='Next time step',
                   icon='PVC TNext',
                   callback=lambda: pvcontrol(self, 'tnext'))
        add_button(hlayo, tooltip='Last time step',
                   icon='PVC TLast',
                   callback=lambda: pvcontrol(self, 'last'))
        # add_separator(hlayo)

        # Display controls
        self.outline_btn = add_button(hlayo, tooltip='Toggle bounding box',
                                      icon='PVC Outline',
                                      callback=lambda: pvcontrol(
                                          self, 'outline'),)
                                    #   checkable=True)

        # add_button(hlayo, tooltip='Toggle reference position',
        #            icon='PVC Reference',
        #            callback=lambda: pvcontrol(self, 'reference'),
        #            checkable=False)
        # self.minmax_btn = add_button(hlayo, tooltip='Toggle min/max',
        #                              icon='PVC MinMax',
        #                              callback=lambda: pvcontrol(
        #                                  self, 'min_max'),
        #                              checkable=True)
        # add_button(hlayo, tooltip='Rescale colorbar to current step range',
        #            icon='PVC Rescale',
        #            callback=lambda: pvcontrol(self, 'rescale_colorbar'),
        #            checkable=False)

        # # TODO ADD THE PROBE CONTROL HERE
        # # add_separator(hlayo)
        # add_button(hlayo, tooltip='Probe values on one or more points or cells',
        #            icon='PVC Probe',
        #            callback=lambda: pvcontrol(self, 'probe'))
        # add_button(hlayo, tooltip='Plot data over time for a single point or cell',
        #            icon='PVC Plot',
        #            callback=lambda: pvcontrol(self, 'plot_over_time'))
        # add_separator(hlayo)

        # Export view & animation
        add_button(hlayo, tooltip='Save a screenshot of the current representation',
                   icon='PVC Screenshot',
                   callback=lambda: pvcontrol(self, 'screenshot'))
        add_button(hlayo, tooltip='Save a movie of the current animation',
                   icon='PVC Movie',
                   callback=lambda: pvcontrol(self, 'movie'))
        spacer = Q.QSpacerItem(25, 25, hPolicy=Q.QSizePolicy.Expanding)
        hlayo.addItem(spacer)

        # >> Information labels bar
        self.infobar_label = Q.QLabel(self.pv_overlay)
        hlayo.addWidget(self.infobar_label)
        self.update_infobar()

        self.pv_overlay.setLayout(hlayo)

    def update_pv_layout_view(self, full_update=True):
        """
        Updates or creates a new PV layout and view for AsterStudy
        post processing in the Results tab
        """
        import pvsimple as pvs
        from ..salomegui import get_salome_pyqt
        # pvs.Delete(renderView1)
        # del renderView1
        pv_layout = pvs.GetLayoutByName(RESULTS_PV_LAYOUT_NAME)
        if not pv_layout:
            pv_layout = pvs.CreateLayout(name=RESULTS_PV_LAYOUT_NAME)
            
            # if self.windows==1:
            #     pv_layout.SplitHorizontal(1, 0)
            
        self.views = pvs.GetViewsInLayout(pv_layout)
        if not self.views:
            # self.views = []
            # for i in range(self.windows):
            #     pvs.SetActiveView(None)
            #     # newview = pvs.CreateRenderView(guiName=RESULTS_PV_VIEW_NAME) 
            #     self.views += pvs.CreateRenderView(guiName=RESULTS_PV_VIEW_NAME)
            #     # Some basic customizations
            #     logo = pvs.servermanager.rendering.ImageTexture()
            #     logo.FileName = CFG.rcfile('results-pv-bg.png')

            #     self.views[-1].BackgroundTexture = logo
            #     self.views[-1].UseTexturedBackground = 1

            #     self.views[-1].OrientationAxesLabelColor = [0.1, 0.1, 0.1]
            #     self.views[-1].OrientationAxesOutlineColor = [0.0, 0.0, 0.0]
            pvs.SetActiveView(None)
            self.ren_view = pvs.CreateRenderView(guiName=RESULTS_PV_VIEW_NAME)
            self.ren_view.UseGradientBackground = 1
            pv_layout.AssignView(0, self.ren_view)

        self.pv_layout = pvs.GetLayoutByName("Layout #1")
        # Reinforce event filter installation for capturing mouse
        # and keyboard events on the imported paraview view
        pvs.RenameLayout('Results', layout1)
        self.pv_widget = get_salome_pyqt().getViewWidget(self.pv_view)
        print(self.pv_widget)

        self.pv_widget.setSizePolicy(Q.QSizePolicy.Expanding,
                                    Q.QSizePolicy.Expanding)
        # self.QDialog = Q.QDialog()
        # self.verticalLayout_2 = Q.QVBoxLayout(self.QDialog)
        # self.verticalLayout_2.addWidget(self.pv_widget)
        # self.QDialog.show()

        # self.widget111 = Q.QWidget(self)
        # self.pv_widget.setCentralWidget(self.widget111)
        self.res_splitter.addWidget(self.pv_widget)
        # self.widget111 = Q.QWidget(self)
        # self.verticalLayout_2 = Q.QVBoxLayout(self.widget111)
        # self.verticalLayout_2.addWidget(self.pv_widget)
        # self.test666 = Q.QLabel('111111111')

        # self.verticalLayout_2.addWidget(self.test666)
        # self.res_splitter.addWidget(self.widget111)
        # self.test666 = Q.QLabel('111111111')

        # self.res_splitter.addWidget(self.test666)


        # The following insures that the view is refreshed
        # self.res_splitter.widget(1).setVisible(True)
        self.res_splitter.setVisible(False)
        self.res_splitter.setVisible(True)

        pvs.Render()
        ################################################################
        # COMMENTED : RETRIEVE THE 3D PV FRAME
        # frames = self.pv_widget.findChildren(Q.QFrame)
        # for frame in frames[::-1]:
        #     if type(frame) == Q.QFrame:
        #         break
        # self.pv_frame = frame
        # self.pv_frame.setContextMenuPolicy(Q.Qt.CustomContextMenu)
        # self.pv_frame.customContextMenuRequested.connect(
        #    lambda: results.navtree.contextMenuEvent('Representation'))
        ################################################################
        # To create the context menu;
        # context = Q.QContextMenuEvent(Q.QContextMenuEvent.Mouse,
        #                               self.cursor().pos())
        # Q.QCoreApplication.postEvent(self.pv_frame, context)
        ################################################################

        self.pv_widget_children = [self.pv_widget]
        self.pv_widget_children += self.pv_widget.findChildren(Q.QWidget)

        to_ignore = []
        if self.pv_overlay:
            to_ignore = [self.pv_overlay] + \
                self.pv_overlay.findChildren(Q.QWidget)

        for child in self.pv_widget_children:
            if not child in to_ignore:
                child.installEventFilter(self)

        # Account for the possibility that some readers are deleted by the user
        # in the paravis module, keep only the available readers
        proxy_man = pvs.servermanager.ProxyManager()
        available_sources = list(
            proxy_man.GetProxiesInGroup('sources').values())
        unavailable = []
        for path in self.previous:
            prev, _ = self.previous[path]
            if not prev.full_source in available_sources:
                unavailable.append(path)
                continue

            for source in ['filter_source', 'extract_source', 'source',
                           'mode_source', 'dup_source']:
                src = getattr(self.current, source)
                if src and not src in available_sources:
                    setattr(self.current, source, None)

        for path in unavailable:
            self.previous[path][0].full_source = None
            self.previous.pop(path, None)

        if self.current:
            do_delete = False
            for source in ['filter_source', 'extract_source', 'source',
                           'full_source', 'mode_source', 'dup_source']:
                src = getattr(self.current, source)
                if src and not src in available_sources:
                    setattr(self.current, source, None)
                    do_delete = True
            if do_delete:
                self.current = None

        BaseRep.refresh_available_sources()

    def refresh(self):
        pvs.ReloadFiles(self.solidpvd)
        pvs.ReloadFiles(self.fluidfoam)

    def clear_paraview_pipeline(self):
        """
        Clears up intermediate paraview pipeline sources and
        refreshes the current representation
        """
        wait_cursor(True)
        self.shown.clear_sources()
        self.clear_readers()
        self.redraw()
        wait_cursor(False)

    def clear_readers(self):
        """
        Clears readers from the paraview pipeline not relevant
        to the current representation
        """
        import pvsimple as pvs

        to_remove = []
        for path in self.previous:
            if path == self.current.path:
                continue
            prev, _ = self.previous[path]

            for source in ['filter_source', 'extract_source', 'source',
                           'full_source', 'mode_source', 'dup_source']:
                if hasattr(prev, source):
                    src = getattr(prev, source)
                    setattr(prev, source, None)
                    if not src:
                        continue
                    try:
                        pvs.Delete(src)
                    except RuntimeError:
                        pass

            to_remove.append(path)

        for path in to_remove:
            self.previous.pop(path, None)

        for source in ['mode_source', 'dup_source']:
            if hasattr(self.current, source):
                src = getattr(self.current, source)
                setattr(self.current, source, None)
                if not src:
                    continue
                try:
                    pvs.Delete(src)
                except RuntimeError:
                    pass

    def minmax_shown(self):
        """Returns whether the minmax button is checked"""
        return self.minmax_btn.isChecked()

    def set_minmax_shown(self):
        """Checks the minmax button"""
        self.minmax_btn.setChecked(True)

    def outline_shown(self):
        """Returns whether the outline button is checked"""
        return self.outline_btn.isChecked()

    def set_outline_shown(self):
        """Checks the outline button"""
        self.outline_btn.setChecked(True)

    def load_med_result(self, med_fn, loader):
        """
        Load a results file in MED format

        Arguments:
            med_fn (string): full path to the MED filename to be loaded
            loader
        """
        if not med_fn:
            dbg_print("Invalid med file")
            return

        self._loader = loader
        self._loader.start()
        Q.QTimer.singleShot(50, lambda: self.load_med_result_call(med_fn))

    def load_med_result_call(self, med_fn, full_load_pv=True):
        """
        Load a results file in MED format

        Arguments:
            med_fn (string): full path to the MED filename to be loaded
        """
        # Initialize paraview widget in asterstudy gui
        # (this can take a few seconds on first load)
        new_load = True

        self.init_paraview(full_load_pv=full_load_pv)
        self.shown = None

        modif_time = os.path.getmtime(med_fn)
        if med_fn in self.previous:
            # This file has already been read, check if the modification date
            # is identifical to the previous load, if so then just set it as current
            new_load = (modif_time != self.previous[med_fn][1])

        if new_load:
            if not self._loader:
                from . salomegui import LoadingMessage
                self._loader = LoadingMessage(self, 'Please wait...', True)
                self._loader.start()

            res = ResultFile(med_fn)

            # Check if there are indeed fields that can be represented
            if res.is_empty():
                if self._loader:
                    self._loader.terminate()
                wait_cursor(False)

                if self.astergui:
                    msg = translate("AsterStudy",
                                    "The provided MED file contains no "
                                    "result concepts or fields.\n")
                    buttons = Q.QMessageBox.Ok
                    Q.QMessageBox.warning(self.astergui.mainWindow(), "AsterStudy",
                                          msg, buttons, Q.QMessageBox.Ok)

                return

            self.current = res
            self.previous.update({self.current.path: (self.current, modif_time)})
        else:
            self.current = self.previous[med_fn][0]

        self.ren_view.ResetCamera()

        # self.refresh_navigator()
        pvcontrol(self, 'first')

        # Show displacement field preferentially by default
        for concept in self.current.concepts:
            for field in concept.fields:
                if 'DEPL' in field.name:
                    self.represent(field, WarpRep)
                    pvcontrol(self, 'resetview')
                    return

        # If not found, show the first field that is found
        for concept in self.current.concepts:
            for field in concept.fields:
                self.represent(field)
                pvcontrol(self, 'resetview')
                return

    def autoscreenshots(self,path):
        from xml.etree import ElementTree
        parser = ElementTree.parse(path+"/Solid/tanksim.pvd")
        root=parser.getroot()

        if len(root[0])<4:
            screenshotindex = [-1]
        #timeseries=[root[0][-1].attrib['timestep']]
        elif len(root[0])<14:
            screenshotindex = [2,-2]
        #timeseries=[root[0][2].attrib['timestep'],root[0][-2].attrib['timestep']]
        else:
            screenshotindex = [2,len(root[0])//2,-2]
        #timeseries=[root[0][2].attrib['timestep'],root[0][len(root[0])//2].attrib['timestep'],root[0][-2].attrib['timestep']]

        timeseries=[]
        for i in range(len(root[0])):
            timeseries.append(root[0][i].attrib['timestep'])

        # 所有时间步的列表(float)
        times = self.solidpvd.TimestepValues

        for n in screenshotindex:
            # reader = pvs.GetActiveSource()
            # times = reader.TimestepValues
            # print('times=',times)
            self.ren_view.ViewTime = times[n]
            pvs.Render()

            # self.ren_view.CameraPosition = [0.0, 0.0, 1.0]
            # self.ren_view.ResetCamera()
            self.projection(self.ren_view,'z')
            pvs.SaveScreenshot(path+'/maxvonmisesZ+'+timeseries[n]+'s.png', self.ren_view)
            self.ren_view.CameraPosition = [0.0, 0.0, 1.0]
            self.ren_view.ResetCamera()
            pvs.SaveScreenshot(path+'/maxvonmisesZ-'+timeseries[n]+'s.png', self.ren_view)

            # self.ren_view.CameraPosition = [1.0, 0.0, 0.0]
            # self.ren_view.ResetCamera()
            self.projection(self.ren_view,'x')
            pvs.SaveScreenshot(path+'/maxvonmisesX+'+timeseries[n]+'s.png', self.ren_view)
            self.ren_view.CameraPosition = [-1.0, 0.0, 0.0]
            self.ren_view.ResetCamera()
            pvs.SaveScreenshot(path+'/maxvonmisesX-'+timeseries[n]+'s.png', self.ren_view)
            
            # self.ren_view.CameraPosition = [0.0, 1.0, 0.0]
            # self.ren_view.ResetCamera()
            self.projection(self.ren_view,'y')
            pvs.SaveScreenshot(path+'/maxvonmisesY+'+timeseries[n]+'s.png', self.ren_view)
            self.ren_view.CameraPosition = [0.0, -1.0, 0.0]
            self.ren_view.ResetCamera()
            pvs.SaveScreenshot(path+'/maxvonmisesY-'+timeseries[n]+'s.png', self.ren_view)
                

        for n in screenshotindex:
            # reader = pvs.GetActiveSource()
            # times = reader.TimestepValues
            # print('times=',times)
            self.ren_view1.ViewTime = times[n]
            pvs.Render()

            # self.ren_view1.CameraPosition = [0.0, 0.0, 1.0]
            # self.ren_view1.ResetCamera()
            self.projection(self.ren_view1,'z')
            pvs.SaveScreenshot(path+'/alphawaterZ+'+timeseries[n]+'s.png', self.ren_view1)
            
            self.ren_view1.CameraPosition = [0.0, 0.0, 1.0]    
            self.ren_view1.ResetCamera()                      
            pvs.SaveScreenshot(path+'/alphawaterZ-'+timeseries[n]+'s.png', self.ren_view1)                                                        

            
            # self.ren_view1.CameraPosition = [1.0, 0.0, 0.0]
            # self.ren_view1.ResetCamera()
            self.projection(self.ren_view1,'x')
            pvs.SaveScreenshot(path+'/alphawaterX+'+timeseries[n]+'s.png', self.ren_view1)
            
            self.ren_view1.CameraPosition = [-1.0, 0.0, 0.0]
            self.ren_view1.ResetCamera()
            pvs.SaveScreenshot(path+'/alphawaterX-'+timeseries[n]+'s.png', self.ren_view1)
            
            # self.ren_view1.CameraPosition = [0.0, 1.0, 0.0]
            # self.ren_view1.ResetCamera()
            self.projection(self.ren_view1,'y')
            pvs.SaveScreenshot(path+'/alphawaterY+'+timeseries[n]+'s.png', self.ren_view1)
            
            self.ren_view1.CameraPosition = [0.0, -1.0, 0.0]
            self.ren_view1.ResetCamera()
            pvs.SaveScreenshot(path+'/alphawaterY-'+timeseries[n]+'s.png', self.ren_view1)

    def projection(self,ren_view,request):
        if request == 'x':
            refpos = [-1e5, 0., 0.]\
                if ren_view.CameraPosition[0] > 0\
                else [1e5, 0., 0.]
            ren_view.CameraPosition = refpos
            ren_view.CameraFocalPoint = [0.0, 0.0, 0.0]
            ren_view.CameraViewUp = [0.0, 0.0, 1.0]
            ren_view.ResetCamera()
        elif request == 'y':
            refpos = [0., -1e5, 0.] if ren_view.CameraPosition[1] > 0 else [0., 1e5, 0.]
            ren_view.CameraPosition = refpos
            ren_view.CameraFocalPoint = [0.0, 0.0, 0.0]
            ren_view.CameraViewUp = [0.0, 0.0, 1.0]
            ren_view.ResetCamera()
        elif request == 'z':
            refpos = [0., 0., 1e5] if ren_view.CameraPosition[2] < 0 \
                else [0., 0., -1e5]
            ren_view.CameraPosition = refpos
            ren_view.CameraFocalPoint = [0.0, 0.0, 0.0]
            ren_view.CameraViewUp = [0.0, 1.0, 0.0]
            ren_view.ResetCamera()        

    def load_ofccx_result_call(self,path=None):
        """
        仿照load_med_result_call所写的载入openfoam和calculix流固耦合结果函数
        daizijian 2020/3/22

        Arguments:
            of_fn (string): full path to the openfoam .foam filename to be loaded
            ccx_fn (string): full path to the calculix .frd filename to be loaded
        """
        # Initialize paraview widget in asterstudy gui
        # (this can take a few seconds on first load)

        full_load_pv=True
        # self.init_paraview(full_load_pv=full_load_pv)
        self.shown = None

        # fname = '/home/export/online1/amd_app/TanksimulatorProject/testnew01/Fluid/Fluid.foam'
        # res = pvs.OpenFOAMReader(FileName=fname)
        if path:
            fname = os.path.join(path,'Solid','tank.pvd')
        else:
            # fname = '/home/export/online1/amd_app/TanksimulatorProject/testnew01/Solid/tank.pvd'
            Q.QMessageBox.information(self, '错误', '工程目录不存在后处理文件！')
        self.solidpvd = pvs.PVDReader(FileName=fname)
        self.alltimes = self.solidpvd.TimestepValues

        for array in self.solidpvd.PointArrays:
            self.sidebar.comboBox_5.addItem(array)

        # for direction in []:
        #     self.sidebar.comboBox_6.addItem(direction)

        #self.fluidfoam
        # res.CaseType = 'Decomposed Case'
        # Check if there are indeed fields that can be represented
        # self.current = res
        # pv_layout = pvs.GetLayoutByName(RESULTS_PV_LAYOUT_NAME)
        # views = pvs.GetViewsInLayout(pv_layout)
        # self.ren_view = self.views[-1]
        # self.ren_view = pvs.GetActiveView()

        # self.ren_view.ResetCamera()
        self.tankpvdDisplay = pvs.Show(self.solidpvd, self.ren_view)

        annotateTimeFilter1 = pvs.AnnotateTimeFilter(Input=self.solidpvd)
        annotateTimeFilterDisplay1 = pvs.Show(annotateTimeFilter1, self.ren_view)
        # 时间字的颜色
        # annotateTimeFilterDisplay1.Color = [0.0, 0.0, 0.5000076295109483]

        self.tankpvdDisplay.Ambient = 0.48
        # self.tankpvdDisplay.Specular = 0.68
        # 更改光线相关参数
        # self.tankpvdDisplay.Specular = 0.33
        # self.tankpvdDisplay.SpecularPower = 60.0
        # self.tankpvdDisplay.Luminosity = 46.0
        # self.tankpvdDisplay.Diffuse = 0.6

        # trace defaults for the display properties.
        self.tankpvdDisplay.Representation = 'Surface'

        self.tankpvdDisplay.SetScalarBarVisibility(self.ren_view, True)

        pvs.ColorBy(self.tankpvdDisplay, ('POINTS', 'S', 'Magnitude'))

        # # rescale color and/or opacity maps used to include current data range
        # self.tankpvdDisplay.RescaleTransferFunctionToDataRange(True, False)

        # get color transfer function/color map for 'S'
        sLUT = pvs.GetColorTransferFunction('S')

        # get opacity transfer function/opacity map for 'S'
        sPWF = pvs.GetOpacityTransferFunction('S')

        #彩虹 colorset
        # sLUT.ApplyPreset('Rainbow Uniform', True)

        # set scalar coloring
        pvs.ColorBy(self.tankpvdDisplay, ('POINTS', 'S', 'Mises'))

        # # rescale color and/or opacity maps used to exactly fit the current data range
        # self.tankpvdDisplay.RescaleTransferFunctionToDataRange(False, False)

        # Update a scalar bar component title.
        pvs.UpdateScalarBarsComponentTitle(sLUT, self.tankpvdDisplay)

        # rescale color and/or opacity maps used to exactly fit the current data range
        self.tankpvdDisplay.RescaleTransferFunctionToDataRange(False, True)
        self.currentdisplay = self.tankpvdDisplay

        if path:
            fname = os.path.join(path,'Fluid','Fluid.foam')
        else:
            # fname = '/home/export/online1/amd_app/TanksimulatorProject/testnew01/Fluid/Fluid.foam'
            # fname = '/home/export/online1/amd_app/TanksimulatorProject/testmonpoint/Fluid/Fluid.foam'
            return
        self.fluidfoam = pvs.OpenFOAMReader(FileName=fname)

        # set active source
        pvs.SetActiveSource(self.fluidfoam)

        for array in self.fluidfoam.CellArrays:
            self.sidebar.comboBox_7.addItem(array)

        #根据分量选择改变表示内容
        connect(self.sidebar.comboBox_5.activated, self.renviewchange)
        connect(self.sidebar.comboBox_6.activated, self.renviewdirchange)
        connect(self.sidebar.comboBox_7.activated, self.renviewchange1)
        # connect(self.sidebar.comboBox_8.activated, self.renviewchange1)

        #根据渐变颜色选择改变内容
        connect(self.sidebar.comboBox.activated, self.colorbarchange)
        connect(self.sidebar.comboBox_3.activated, self.colorbarchange)

        connect(self.sidebar.pushButton_2.clicked, self.raytracing)
        connect(self.sidebar.pushButton.clicked, self.raytracing)  

        connect(self.sidebar.comboBox_9.activated, self.cliping)  
        connect(self.sidebar.comboBox_10.activated, self.cliping)  

        connect(self.sidebar.groupBox_5.clicked[bool], self.resetview)
        connect(self.sidebar.groupBox_6.clicked[bool], self.resetview)

        # connect(self.sidebar.groupBox_2.clicked[bool], self._meshActivated)  
        # connect(self.sidebar.groupBox_4.clicked[bool], self._meshActivated)
        
        #self.fluidfoam
        self.fluidfoam.CaseType = 'Decomposed Case'

        # show data in view
        self.fluidfoamDisplay = pvs.Show(self.fluidfoam, self.ren_view1)

        annotateTimeFilter = pvs.AnnotateTimeFilter(Input=self.fluidfoam)
        annotateTimeFilterDisplay = pvs.Show(annotateTimeFilter, self.ren_view1)
        # annotateTimeFilterDisplay.Color = [0.0, 0.0, 0.5000076295109483]

        self.fluidfoamDisplay.Ambient = 0.48
        # self.fluidfoamDisplay.Specular = 1
        # 更改光线相关参数
        # self.fluidfoamDisplay.Specular = 0.33
        # self.fluidfoamDisplay.SpecularPower = 60.0
        # self.fluidfoamDisplay.Luminosity = 46.0
        # self.fluidfoamDisplay.Diffuse = 0.6

        # trace defaults for the display properties.
        self.fluidfoamDisplay.Representation = 'Surface'

        self.fluidfoamDisplay.SetScalarBarVisibility(self.ren_view1, True)
        self.currentdisplay1 = self.fluidfoamDisplay

    def resetview(self,needreset):
        if not needreset:
            if self.sender() == self.sidebar.groupBox_5:
                pvs.HideAll(self.ren_view)
                pvs.Show(self.solidpvd, self.ren_view)
                self.currentdisplay = self.tankpvdDisplay
            elif self.sender() == self.sidebar.groupBox_6:
                pvs.HideAll(self.ren_view1)
                pvs.Show(self.fluidfoam, self.ren_view1)
                self.currentdisplay1 = self.fluidfoamDisplay

    def cliping(self):
        if self.sender() == self.sidebar.comboBox_9:
            if not self.clip1:
                self.clip1 = pvs.Clip(Input=self.solidpvd)
            pvs.Hide3DWidgets(proxy=self.clip1.ClipType)
            if self.sender().currentText() == 'X方向':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip1.ClipType.Normal = [1.0, 0.0, 0.0]
            elif self.sender().currentText() == 'Y方向':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip1.ClipType.Normal = [0.0, 1.0, 0.0]
            elif self.sender().currentText() == 'Z方向':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip1.ClipType.Normal = [0.0, 0.0, 1.0]

            pvs.HideAll(self.ren_view)
            clip1Display = pvs.Show(self.clip1, self.ren_view)
            clip1Display.Representation = 'Surface'
            self.currentdisplay = clip1Display

        elif self.sender() == self.sidebar.comboBox_10:
            if not self.clip2:
                self.clip2 = pvs.Clip(Input=self.fluidfoam)
            pvs.Hide3DWidgets(proxy=self.clip2.ClipType)
            if self.sender().currentText() == 'X方向':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip2.ClipType.Normal = [1.0, 0.0, 0.0]
            elif self.sender().currentText() == 'Y方向':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip2.ClipType.Normal = [0.0, 1.0, 0.0]
            elif self.sender().currentText() == 'Z方向':
                # self.clip1.ClipType.Origin = [-13184.847264041935, 0.0, 150000.0]
                self.clip2.ClipType.Normal = [0.0, 0.0, 1.0]

            pvs.HideAll(self.ren_view1)
            clip2Display = pvs.Show(self.clip2, self.ren_view1)
            clip2Display.Representation = 'Surface'
            self.currentdisplay1 = clip2Display

        self.updateview()

    def raytracing(self):
        materialLibrary1 = pvs.GetMaterialLibrary()
        materialLibrary1.LoadMaterials = "/home/export/online3/amd_share/SALOME-9.4.0-CO7-SRC/INSTALL/ParaView/share/materials/ospray_mats.json"

        # if material == '清水':
        #     mat = ''
        mat = {'清水':'cleanwater','蓝色水':'water','铝':'aluminum','铜':'copper','木材':'wood',}

        if self.sender() == self.sidebar.pushButton:
            # if self.sidebar.groupBox_2.isChecked():
                pvs.SetActiveView(self.ren_view)
                view = self.ren_view
                material = self.sidebar.comboBox_2.currentText()
                ambient = self.sidebar.lineEdit.text()
                sampleperpix = self.sidebar.lineEdit_2.text()

                # Properties modified on tankpvdDisplay
                self.currentdisplay.OSPRayMaterial = mat[material]

                # Properties modified on tankpvdDisplay
                self.currentdisplay.OSPRayUseScaleArray = 1

                # Properties modified on view

                pvs.ColorBy(self.currentdisplay, ('POINTS', 'Solid Color'))

                view.EnableOSPRay = int(self.sidebar.groupBox_2.isChecked())

                # # Properties modified on view
                # view.OSPRayRenderer = 'pathtracer'

                # # Properties modified on view
                # view.AmbientSamples = int(ambient)

                # # Properties modified on view
                # view.SamplesPerPixel = int(sampleperpix)

        elif self.sender() == self.sidebar.pushButton_2:
            # if self.sidebar.groupBox_4.isChecked():
                pvs.SetActiveView(self.ren_view1)
                view = self.ren_view1
                material = self.sidebar.comboBox_4.currentText()
                ambient = self.sidebar.lineEdit_3.text()
                sampleperpix = self.sidebar.lineEdit_4.text()

                if self.sidebar.comboBox_7.currentText()=='alpha.water':
                    if not self.threshold1:
                        self.threshold1 = pvs.Threshold(Input=self.fluidfoam)

                        # Properties modified on self.threshold1
                        self.threshold1.Scalars = ['POINTS', 'alpha.water']
                        self.threshold1.ThresholdRange = [0.99, 1.0]
                        self.threshold1.AllScalars = 0

                    # show data in view
                    # 将来考虑替换为HideAll()方法
                    # pvs.Hide(self.fluidfoam, self.ren_view1)
                    pvs.HideAll(self.ren_view1)
                    Display = pvs.Show(self.threshold1, self.ren_view1)
                else:
                    if self.threshold1:
                        # 将来考虑替换为HideAll()方法
                        # pvs.Hide(self.threshold1, self.ren_view1)
                        pvs.HideAll(self.ren_view1)
                    Display = pvs.Show(self.fluidfoam, self.ren_view1)

                # Properties modified on fluidfoamDisplay
                Display.OSPRayMaterial = mat[material]

                # Properties modified on fluidfoamDisplay
                Display.OSPRayUseScaleArray = 1

                pvs.ColorBy(Display, ('POINTS', 'Solid Color'))

                # Properties modified on view
                view.EnableOSPRay = int(self.sidebar.groupBox_4.isChecked())

        # Properties modified on view
        view.OSPRayRenderer = 'pathtracer'

        # Properties modified on view
        view.AmbientSamples = int(ambient)

        # Properties modified on view
        view.SamplesPerPixel = int(sampleperpix)

        pvs.Render()

    def colorbarchange(self):
        if self.sender() == self.sidebar.comboBox:
            pvs.SetActiveView(self.ren_view)
            arrayname = self.sidebar.comboBox_5.currentText()
            color = self.sidebar.comboBox.currentText()
            uselog = int(self.sidebar.checkBox.isChecked())
        elif self.sender() == self.sidebar.comboBox_3:
            pvs.SetActiveView(self.ren_view1)
            arrayname = self.sidebar.comboBox_7.currentText()
            color = self.sidebar.comboBox_3.currentText()
            uselog = int(self.sidebar.checkBox_2.isChecked())

        # get color transfer function/color map for arrayname
        # self.colorobject[arrayname].Hide()
        self.colorobject[arrayname] = pvs.GetColorTransferFunction(arrayname)
        pvs.HideScalarBarIfNotNeeded(self.colorobject[arrayname], self.ren_view)
        pvs.HideScalarBarIfNotNeeded(self.colorobject[arrayname], self.ren_view1)
        self.colorobject[arrayname].UseLogScale = uselog

        #应用对应的 colorset
        if color == '彩虹':
            self.colorobject[arrayname].ApplyPreset('Rainbow Uniform', True)
        elif color == '冷热':
            self.colorobject[arrayname].ApplyPreset('Cold and Hot', True)
        # elif color == '红蓝':
        #     self.colorobject[arrayname].ApplyPreset('Spectral_lowBlue', True)
        # elif color == '蓝红彩虹':
        #     self.colorobject[arrayname].ApplyPreset('Blue to Red Rainbow', True)
        elif color == '红蓝':
            self.colorobject[arrayname].ApplyPreset('Blue to Red Rainbow', True)
        elif color == 'Jet':
            self.colorobject[arrayname].ApplyPreset('jet', True)

        self.updateview()

    def updateview(self):
        # if self.sender() == self.sidebar.comboBox:
            # HideUnusedScalarBars 方法来隐藏多余ScalarBars
            pvs.HideUnusedScalarBars(self.ren_view)
            self.currentdisplay.SetScalarBarVisibility(self.ren_view, True)
            self.ren_view.Update()
        # elif self.sender() == self.sidebar.comboBox_3:
            # HideUnusedScalarBars 方法来隐藏多余ScalarBars
            pvs.HideUnusedScalarBars(self.ren_view1)
            self.currentdisplay1.SetScalarBarVisibility(self.ren_view1, True)
            self.ren_view1.Update()

            pvs.Render()

    def renviewchange(self):
        arrayname = self.sidebar.comboBox_5.currentText()
        self.sidebar.comboBox_6.clear()
        if arrayname in ['S','E']:
            directs = ['Magnitude','xx','yy','zz','xy','yz','zx','Mises','Min Principal','Mid Principal','Max Principal',]
        elif arrayname == 'U':
            directs = ['Magnitude','D1','D2','D3']
        else:
            directs = []

        for d in directs:
            self.sidebar.comboBox_6.addItem(d)
        # pvs.ColorBy(self.currentdisplay, ('POINTS', arrayname, 'Mises'))
        pvs.ColorBy(self.currentdisplay, ('POINTS', arrayname))
        self.colorobject[arrayname] = pvs.GetColorTransferFunction(arrayname)
        # pvs.Render()
        self.updateview()

    def renviewdirchange(self):
        dir = self.sidebar.comboBox_6.currentText()
        arrayname = self.sidebar.comboBox_5.currentText()
        pvs.ColorBy(self.currentdisplay, ('POINTS', arrayname, dir))
        self.colorobject[arrayname] = pvs.GetColorTransferFunction(arrayname)
        # pvs.Render()
        self.updateview()

    def renviewchange1(self):
        arrayname = self.sidebar.comboBox_7.currentText()
        pvs.ColorBy(self.currentdisplay1, ('POINTS', arrayname))
        self.colorobject[arrayname] = pvs.GetColorTransferFunction(arrayname)
        # pvs.Render()
        self.updateview()

    def apply_params(self):
        """
        Called when the parameters are changed from the parameters
        modification box (and the Apply button clicked)
        """
        rep = self.params.rep
        if rep:
            new_opts = self.params.values()
            self.represent(rep.field, rep.__class__, False, **new_opts)

    def represent(self, field, repclass=ColorRep, forced=False, **opts):
        """
        Adds or overloads a representation of a result field

        field: ConceptField, field to be represented
        repclass: class definition of the representation
        opts: additional options for initializing the representation
        """
        import pvsimple as pvs

        # self.ren_view = pvs.FindViewOrCreate(RESULTS_PV_VIEW_NAME, 'RenderView')
        # print "in results.represent"
        # print "   >> self.ren_view", self.ren_view

        # Activate the hour-glass animation
        wait_cursor(True)

        updated = False
        # if isinstance(self.shown, repclass) and not forced:
        if isinstance(self.shown, repclass) and not forced:
            if self.shown.field == field:
                self.shown.update_(opts)
                updated = True

        if not updated:
            pvs.HideAll(self.ren_view)

            # Uncheck minmax
            self.minmax_btn.setChecked(False)
            #######################################################
            # Here is the actual call to the representation class #
            #######################################################
            self.shown = repclass(field, **opts)
            # Animate modes upon the initialization of a ModesRep
            if isinstance(self.shown, ModesRep):
                self.shown.animate()

        if self.minmax_shown():
            show_min_max(self.shown)

        wait_cursor(False)

        # Render the new or modified representation
        pvs.Render()

        # Update the infobar (text above the representation view)
        #隐藏infobar
        self.update_infobar()

        if updated:
            self.params.update_params()
        else:
            self.params.set_representation(self.shown)

        # Insure that the results tab is the one being shown,
        # hide the loader overlay, deactivate the hour-glass
        self.set_as_working_tab()
        if self._loader:
            self._loader.terminate()
        wait_cursor(False)

    def update_infobar(self):
        """
        Method used to update the information bar below the post-processing
        controls based on the shown field (uses self.shown)
        """
        info = 'No data loaded'
        fsuffix = ''
        if self.shown:
            field, opts = self.shown.field, self.shown.opts
            comp = opts['Component'] if 'Component' in opts else ''
            if 'ColorField' in opts:
                cfield = opts['ColorField']
                if cfield != field:
                    fsuffix = ', colored by %s' % (
                        cfield.info['label'].split('(')[0])
                    if len(cfield.info['components']) > 1:
                        fsuffix += ' [%s]' % (comp)

            if not fsuffix:
                if len(field.info['components']) > 1:
                    fsuffix = ' [%s]' % (comp)

            ctime = self.ren_view.ViewTime
            # info = '<B>Concept :</B> %s; '\
            #        '<B>Field :</B> %s%s; '\
            #        '<B>Current time/frequency :</B> %g'\
            #        %(field.concept.name,
            #          field.info['label'], fsuffix, ctime)

            info = '<B><span style="color: #ffffff; background-color: #1d71b8;">'\
                   '&nbsp;Concept&nbsp;</B></span>&nbsp;%s'\
                   '&nbsp;<B><span style="color: #ffffff; background-color: #1d71b8;">'\
                   '&nbsp;Field&nbsp;</B></span>&nbsp;%s%s'\
                   '&nbsp;<B><span style="color: #ffffff; background-color: #1d71b8;">'\
                   '&nbsp;Time/Frequency&nbsp;</B></span>&nbsp;%g'\
                   % (field.concept.name,
                      field.name, fsuffix, ctime)

        if self.infobar_label:
            self.infobar_label.setText(info)

        # if self.mem_bar:
        #     current, available = get_pv_mem_use()
        #     self.mem_bar.setRange(0, int(available / 1024.))
        #     self.mem_bar.setValue(int(current / 1024.))

    def redraw(self):
        """
        Redraws the current field
        """
        pvs.GetActiveView().ResetCamera()
        

    # pragma pylint: disable=invalid-name
    def eventFilter(self, source, event):
        """
        EventFilter for capturing mouse clicks over the ParaView
        widget.
        """
        if not hasattr(self, 'pv_widget_children'):
            return 0

        if source in self.pv_widget_children:
            #定义了在paraview视窗中双击右击操作对应的事件
            # pass
            if event.type() == Q.QEvent.MouseButtonPress:
                # self.on_click_callback()
                if hasattr(event, 'button'):
                    return 1
            elif event.type() == Q.QEvent.MouseButtonRelease:
                self.on_click_callback()
                if hasattr(event, 'button'):
                    if event.button() == Q.Qt.RightButton:
                        # self.navtree.contextMenuEvent('Representation')
                        pass
                    return 1
            # elif event.type() == Q.QEvent.MouseButtonDblClick:
            #     pvcontrol(self, 'clear_selection')
            #     return 1

        return Q.QWidget.eventFilter(self, source, event)

    def on_click_callback(self):
        """
        Callback to launch either a probing or plot operation based
        on the user selection
        """
        if not self.shown:
            return

        if not self.shown.pickable:
            return

        selection, _, _ = get_active_selection(self.shown.source)
        if selection:
            self.probe_plot_callback()
        else:
            Q.QTimer.singleShot(100, self.probe_plot_callback)

    def probe_plot_callback(self):
        """
        Delayed probe as to allow selection to be coined
        """
        selection, _, _ = get_active_selection(self.shown.source)
        if selection:
            if self.probing:
                selection_probe(self)
            else:
                selection_plot(self)
                self.probing = True

    def plot(self, data, variable):
        """
        Adds a popup dialog with a plot of the given data
        """
        dialog = Q.QDialog(self)
        dialog.ui = PlotWindow(data=data, variable=variable)
        dialog.ui.setWindowTitle('AsterStudy - Selection plot over time')
        dialog.ui.show()


def add_button(layout, name='', tooltip='', icon=None,
               callback=None, checkable=False):
    """
    Adds a push button to the given parent widget and layout with some
    user-defined properties
    """
    button = Q.QPushButton(name)

    if tooltip:
        button.setToolTip(tooltip)
    # if icon:
    #     button.setIcon(get_icon(icon))
    button.setCheckable(checkable)
    if checkable:
        button.toggled.connect(callback)
    else:
        button.clicked.connect(callback)

    layout.addWidget(button)
    return button


def add_separator(layout, width=2, color='#fff'):
    """
    Adds a "fake" separator
    """
    sep = Q.QWidget()
    sep.setMinimumWidth(width)
    sep.setMaximumWidth(width)
    # White makes the separator hidden
    sep.setStyleSheet('background-color:{};'.format(color))
    sep.setSizePolicy(Q.QSizePolicy.Fixed,
                      Q.QSizePolicy.Minimum)
    layout.addWidget(sep)
    return sep
