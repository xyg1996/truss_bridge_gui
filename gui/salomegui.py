


#


"""
ASTERSTUDY module: SALOME wrapping for AsterStudy application.

SALOME GUI
----------

Implementation of ASTERSTUDY SALOME GUI - a wrapper for AsterStudy
application.

"""



import zipfile

import PyQt5.Qt as Q

from ..common import (FilesSupplier, MeshElemType, common_filters,
                      debug_message, enable_except_hook,
                      external_files_callback, get_base_name, get_file_name,
                      info_message, is_medfile, translate)
from . import Context, NodeType, Panel, WorkingMode, check_selection, str2font
from .astergui import AsterGui
from .behavior import behavior
# from .controller import Controller
from .meshview import MeshBaseView, MeshView, elem2smesh
from .prefmanager import tab_position
# from .remotefs import MountWorker
from .salomegui_utils import get_salome_gui, get_salome_pyqt
from .widgets import PopupFrame

import shutil
from pathlib import Path
import os

def get_aster_view_type():
    """
    Get Aster workspace view type name.

    Returns:
        string: AsterStudy workspace's type name
    """
    # return 'AsterWorkspace'
    return 'PFsalome'

class MeshObjects(FilesSupplier):
    """Provides access to SMESH Mesh data."""
    # pragma pylint: disable=no-member

    def files(self, file_format=None):
        """
        Redefined from FilesSupplier.
        Get list of SMESH Mesh objects.
        """
        # pragma pylint: disable=import-error,protected-access
        files = []
        if file_format is None or file_format in ('MED',):
            try:
                import salome
                import SMESH
                smesh = salome.myStudy.FindComponent('SMESH')
                if smesh:
                    iterator = salome.myStudy.NewChildIterator(smesh)
                    while iterator.More():
                        sobj = iterator.Value()
                        obj = sobj.GetObject()
                        uid = sobj.GetID()
                        if isinstance(obj, SMESH._objref_SMESH_Mesh):
                            files.append(uid)
                        iterator.Next()
            except (AttributeError, ImportError):
                pass
        return files

    def filename(self, uid):
        """
        Redefined from FilesSupplier.
        Get name of SMESH Mesh object by entry specified with *uid*.
        """
        # pragma pylint: disable=import-error
        try:
            import salome
            sobj = salome.myStudy.FindObjectID(uid)
            if sobj and sobj.GetAllAttributes():
                return sobj.GetName()
        except (ImportError, AttributeError):
            pass
        return None

    def groups(self, uid, group_type):
        """
        Redefined from FilesSupplier.
        Get names of groups for given SMESH Mesh object.
        """
        # pragma pylint: disable=import-error,protected-access
        groups = []
        try:
            import salome
            import SMESH
            sobj = salome.myStudy.FindObjectID(uid)
            if sobj and sobj.GetAllAttributes():
                mesh = sobj.GetObject()
                if mesh and isinstance(mesh, SMESH._objref_SMESH_Mesh):
                    stypes = MeshView.smesh_types(group_type)
                    groups = [i.GetName() for i in mesh.GetGroups() \
                                  if i.GetType() in stypes]
        except (ImportError, AttributeError):
            pass
        return groups

    def groups_by_type(self, uid, elem_type, with_size=False):
        """
        Redefined from FilesSupplier.
        Get names of groups for given SMESH Mesh object.
        """
        # pragma pylint: disable=import-error,protected-access
        groups = []
        try:
            import salome
            import SMESH
            from salome.smesh import smeshBuilder
            smesh = smeshBuilder.New()
            sobj = salome.myStudy.FindObjectID(uid)
            if elem_type in MeshElemType.list_elem_types() \
                    and sobj and sobj.GetAllAttributes():
                mesh = sobj.GetObject()
                if mesh and isinstance(mesh, SMESH._objref_SMESH_Mesh):
                    wobj = smesh.Mesh(mesh, sobj.GetName())
                    all_groups = mesh.GetGroups()
                    for group in all_groups:
                        if group.GetType() in elem2smesh(elem_type):
                            if with_size:
                                name = group.GetName()
                                occs = max(len(wobj.GetGroupByName(name, SMESH.ALL)) \
                                         - len(wobj.GetGroupByName(name, SMESH.NODE)), 1)
                                groups.append((name.rstrip(),
                                               group.Size(),
                                               occs))
                            else:
                                groups.append(group.GetName().rstrip())
        except (ImportError, AttributeError):
            pass
        return groups

    def export_to_med(self, uid, filepath):
        """
        Export the MESH object with entry `uid` to `filepath`.

        Arguments:
            uid (str): entry of the object
            filepath (str): path where to export it as a file
        """
        # pragma pylint: disable=import-error,no-name-in-module,protected-access
        try:
            import salome
            from salome.smesh import smeshBuilder
            sobj = salome.myStudy.FindObjectID(uid)
            smesh = smeshBuilder.New()
            import SMESH
            corba_obj = sobj.GetObject()
            assert isinstance(corba_obj, SMESH._objref_SMESH_Mesh)
            mesh_obj = smesh.Mesh(corba_obj, sobj.GetName())
            mesh_obj.ExportMED(filepath, 0)
        except (ImportError, AttributeError):
            pass

external_files_callback(MeshObjects(), True)


def enable_salome_actions(enable):
    """
    Show / hide unnecessary SALOME actions

    Note:
        This is a workaround until SALOME GUI is not improved to provide
        better way to do this.
    """
    import SalomePyQt
    menu = get_salome_pyqt().getPopupMenu(SalomePyQt.Edit)
    for action in menu.actions():
        action.setVisible(enable)

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class SalomePreferencesMgr:
    """A wrapper for preference management in SALOME."""

    # pragma pylint: disable=no-self-use
    def value(self, key, default=None):
        """
        Get preference option's value.

        Arguments:
            key (str): Option's name.
            default (Optional[str]). Default value for the option.
                Defaults to *None*.

        Returns:
            str: Option's value.
        """
        section, parameter = self._splitKey(key)
        value = get_salome_pyqt().stringSetting(section, parameter, default, True)
        if value.startswith("@ByteArray"):
            try:
                value = get_salome_pyqt().byteArraySetting(section, parameter)
            except AttributeError:
                info_message(translate("PrefDlg", "WARNING: can not yet "
                                       "restore setting {0}.".format(key)))
        return value

    # pragma pylint: disable=no-self-use
    def int_value(self, key, default=0):
        """
        Get preference option's value as an integer.

        Arguments:
            key (str): Option's name.
            default (Optional[int]). Default value for the option.
                Defaults to 0.

        Returns:
            int: Option's value.
        """
        section, parameter = self._splitKey(key)
        return get_salome_pyqt().integerSetting(section, parameter, default)

    # pragma pylint: disable=no-self-use
    def float_value(self, key, default=.0):
        """
        Get preference option's value as a float.

        Arguments:
            key (str): Option's name.
            default (Optional[float]). Default value for the option.
                Defaults to 0.0.

        Returns:
            float: Option's value.
        """
        section, parameter = self._splitKey(key)
        return get_salome_pyqt().doubleSetting(section, parameter, default)

    # pragma pylint: disable=no-self-use
    def bool_value(self, key, default=False):
        """
        Get preference option's value as a boolean.

        Arguments:
            key (str): Option's name.
            default (Optional[bool]). Default value for the option.
                Defaults to *False*.

        Returns:
            bool: Option's value.
        """
        section, parameter = self._splitKey(key)
        return get_salome_pyqt().boolSetting(section, parameter, default)

    # pragma pylint: disable=no-self-use
    def str_value(self, key, default="", subst=True):
        """
        Get preference option's value as a string.

        Arguments:
            key (str): Option's name.
            default (Optional[str]). Default value for the option.
                Defaults to empty string.
            subst (Optional[bool]). Flag specifying if it's necessary to
                perform auto-substitution of variables. Defaults to
                *True*.

        Returns:
            str: Option's value.
        """
        section, parameter = self._splitKey(key)
        return get_salome_pyqt().stringSetting(section, parameter, default, subst)

    # pragma pylint: disable=no-self-use
    def font_value(self, key, default=Q.QFont()):
        """
        Get preference option's value as *QFont*.

        Arguments:
            key (str): Option's name.
            default (Optional[int]). Default value for the option.
                Defaults to null font.

        Returns:
            QFont: Option's value.
        """
        section, parameter = self._splitKey(key)
        try:
            return get_salome_pyqt().fontSetting(section, parameter, default)
        except AttributeError:
            text = get_salome_pyqt().stringSetting(section, parameter,
                                                   default.toString(), True)
            return str2font(text)

    # pragma pylint: disable=no-self-use
    def color_value(self, key, default=Q.QColor()):
        """
        Get preference option's value as *QColor*.

        Arguments:
            key (str): Option's name.
            default (Optional[int]). Default value for the option.
                Defaults to null color.

        Returns:
            QColor: Option's value.
        """
        section, parameter = self._splitKey(key)
        return get_salome_pyqt().colorSetting(section, parameter, default)

    # pragma pylint: disable=no-self-use
    def setValue(self, key, value):
        """
        Set preference option's value.

        Arguments:
            key (str): Option's name.
            value (any). Option's value.
        """
        section, parameter = self._splitKey(key)
        get_salome_pyqt().addSetting(section, parameter, value)

    # pragma pylint: disable=no-self-use
    def contains(self, key):
        """
        Check if option is known by preference manager.

        Arguments:
            key (str): Option's name.

        Returns:
            bool: *True* if this is a known option; *False* otherwise.
        """
        section, parameter = self._splitKey(key)
        return get_salome_pyqt().hasSetting(section, parameter)

    def _splitKey(self, key):
        """
        Split option to section and key components.

        For example, _splitKey('aaa/bbb') will return ('aaa', 'bbb').

        If section is not given, it defaults to name of the module.

        Arguments:
            key (str): Option's name.

        Returns:
            (str, str): Section and key components of option.
        """
        separator = '/'
        section, parameter = '', key
        if separator in key:
            index = key.index(separator)
            section, parameter = key[:index], key[index+1:]
        return section if section else AsterSalomeGui.NAME, parameter


class AsterSalomeGui(AsterGui):
    """ASTERSTUDY SALOME module GUI."""

    NAME = 'ASTERSTUDY'
    _prefMgr = None

    def __init__(self):
        """Create GUI instance."""
        AsterGui.__init__(self)
        self._loader = None
        self.currentpath = None
        self.work_space = self._createWorkspace(self.main_window)
        # self.work_space.set_workingdir.connect(self.save)

    # def save_prepare(self):
    #     import salome
    #     self.work_space.default_file_root = self.work_space.pimplefoam_root + '/defaultfile'
    #     self.work_space.cwd = '/usr/sw-cluster/simforge/PFsalome/SALOME-9.4.0-CO7-SRC/BINARIES-CO7/ASTERSTUDY/lib/python3.6/site-packages'
    #     filedir = self.work_space.get_dir_name()
    #     if filedir:
    #         filedir += '/workingdirectory'
    #         inittree(filedir,self.work_space.default_file_root)
    #         self.work_space.workingdirectory = filedir
    #         self.work_space.update_workingdir_for_dialogs(self.work_space.workingdirectory)
    #         self.save(filedir)
    #     else:
    #         pass
    # pragma pylint: disable=no-self-use
    def createMenu(self, text, parent=-1, group=-1):
        """
        Create menu item in the main menu of application.

        Menu item is specified by its label. If there is already a menu
        with given text, its identifier is returned.

        Parent menu is specified via the identifier; -1 means top-level
        menu.

        Menu items are combined into groups; -1 means most bottom (last)
        group.

        Arguments:
            text (str): Text label of menu item.
            parent (Optional[int]): Parent menu item. Defaults to -1.
            group (Optional[int]): Menu group. Defaults to -1.

        Returns:
            int: Menu item's unique identifier.

        Raises:
            RuntimeError: If parent menu was not found.

        See also:
            `addMenuAction()`
        """
        return get_salome_pyqt().createMenu(text, parent, -1, group)

    # pragma pylint: disable=no-self-use
    def addMenuAction(self, action, parent, group=-1):
        """
        Add action to the menu.

        Similarly to menu items, actions are combined into groups;
        see `createMenu()` for more details.

        Arguments:
            action (QAction): Menu action.
            parent (int): Parent menu item.
            group (Optional[int]): Menu group. Defaults to -1.

        Raises:
            RuntimeError: If parent menu was not found.

        See also:
            `createMenu()`
        """
        if action is None:
            action = get_salome_pyqt().createSeparator()
        get_salome_pyqt().createMenu(action, parent, -1, group)

    # pragma pylint: disable=no-self-use
    def createToolbar(self, text, name):
        """
        Create toolbar.

        Toolbar is specified by its label and name.
        Label normally is specified as a text translated to the current
        application's language, while name should not be translated - it
        is used to properly save and restore positions of toolbars.

        Arguments:
            text (str): Text label of toolbar.
            name (str): Unique name of toolbar.

        Returns:
            int: Toolbar's unique identifier.

        See also:
            `addToolbarAction()`
        """
        return get_salome_pyqt().createTool(text, name)

    # pragma pylint: disable=no-self-use
    def addToolbarAction(self, action, parent):
        """
        Add action to the toolbar.

        Arguments:
            action (QAction): Toolbar action.
            parent (int): Parent toolbar.

        Raises:
            RuntimeError: If parent toolbar was not found.

        See also:
            `createToolbar()`
        """
        if action is None:
            action = get_salome_pyqt().createSeparator()
        get_salome_pyqt().createTool(action, parent)

    @classmethod
    def preferencesMgr(cls):
        """
        Get preferences manager.

        Returns:
            object: Application's Preferences manager.
        """
        if cls._prefMgr is None:
            cls._prefMgr = SalomePreferencesMgr()
        return cls._prefMgr

    def createPreferences(self):
        """Export preferences to common Preferences dialog."""
        # pragma pylint: disable=too-many-statements

        import SalomePyQt
        def _addSpacing(_title, _gid):
            spacer = get_salome_pyqt().addPreference(_title, _gid, SalomePyQt.PT_Space)
            get_salome_pyqt().setPreferenceProperty(spacer, "hsize", 0)
            get_salome_pyqt().setPreferenceProperty(spacer, "vsize", 10)
            get_salome_pyqt().setPreferenceProperty(spacer, "hstretch", 0)
            get_salome_pyqt().setPreferenceProperty(spacer, "vstretch", 0)

        # 'General' page
        title = translate("PrefDlg", "General")
        gid = get_salome_pyqt().addPreference(title)

        # Workspace tab pages position
        title = translate("PrefDlg", "Workspace tab pages position")
        item = get_salome_pyqt().addPreference(title,
                                               gid,
                                               SalomePyQt.PT_Selector,
                                               AsterSalomeGui.NAME,
                                               "workspace_tab_position")
        values = []
        values.append(translate("PrefDlg", "North"))
        values.append(translate("PrefDlg", "South"))
        values.append(translate("PrefDlg", "West"))
        values.append(translate("PrefDlg", "East"))
        get_salome_pyqt().setPreferenceProperty(item, "strings", values)
        values = ["north", "south", "west", "east"]
        get_salome_pyqt().setPreferenceProperty(item, "ids", values)

        # Initial workspace view
        title = translate("PrefDlg", "默认打开的标签页")
        item = get_salome_pyqt().addPreference(title,
                                               gid,
                                               SalomePyQt.PT_Selector,
                                               AsterSalomeGui.NAME,
                                               "workspace_initial_view")
        values = []
        # values.append(translate("PrefDlg", "History view"))
        # values.append(translate("PrefDlg", "Case view"))
        values.append('参数化几何建模')
        values.append('前处理')
        values.append('仿真设置')
        values.append('计算监控')
        values.append('后处理')
        get_salome_pyqt().setPreferenceProperty(item, "strings", values)
        # values = [WorkingMode.value2pref(WorkingMode.HistoryMode),
        #           WorkingMode.value2pref(WorkingMode.CaseMode)]
        values = list(range(4))
        get_salome_pyqt().setPreferenceProperty(item, "ids", values)

        # Add spacing
        _addSpacing("2", gid)

        # --- end of 'Confirmations' page

        if hasattr(SalomePyQt, 'UserDefinedContent'):
            from .widgets.dirwidget import DirWidget

            # 'Catalogs' page
            title = translate("PrefDlg", "Catalogs")
            gid = get_salome_pyqt().addPreference(title)

            # User's catalogs
            title = translate("PrefDlg", "User's catalogs")
            sgid = get_salome_pyqt().addPreference(title, gid)
            item = get_salome_pyqt().addPreference('',
                                                   sgid,
                                                   SalomePyQt.PT_UserDefined,
                                                   AsterSalomeGui.NAME,
                                                   "user_catalogs")
            widget = DirWidget.instance()
            get_salome_pyqt().setPreferencePropertyWg(item, "content", widget)

            # --- end of 'Catalogs' page

    def preferenceChanged(self, section, name):
        """
        Called when preferences item is changed in Preferences dialog.

        Arguments:
            section (str): Resource section's name.
            name (str): Resource parameter's name.
        """
        has_changes = False

        if section == AsterSalomeGui.NAME:
            has_changes = True
            self.from_preferences() # re-initialize behavior from preferences
            if name == "workspace_tab_position":
                if self.work_space is not None:
                    tbposition = behavior().workspace_tab_position
                    self.work_space.setTabPosition(tab_position(tbposition))
            elif name in ("use_business_translations", "content_mode"):
                self.updateTranslations()
            elif name == "sort_stages":
                self.workSpace().view(Context.DataFiles).resort()
            elif name in ("show_related_concepts", "join_similar_files"):
                self.workSpace().view(Context.DataFiles).update()
            elif name in ("show_catalogue_name", "show_comments",
                          "show_categories"):
                self.workSpace().view(Context.DataSettings).update()
            elif name in ("show_catalogue_name_data_files",):
                self.workSpace().view(Context.DataFiles).update()
            elif name == "auto_hide_search":
                view = self.workSpace().view(Context.DataSettings)
                view.setAutoHideSearch(behavior().auto_hide_search)
            elif name == "show_readonly_banner":
                self._updateWindows()
            elif name == "summary_chunk":
                self.workSpace().panel(Panel.View).updateInfo()

        elif section == "PyEditor":
            has_changes = True

        if has_changes:
            self.preferencesChanged.emit(self.preferencesMgr())

    def showNotification(self, text, timeout=-1):
        """Reimplemented from AsterGui."""
        spq = get_salome_pyqt()
        return spq.showNotification(text, "AsterStudy", timeout) \
            if hasattr(spq, 'showNotification') else -1

    def hideNotification(self, textorid):
        """Reimplemented from AsterGui."""
        spq = get_salome_pyqt()
        if hasattr(spq, 'hideNotification'):
            spq.hideNotification(textorid)

    def activate(self):
        """Activate Tanksimulator GUI."""
        info_message("PFsalome is activating...")
        self._loader = BackgroundLoading(self.main_window,msg='正在载入App,请稍候...')
        self._loader.start()

        if int(os.getenv("ASTER_NO_EXCEPTHANDLER", "0")) == 0:
            enable_except_hook(True)
        enable_salome_actions(False)
        view = get_salome_pyqt().findViews(get_aster_view_type())

        if view:
            reactivate = True
            get_salome_pyqt().setViewVisible(view[0], True)
            # self.work_space.result01.detach(keep_pipeline=False)

        else:
            reactivate = False
            print("else: Creating workspace...")
            
            info_message("workspace is ready.")
            view = get_salome_pyqt().createView(get_aster_view_type(), self.work_space)
            views = get_salome_pyqt().getViews()
            get_salome_pyqt().setViewTitle(views[1],'Smesh')
            get_salome_pyqt().setViewTitle(views[0],'Geometry')
            get_salome_pyqt().setViewClosable(view, True)
            get_salome_pyqt().setViewTitle(view,get_aster_view_type())

        self._connectWorkspace()

        self.work_space.activate(True)

        if hasattr(get_salome_pyqt(), "createRoot"):
            get_salome_pyqt().createRoot()
        else:
            children = get_salome_pyqt().getChildren()
            if not children:
                get_salome_pyqt().createObject()

        self._loader.terminate()
        get_salome_pyqt().enableSelector()
        info_message("PFsalome activated")
        
        # self.work_space.work_space_tool.ui.pushButton_15.clicked.connect(self.save_prepare)

    def deactivate(self):
        """Deactivate AsterStudy GUI."""

        # If ParaView view is initialized in Asterstudy workspace,
        # move it back to the SALOME workspace
        # if self.work_space:
        #     # results = self.work_space.view(Context.Results)
        #     # if results.pv_view:
        #     #     results.detach(keep_pipeline=True)
        #     #     self.work_space.setWorkingMode(WorkingMode.CaseMode)
        #     # if self.work_space.result01.pv_view:
        #     self.work_space.result01.detach(keep_pipeline=True)

        if self.work_space:
            # self.work_space.panels[Panel.View].deactivate()
            self.work_space.activate(False)
        view = get_salome_pyqt().findViews(get_aster_view_type())
        if view:
            get_salome_pyqt().setViewVisible(view[0], False)
        if int(os.getenv("ASTER_NO_EXCEPTHANDLER", "0")) == 0:
            enable_except_hook(False)
        enable_salome_actions(True)
        get_salome_pyqt().disableSelector()

    def save(self, directory, url):
        """
        Save module data to files; returns file names.

        The function saves the module data to the files in a temporary
        directory specified as a parameter and returns names if files in
        which module data is saved.

        Arguments:
            directory (str): A directory to store data files. Note: this
                can be not a final study destination folder but a
                temporary directly, depending on used save mode
                (single-file or multi-file).

            url (str): Actual study URL (the final study destination).
                Note: this parameter is provided for information
                purposes only! Depending on version of SALOME being used
                this parameter may be empty!

        Returns:
            list[str]: names of files in which data is saved
        """

        # if Path(url[:-4]).is_dir():
        #     self.work_space.maincontrol.currentpath = url[:-4]
            
        #     if not self.work_space.maincontrol.addcase():
        #         return []
        # else:

        # print(directory)
        # os.mkdir(url[:-4])
        # self.work_space.workingdirectory = url[:-4]
        # workpath = self.work_space.workingdirectory
        # allfiles = []
        # print(self.work_space.workingdirectory)
        # z = zipfile.ZipFile(directory+'all.zip', 'w')
        # import glob
        # filelist = ['*.med','*.unv','log.*','savedata.json','Fluid/processor*/0','Fluid/processor*/constant','Fluid/system',]
        # filelist += ['Fluid/0','Fluid/constant']
        # for pattern in filelist:
        #     for unv in glob.glob(workpath+'/'+pattern):
        #         #shutil.copyfile(unv,directory+Path(unv).relative_to(Path(workpath)))
        #         #allfiles.append(Path(unv).name)
        #         if Path(unv).is_dir():
        #             for root, dirs, files in os.walk(unv):
        #                 for f in files:
        #                     f1 = root + '/' + f
        #                     z.write(f1,Path(f1).relative_to(Path(workpath)))
                            
        #         elif Path(unv).is_file():
        #             z.write(unv,Path(unv).relative_to(Path(workpath)))

        # workpath = url[:-4]
        # self.work_space.workingdirectory = workpath



        # self.work_space.maincontrol._msg.setText('当前工程文件目录是:'+workpath)
        #路径宽度过长会将页面撑的过长
        # if len(workpath)>50:
        #     self.work_space.maincontrol._msg.setText('当前工程文件目录是:'+workpath[-50:])
        # else:
        #     self.work_space.maincontrol._msg.setText('当前工程文件目录是:'+workpath)
        # z.close()

        #return allfiles
        # return ['all.zip']
        print(url)
        print(directory)
        return ['all.zip']

    def load(self, files, url):
        """
        Load data from the files; return result status.

        The function restores module data from the files specified as a
        parameter; returns *True* in case of success or *False*
        otherwise.

        Arguments:
            files (list[str]): Data files in which module data is
                stored. Note: first element of this list is a directory
                name. File names are normally specified as relative to
                this directory.

            url (str): Actual study URL (the original study file path).
                Note: this parameter is provided for information
                purposes only! Depending on version of SALOME being used
                this parameter may be empty!

        Returns:
            bool: *True* in case of success; *False* otherwise
        """
        # written by dzj on 2019/1/9
        print(files)
        if not url:
            return False
        self.currentpath = url[:-4]
        
        #self.work_space.maincontrol. 调用保存当前算例功能
        #self.work_space.maincontrol.addcase()
        
        # if Path(self.currentpath).is_dir():
        #     Q.QMessageBox.information(self, 'Title', 'fa'+self.currentpath, Q.QMessageBox.Yes)
        #     return Fal

        if not Path(self.currentpath).is_dir():
            # z = zipfile.ZipFile(files[0]+files[1], 'r')
            # z.extractall(self.currentpath)
            #shutil.copytree(files[0],self.currentpath)
            
            #copytree(files[0],self.currentpath)
            #shutil.unpack_archive(files[0]+files[-1],self.currentpath)
            shutil.unpack_archive(files[0]+files[-1],self.currentpath)
        else:
            pass
            #TODO
            #ask if overwrite

        return True

    def close(self):
        """Clean-up data model to handle study closure."""
        if self._loader:
            self._loader.closure_tasks()

        # delete directory with embedded files
        if self.study():
            # self.study().history.clean_embedded_files()
            pass

        # Controller.abortAll()
        ###改动
        # self.work_space.result01.detach(keep_pipeline=False)

        self.work_space = None
        

    def hasModule(self, name):
        """Reimplemented from AsterGui."""
        try:
            return get_salome_gui().getComponentUserName(name) is not None
        except (ImportError, AttributeError):
            pass
        return False

    def showResults(self):
        """Reimplemented from AsterGui."""
        selected = self.selected(Context.DataFiles)
        if check_selection(selected, size=1, typeid=NodeType.Unit):
            node = self.study().node(selected[0])

            if node.filename is None:
                return

            if not os.path.exists(node.filename):
                message = translate("AsterStudy", "File '{}' does not exist.")
                message = message.format(node.filename)
                Q.QMessageBox.critical(self.mainWindow(), "AsterStudy",
                                       message)
                return

            self.showResultsFile(node.filename)

    def showResultsFile(self, filename):
        """Show results from a MED file in 'Results' tab.

        Arguments:
            filename (str): MED file to be opened.
        """
        return
        size_mb = os.path.getsize(filename) / (1024. * 1024)

        # Show a loading message as this action is not instantaneous
        results = self.workSpace().view(Context.Results)
        if results.pv_view:
            msg = translate("AsterStudy",
                            "Loading result file ({0:.1f} MB)"
                            .format(size_mb))
        else:
            msg = translate("AsterStudy",
                            "Initializing post-processor "
                            "and loading result file ({0:.1f} MB)"
                            .format(size_mb))
        loader = LoadingMessage(self.main_window, msg, True)

        results.load_med_result(filename, loader)

    def showExternalResults(self):
        """Open a results file in MED format in the Resuls tab."""
        msg = translate("AsterStudy",
                        "The result file must be in the MED format "
                        "and created by code_aster.\n"
                        "Otherwise the post-processing will fail!")
        buttons = Q.QMessageBox.Ok | Q.QMessageBox.Cancel
        answ = Q.QMessageBox.warning(self.mainWindow(), "AsterStudy",
                                     msg, buttons, Q.QMessageBox.Ok)
        if answ != Q.QMessageBox.Ok:
            return

        file_name = get_file_name(1, self.mainWindow(),
                                  "Select a results file in MED format", "",
                                  [common_filters()[0], common_filters()[-1]])
        if not file_name:
            return

        if not is_medfile(file_name):
            msg = translate("AsterStudy",
                            "The selected file is not in MED format.")
            Q.QMessageBox.critical(self.mainWindow(), "AsterStudy", msg)
            return

        self.showResultsFile(file_name)

    def createMeshView(self, parent=None):
        """Reimplemented from AsterGui."""
        no_mesh_view = behavior().no_mesh_view
        return MeshView(self, parent) if not no_mesh_view and \
            hasattr(get_salome_pyqt(), 'getViewWidget') \
            else MeshBaseView(self, parent)

    def _createMainWindow(self):
        """Initialize main window of application."""
        self.main_window = get_salome_pyqt().getDesktop()

    def _updateActions(self):
        """Update state of actions, menus, toolbars, etc."""
        return
        # AsterGui._updateActions(self)

        # has_study = self.study() is not None
        # is_modified = has_study and self.study().isModified()
        # get_salome_pyqt().setModified(is_modified)

    def autosave(self):
        """Calls SALOME save mechanism"""
        # disable pylint, `salome` module only known within salome python shell
        import salome # pragma pylint: disable=import-error
        salome.salome_init() # necessary or not?
        salome.myStudy.Save(False, False)

    def onSelectionUpdated(self, entryList):
        """
        called when selection is modified on other views (modules, viewers...)
        """
        # # Look if the group widget is on display
        # if self.workSpace().workingMode() == WorkingMode.CaseMode:
        #     edit_panel = self.workSpace().panel(Panel.Edit)
        #     if edit_panel is not None:
        #         editor = edit_panel.editor()
        #         if isinstance(editor, ParameterPanel):
        #             current_pwin = editor.currentParameterView()
        #             if isinstance(current_pwin, ParameterMeshGroupWindow):
        #                 current_pview = current_pwin.view()
        #                 mview = current_pview.meshview()
        #                 if not mview.enable_selection:
        #                     return
        #                 # Tick box for all selected objects
        #                 import salome
        #                 grnames = [salome.IDToSObject(e).GetName() \
        #                             for e in entryList]
        #                 current_pview.setSelectedMeshGroups(grnames, True)

        # Mesh VTK视窗双向交互
        
        # if self.workSpace().workingMode() == WorkingMode.QianchuliMode:
        # if self.workSpace().workingMode() == 1:
        #     mview = self.workSpace().panels[Panel.View]
        #     if not mview.enable_selection:
        #         return
        #     # Tick box for all selected objects
        #     import salome
        #     grnames = [salome.IDToSObject(e).GetName() \
        #                 for e in entryList]
        #     # current_pview.setSelectedMeshGroups(grnames, True)
        #     print(grnames)
        #     self.workSpace().Qianchuli.setSelectedMeshGroups(grnames, True)

class LoadingMessage(Q.QObject):
    """Object that manages loading messages."""

    def __init__(self, parent, message="Loading", closable=True):
        """Initialization.

        Arguments:
            parent (QWidget): Parent widget.
        """
        super().__init__()

        self._done = False
        self.widget = None
        self.timer = None
        self.parent = parent
        self.message = message
        self.closable = closable

    def start(self, interval=1000):
        """Shows a loading page that is maintained until it is done."""
        self.widget = PopupFrame(self.parent,
                                 msg=self.message,
                                 closable=self.closable)
        self.widget.move(0, 0)
        self.widget.resize(self.parent.width(), self.parent.height())
        self.widget.show()
        self.widget.closed.connect(self.close)

        self.timer = Q.QTimer(self.widget)
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.check_end)
        self.timer.start()
        self.init_tasks()

    # pragma pylint: disable=no-self-use
    def init_tasks(self):
        """Execute initialization tasks"""
        return

    # pragma pylint: disable=no-self-use
    def closure_tasks(self):
        """Execute closure tasks"""
        return

    def close(self):
        """Closes the popup manually (without interrupting tasks that are
        eventually running in background).
        """
        self.terminate()
        self.check_end()

    def check_end(self):
        """Check if the loading popup can be closed."""
        if self._done:
            self.timer.stop()
            self.widget.close()

    def terminate(self):
        """Note that the loading is terminated."""
        self._done = True

class BackgroundLoading(LoadingMessage):
    """Object that manage the loading of the module."""

    def __init__(self, parent, msg=''):
        """Initialization.

        Arguments:
            parent (QWidget): Parent widget.
        """
        # msg = translate("AsterStudy",
        #                 "Please wait while AsterStudy "
        #                 "finishes loading...")
        if not msg:
            msg = '未指定过度文字信息'
        LoadingMessage.__init__(self, parent, msg)
        # self.mountWorker = MountWorker()

    def init_tasks(self):
        """Execute initialization tasks"""
        if behavior().connect_servers_init:
            self.mount()

    def closure_tasks(self):
        """Execute closure tasks"""
        self.unmount()

    def mount(self):
        """Start thread to mount remote filesystems."""
        # self.mountThread.start()
        # self.mountStarted.emit()
        # self.mountWorker.mount()
        pass

    def unmount(self):
        """Unmount remote filesystems."""
        # self.mountWorker.unmount()
        pass

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
