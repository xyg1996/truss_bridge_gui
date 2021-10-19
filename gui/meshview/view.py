


#


"""
Mesh view
---------

Implementation of mesh view for SALOME ASTERSTUDY module.

"""


from contextlib import contextmanager

from PyQt5 import Qt as Q

from ...common import (MeshElemType, MeshGroupType, change_cursor, connect,
                       debug_message, disconnect, is_reference)
from ..behavior import behavior
from ..salomegui_utils import (decode_view_parameters, get_salome_gui,
                               get_salome_pyqt, publish_meshes)
from .baseview import MeshBaseView

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


def get_smesh_gui():
    """
    Get SMESH GUI Python interface.
    """
    if not hasattr(get_smesh_gui, 'smesh_gui'):
        import salome
        get_smesh_gui.smesh_gui = salome.ImportComponentGUI('SMESH')
    return get_smesh_gui.smesh_gui


def find_mesh_by_name(meshfile=None, meshname=None):
    """
    Search mesh object in the SALOME study.

    If *meshname* is not given, last published mesh object from
    *meshfile* is returned.

    If *meshfile* is not given, last published in the study with given
    *meshname* is returned.

    If both *meshfile* and *meshname* are not given, last published
    in the study mesh object is returned.

    Arguments:
        meshfile (Optional[str]): Mesh file name. Defaults to *None*.
        meshname (Optional[str]): Name of the mesh. Defaults to *None*.

    Returns:
        SObject: SALOME study object (*None* if mesh is not found).
    """
    import salome
    import SMESH

    meshobjs = []

    if is_reference(meshfile): # 'meshfile' is entry
        return salome.myStudy.FindObjectID(meshfile)

    # find SMESH component
    smesh_component = salome.myStudy.FindComponent('SMESH')
    if smesh_component is not None:
        # iterate through all children of SMESH component, i.e. mesh objects
        iterator = salome.myStudy.NewChildIterator(smesh_component)
        while iterator.More():
            sobject = iterator.Value() # SALOME study object (SObject)
            name = sobject.GetName() # study name of the object
            comment = sobject.GetComment() # file name (see register_meshfile)
            tag = sobject.Tag() # tag (row number)

            # name is empty if object is removed from study
            # tag for mesh object is >= SMESH.Tag_FirstMeshRoot
            if name and tag >= SMESH.Tag_FirstMeshRoot:
                if meshfile is None or comment == meshfile:
                    if not meshname or name == meshname:
                        meshobjs.append(sobject)
            iterator.Next()

    # return last found object (study object)
    return meshobjs[-1] if meshobjs else None


@contextmanager
def selection_feedback(meshview, is_enabled):
    """Context manager enabling selection feedback"""
    try:
        oldstate = meshview.enable_selection
        meshview.enable_selection = is_enabled
        yield
    finally:
        meshview.enable_selection = oldstate

def elem2smesh(elem_type):
    """
    Mapping from Asterstudy's element types into SMESH types.

    Arguments:
        elem_type(int): Asterstudy type as defined by *MeshElemType* class.

    Returns:
        tuple: corresponding SMESH types
    """
    try:
        import SMESH
        type_dict = {MeshElemType.ENode: (SMESH.NODE,),
                     MeshElemType.E0D: (SMESH.ELEM0D, SMESH.BALL,),
                     MeshElemType.E1D: (SMESH.EDGE, ),
                     MeshElemType.E2D: (SMESH.FACE, ),
                     MeshElemType.E3D: (SMESH.VOLUME,),
                     MeshElemType.EAll: (SMESH.ALL,),}
        return type_dict[elem_type]
    except (ImportError, AttributeError):
        return ()

class MeshView(MeshBaseView):
    """
    Central view to display mesh and groups.

    Attributes:
         _filename2entry (dict): indicates entry in SMESH for a mesh
             refered by its `meshfile` and `meshname`
             as a two-level dictionary {meshfile: {meshname: entry}}
         _displayed_entry (dict): memorizes SMESH entities currently
             on display to avoid unnecessary redisplay and save time
         ------
         _displayed_mesh (tuple): useful for redisplay function (when
            central view is reactivated, it restores the state of
            the central view when it was last deactivated)
         _displayed_groups (dict): useful for redisplay function
         _displayed_normals (dict): useful for redisplay function
         ------
         _entry2aspect(dict): has {entry: (opacity, rgb)} pairs.
            Allows to change only the aspect without displaying again.
         _entry2defaspect (dict): memorizes the default aspect for later
            restoring.

    Note:
        The `_displayed_mesh` attribute also serves to track the current
        mesh on display, to avoid unnecessary redisplay.
    """

    VIEW_TITLE = "VTK Viewer for Asterstudy"

    def __init__(self, astergui, parent=None):
        """
        Create panel.

        Arguments:
            astergui (AsterGui): AsterGui instance.
            parent (Optional[QWidget]): Parent widget. Defaults to None.

        Note:
            The VTK detached view is not created here but later, on purpose.
            For now, the place where a detached view is put shall
            not be visible at the time when it is created.
            Therefore, the detached view is only created once the
            creation of Asterstudy's desktop is complete.
        """
        MeshBaseView.__init__(self, astergui, parent)

        # attached VTK viewer
        self._vtk_viewer = None

        # define dictionnary to collect displayed object
        self._displayed_entry = dict()
        self._filename2entry = dict()

        # Useful for the redisplay function
        self._displayed_mesh = (None, None, 1.0)
        self._displayed_groups = dict()
        self._displayed_normals = dict()

        # supported features
        self._features.append('switchable')
        if hasattr(get_smesh_gui(), 'setOrientationShown'):
            self._features.append('normals')
        if hasattr(get_salome_gui(), 'FitIObjects'):
            self._features.append('fit_objects')

        # define current view parameters to avoid unnecessary update
        self._entry2aspect = dict()
        self._entry2defaspect = dict()

        # flag to avoid onSelectionUpdated to be called
        # when setSelection is called
        self._enable_selection = False

        self.selection = None

    @property
    def enable_selection(self):
        """Getter to enable the selection interaction straight from view"""
        return self._enable_selection

    @enable_selection.setter
    def enable_selection(self, value):
        """Accessor to enable the selection interaction straight from view"""
        self._enable_selection = value

    def activate(self):
        """
        Redefined from *MeshBaseView*.

        Create or activate VTK detached view.

        Note:
            The creation of the VTK detached view is not in the initializer.
            The detached view has to be created only once the
            creation of Asterstudy's desktop is complete.
        """
        sgPyQt = get_salome_pyqt()

        self.selection = sgPyQt.getSelection()
        self.selection.ClearIObjects()
        connect(self.selection.currentSelectionChanged, self._selectionChanged)

        if self._vtk_viewer is None:
            self._vtk_viewer = sgPyQt.createView('VTKViewer', True, 0, 0, True)
            sgPyQt.setViewTitle(self._vtk_viewer, MeshView.VIEW_TITLE)

        # put widget within the layout
        view = sgPyQt.getViewWidget(self._vtk_viewer)
        self._viewer.layout().addWidget(view)
        view.setVisible(behavior().show_mesh_view)
        # activate 'keyboard-free' navigation style
        view.findChildren(Q.QToolBar)[0].actions()[1].setChecked(True)

    def deactivate(self):
        """Redefined from *MeshBaseView*."""
        if self.selection:
            disconnect(self.selection.currentSelectionChanged,
                       self._selectionChanged)

    def setViewVisible(self, is_on):
        """
        Change mesh view visibility.

        Arguments:
            is_on (bool): Visibility state.
        """
        sgPyQt = get_salome_pyqt()

        behavior().show_mesh_view = is_on

        if self._vtk_viewer is not None:
            view = sgPyQt.getViewWidget(self._vtk_viewer)
            if view is not None:
                view.setVisible(is_on)

        self._redisplay()
        self._selectionChanged()

    @staticmethod
    def smesh_types(group_type):
        """
        Get element types for given `group_type`.

        Arguments:
            group_type (int): Group type (*MeshGroupType*).

        Returns:
            list[int]: List of SMESH element types (SMESH type)
        """
        import SMESH
        smesh_types = {
            MeshGroupType.GNode: (SMESH.NODE,),
            MeshGroupType.GElement: (SMESH.EDGE, SMESH.FACE, SMESH.VOLUME,
                                     SMESH.ELEM0D, SMESH.BALL,)
            }
        return smesh_types.get(group_type, [])

    def getMeshSObj(self, meshfile, meshname):
        """
        Get the SObject of a mesh in the Salome study.

        Arguments:
            meshfile (str): MED file to read.
            meshname (Optional[str]): Name of the mesh to read.
                If empty, use the first mesh. Defaults to *None*.

        Returns:
            SObject: entry of the mesh.

        Note:
            The entry may then easily be found with sobj.GetID()
        """
        import salome

        if is_reference(meshfile): # 'meshfile' is entry
            return salome.myStudy.FindObjectID(meshfile)

        # we get the entry of the mesh in SMESH
        entry = None
        if meshfile not in self._filename2entry:
            # issue27744: test objects already in SMESH first
            # Only create new objects in SMESH if not found
            found = find_mesh_by_name(meshfile, meshname)
            if found is None:
                publish_meshes(meshfile)
                sobject = find_mesh_by_name(meshfile, meshname)
            else:
                sobject = found

            # Register the object to the view
            if sobject is not None:
                entry = sobject.GetID()
                self._filename2entry[meshfile] = {meshname: entry}
        elif meshname not in self._filename2entry[meshfile]:
            sobject = find_mesh_by_name(meshfile, meshname)
            if sobject is not None:
                entry = sobject.GetID()
                self._filename2entry[meshfile][meshname] = entry
        else:
            entry = self._filename2entry[meshfile][meshname]
            sobject = salome.IDToSObject(entry)
        return sobject

    def alreadyOnDisplay(self, meshfile, meshname, group=None, grtype=None):
        """Redefined from *MeshBaseView*."""
        if group is None:
            return (meshfile, meshname) == self._displayed_mesh[:2]
        return self._displayed_groups.get(grtype).get(group, False)

    def _resetView(self):
        """Consistently erase all elements on the view"""
        self._displayed_entry.clear()
        self._displayed_groups.clear()
        self._displayed_normals.clear()
        self._displayed_mesh = (None, None, 1.0)
        self.resetAspects()
        self._entry2aspect.clear()
        get_salome_gui().EraseAll()

    @Q.pyqtSlot(str, str, float, bool)
    @change_cursor
    def displayMEDFileName(self, meshfile, meshname=None,
                           opacity=1.0, erase=False):
        """Redefined from *MeshBaseView*."""
        debug_message("entering displayMEDFileName...")
        if not meshfile:
            return

        if not behavior().show_mesh_view:
            self._displayed_mesh = (meshfile, meshname, opacity)
            if erase:
                self._displayed_groups.clear()
                self._displayed_normals.clear()
                self._entry2aspect.clear()
            return

        sobj = self.getMeshSObj(meshfile, meshname)
        entry = sobj.GetID()

        # get a script to set the camera parameters
        camera_script = get_salome_gui().getViewParameters()

        # activate Asterstudy's VTK view with help of the SalomePyQt utility of
        # SALOME's GUI module
        get_salome_pyqt().activateViewManagerAndView(self._vtk_viewer)

        # if the mesh is already on display and the view need not be reset
        is_mesh_displayed = self.alreadyOnDisplay(meshfile, meshname)
        nothing_displayed = self._displayed_mesh[0] is None
        if is_mesh_displayed and not erase:
            # if opacity setting differs from the previous one
            if self._entry2aspect.get(entry, (None, None))[0] != opacity:
                self.setAspect(sobj, opacity)
                self._displayed_mesh = (meshfile, meshname, opacity)
                get_salome_gui().UpdateView()
            debug_message("displayMEDFileName return #1")
            return

        # display the entry in the active view with help of the `sg` python
        # module of `salome` python package
        self._resetView()
        get_salome_gui().Display(entry)

        if nothing_displayed:
            get_salome_gui().FitAll()
        elif camera_script and not is_mesh_displayed:
            sg = get_salome_gui()
            for meth, args in decode_view_parameters(camera_script):
                getattr(sg, meth)(*args)

        self._displayed_mesh = (meshfile, meshname, opacity)
        self._displayed_entry[entry] = 1
        self.setAspect(sobj, opacity)
        get_salome_gui().UpdateView()
        debug_message("displayMEDFileName return final")

    @Q.pyqtSlot(str, str, str, int,list)
    @change_cursor
    def displayMeshGroupcolor(self, meshfile, meshname, group, grtype,
                         rgb=None, force=False):
        """Redefined by dzj 2020/1/3"""
        if not meshfile:
            return False

        if grtype not in self._displayed_groups:
            self._displayed_groups[grtype] = dict()
        if self._displayed_groups[grtype].get(group, False) and not force:
            return False
        self._displayed_groups[grtype][group] = True
        if not behavior().show_mesh_view:
            return False

        import SMESH

        sm_gui = get_smesh_gui()

        # import MED file and register meshes if needed
        self.getMeshSObj(meshfile, meshname)

        sobject = self.find_group_by_name(meshfile, meshname, group, grtype)
        if sobject is None:
            return False

        entry = sobject.GetID()

        # activate Asterstudy's VTK view with help of the SalomePyQt utility of
        # SALOME's GUI module
        get_salome_pyqt().activateViewManagerAndView(self._vtk_viewer)

        # go for display
        get_salome_gui().Display(entry)
        self._displayed_entry[entry] = 1

        if behavior().grp_global_cmd:
            if self.isFeatureSupported('normals'):
                tag = sobject.GetFather().Tag()
                if tag in (SMESH.Tag_FaceGroups, SMESH.Tag_VolumeGroups):
                    # pragma pylint: disable=no-member
                    sm_gui.setOrientationShown(entry,
                                               self.allNormalsShown(),
                                               self._vtk_viewer)

        self.setAspect(sobject, 1.0, rgb)
        get_salome_gui().UpdateView()
        return True
        

    @Q.pyqtSlot(str, str, str, int)
    @change_cursor
    def displayMeshGroup(self, meshfile, meshname, group, grtype,
                         rgb=None, force=False):
        """Redefined from *MeshBaseView*."""
        if not meshfile:
            return False

        if grtype not in self._displayed_groups:
            self._displayed_groups[grtype] = dict()
        if self._displayed_groups[grtype].get(group, False) and not force:
            return False
        self._displayed_groups[grtype][group] = True
        if not behavior().show_mesh_view:
            return False

        import SMESH

        sm_gui = get_smesh_gui()

        # import MED file and register meshes if needed
        self.getMeshSObj(meshfile, meshname)

        sobject = self.find_group_by_name(meshfile, meshname, group, grtype)
        if sobject is None:
            return False

        entry = sobject.GetID()

        # activate Asterstudy's VTK view with help of the SalomePyQt utility of
        # SALOME's GUI module
        get_salome_pyqt().activateViewManagerAndView(self._vtk_viewer)

        # go for display
        get_salome_gui().Display(entry)
        self._displayed_entry[entry] = 1

        if behavior().grp_global_cmd:
            if self.isFeatureSupported('normals'):
                tag = sobject.GetFather().Tag()
                if tag in (SMESH.Tag_FaceGroups, SMESH.Tag_VolumeGroups):
                    # pragma pylint: disable=no-member
                    sm_gui.setOrientationShown(entry,
                                               self.allNormalsShown(),
                                               self._vtk_viewer)

        self.setAspect(sobject, 1.0, rgb)
        get_salome_gui().UpdateView()
        return True

    @Q.pyqtSlot(str, str, str, int)
    def undisplayMeshGroup(self, meshfile, meshname, group, grtype, force=False):
        """Redefined from *MeshBaseView*."""
        if not meshfile:
            return False

        if grtype not in self._displayed_groups:
            self._displayed_groups[grtype] = dict()
        if not self._displayed_groups[grtype].get(group, False) and not force:
            return False
        self._displayed_groups[grtype][group] = False
        if not behavior().show_mesh_view:
            return False

        sobject = self.find_group_by_name(meshfile, meshname, group, grtype)
        if sobject is None:
            return False

        entry = sobject.GetID()

        if self._displayed_entry.get(entry):
            # activate Asterstudy's VTK view with help of the SalomePyQt
            # utility of SALOME's GUI module
            get_salome_pyqt().activateViewManagerAndView(self._vtk_viewer)

            # go for display
            get_salome_gui().Erase(entry)
            self._displayed_entry[entry] = 0

            get_salome_gui().UpdateView()
            return True

        return False

    def setAspect(self, sobj, opacity=None, rgb=None):
        """
        Set aspect of an object.

        Arguments:
            sobj (SObject): SALOMEDS object
            opacity (float): in (0, 1), 0 is transparent and 1 opaque
            rgb (float[3]): ranging from (0, 1), RGB definition of the color
        """
        import SMESH

        # Let us retrieve an instance of libSMESH_Swig.SMESH_Swig
        sm_gui = get_smesh_gui()
        if not hasattr(sm_gui, 'GetActorAspect'):
            # Customizing aspect requires a newer GUI module.
            return

        entry = sobj.GetID()

        # pragma pylint: disable=no-member
        # retrieve a structure with presentation parameters for this actor
        pres = sm_gui.GetActorAspect(entry, self._vtk_viewer)

        # The color can be changed with:
        # >>> pres.surfaceColor.r = 0.
        # >>> pres.surfaceColor.g = 1.
        # >>> pres.surfaceColor.b = 0.
        #
        # Note: the above code has to be adapted according to dimension
        # volumeColor  : 3D
        # surfaceColor : 2D
        # edgeColor    : 1D
        # nodeColor    : 0D
        #
        obj = sobj.GetObject()
        thetype = obj.GetType() \
            if isinstance(obj, SMESH._objref_SMESH_GroupBase) else None # pragma pylint: disable=protected-access
        type2handle = {SMESH.NODE  : pres.nodeColor,
                       SMESH.ELEM0D: pres.nodeColor,
                       SMESH.EDGE  : pres.edgeColor,
                       SMESH.FACE  : pres.surfaceColor,
                       SMESH.VOLUME: pres.volumeColor}
        handle = type2handle.get(thetype, None)

        # memorize default values
        if entry not in self._entry2defaspect:
            def_opacity = pres.opacity
            def_rgb = (handle.r, handle.g, handle.b) if handle else None
            self._entry2defaspect[entry] = (def_opacity, def_rgb)

        # set new values
        if rgb:
            handle.r, handle.g, handle.b = rgb
            # For faces, avoids a different color of one side from the other
            handle.delta = 0

        if opacity:
            pres.opacity = opacity

        # reinject this for the actor
        sm_gui.SetActorAspect(pres, entry, self._vtk_viewer)
        final_rgb = (handle.r, handle.g, handle.b) if handle else None
        self._entry2aspect[entry] = (pres.opacity, final_rgb)

    def resetAspects(self):
        """Reset older aspect of the objects"""
        import salome
        for entry in self._entry2aspect.keys():
            oldaspect = self._entry2defaspect.get(entry, (None, None))
            self.setAspect(salome.IDToSObject(entry),
                           oldaspect[0],
                           oldaspect[1])

    #zijian dai 2019/12/20 Boundingbox6个值
    # TODO: 分group的Boundingbox 
    def getBounding6(self,meshfile, meshname):
        sobject = find_mesh_by_name(meshfile, meshname)
        import salome
        from salome.smesh import smeshBuilder
        smesh = smeshBuilder.New()
        if sobject is not None:
            obj = sobject.GetObject()
            wobj = smesh.Mesh(obj, sobject.GetName())
            return wobj.BoundingBox()

    #zijian dai 2019/12/23
    #(file_name,nom_med,des,stldic[stlnames[i]],stlnames[i])
    def exportstl(self,meshfile, meshname,des,glist,gname):
        import SMESH
        sobject = find_mesh_by_name(meshfile, meshname)
        import salome
        from salome.smesh import smeshBuilder
        smesh = smeshBuilder.New()
        if sobject is not None:
            obj = sobject.GetObject()
            wobj = smesh.Mesh(obj, sobject.GetName())
            groups = []
            #groups = wobj.GetGroupByName(glist)
            for item in glist:
                groups += wobj.GetGroupByName(item,elemType = SMESH.FACE)
            print(groups)
            print(wobj.GetGroupNames())
            #groups = wobj.GetGroups()
            #newgroup = wobj.GetMesh().UnionListOfGroups(groups, gname)
            #Compound_Mesh = wobj.UnionListOfGroups(groups, gname)
            
            Compound_Mesh_1 = smesh.Concatenate(groups, 1, 1, 1e-05, False )
            Compound_Mesh_1.ExportSTL(des,1)

    def find_group_by_name(self, meshfile, meshname, groupname,
                           grtype=MeshGroupType.GElement):
        """
        Search mesh group.

        Arguments:
            meshfile (str): Mesh file name.
            meshname (str): Name of the mesh.
            groupname (str): Name of the group.
            grtype (int): Type of the group (nodes or elements).

        Returns:
            SObject: SALOME study object (*None* if group is not found).
        """
        # pragma pylint: disable=import-error,no-name-in-module
        import salome
        from salome.smesh import smeshBuilder
        smesh = smeshBuilder.New()
        sobject = find_mesh_by_name(meshfile, meshname)
        group_sobj = None
        if sobject is not None:
            obj = sobject.GetObject()
            for smeshtype in self.smesh_types(grtype):
                try:
                    wobj = smesh.Mesh(obj, sobject.GetName())
                    group_obj = wobj.GetGroupByName(groupname,
                                                    smeshtype)[0]
                    group_sobj = salome.ObjectToSObject(group_obj)
                    break
                except IndexError:
                    continue
        return group_sobj

    def displayAllGroups(self,
                         meshfile,
                         meshname,
                         grtype=MeshGroupType.GElement,
                         elemtype=MeshElemType.EAll,
                         grlist=None):
        """
        Display all groups (nodes or elements) of a given mesh.
        """
        sobj = self.getMeshSObj(meshfile, meshname)
        self._resetView()
        if grlist is not None:
            self.displayMEDFileName(meshfile, meshname, 0.1)
        self._displayAllGroups(sobj, grtype, elemtype, grlist)

    def _displayAllGroups(self, sobj, grtype, elemtype, grlist):
        """
        Display all groups (nodes or elements) of a given mesh.

        Arguments:
            sobj (SObject): SALOMEDS object containing the mesh.
            grtype (int): group ot nodes or elements.
            elemtype (int): dimension of the entities in the group.
        """
        #
        try:
            import salome
            import SMESH
            for tag in range(SMESH.Tag_FirstGroup, SMESH.Tag_LastGroup+1):
                ok, container = sobj.FindSubObject(tag)
                if not ok or container is None:
                    continue
                # iterate through all group of particular type
                iterator = salome.myStudy.NewChildIterator(container)
                while iterator.More():
                    child = iterator.Value()
                    obj = child.GetObject()
                    if obj and obj.GetType() in self.smesh_types(grtype):
                        smeshtypes = elem2smesh(elemtype)
                        if any((SMESH.ALL in smeshtypes,
                                obj.GetType() in smeshtypes)):
                            if grlist is None \
                            or child.GetName() in grlist:
                                # A rough display to adjust later
                                entr = child.GetID()
                                get_salome_gui().Display(entr)
                                self._displayed_entry[entr] = 1
                    iterator.Next()
        except (ImportError, AttributeError):
            pass

    def setSelection(self,
                     meshfile,
                     meshname,
                     grlist,
                     grtype,
                     elemtype=MeshElemType.EAll):
        """Initialize central view selection with list of groups"""
        import SMESH
        with selection_feedback(self, False):
            entry_list = []
            for group in grlist:
                sobj = self.find_group_by_name(meshfile,
                                               meshname,
                                               group,
                                               grtype)
                smeshtypes = elem2smesh(elemtype)
                if any((SMESH.ALL in smeshtypes,
                        sobj.GetObject().GetType() in smeshtypes)):
                    entry_list.append(sobj.GetID())
            get_salome_pyqt().setSelection(entry_list)

    def normalsShown(self, meshfile, meshname, group):
        """Redefined from *MeshBaseView*."""
        import SMESH

        sm_gui = get_smesh_gui()
        if not self.isFeatureSupported('normals'):
            return None

        if not behavior().show_mesh_view:
            return self._displayed_normals.get(group)

        sobject = self.find_group_by_name(meshfile, meshname, group)
        if sobject is None:
            return None

        entry = sobject.GetID()
        tag = sobject.GetFather().Tag()

        if tag not in (SMESH.Tag_FaceGroups, SMESH.Tag_VolumeGroups):
            return None

        if self._displayed_entry.get(entry):
            # pragma pylint: disable=no-member
            return sm_gui.isOrientationShown(entry, self._vtk_viewer)

        return None

    def showNormals(self, meshfile, meshname, group, visible):
        """Redefined from *MeshBaseView*."""
        self._displayed_normals[group] = visible
        if not behavior().show_mesh_view:
            return

        sm_gui = get_smesh_gui()
        if not self.isFeatureSupported('normals'):
            return

        if behavior().grp_global_cmd:
            return

        sobject = self.find_group_by_name(meshfile, meshname, group)
        if sobject is None:
            return

        entry = sobject.GetID()
        if self._displayed_entry.get(entry):
            # pragma pylint: disable=no-member
            sm_gui.setOrientationShown(entry, visible, self._vtk_viewer)

    def setSelected(self, selection):
        """Redefined from *MeshBaseView*."""
        blocked = self.blockSignals(True)
        entries = []
        self.selection.ClearIObjects()
        import salome
        for item in selection:
            sobject = self.find_group_by_name(*item)
            if sobject is None:
                return
            entries.append(sobject.GetID())
            salome.sg.AddIObject(sobject.GetID())
        self.blockSignals(blocked)

    def getSelected(self):
        """Redefined from *MeshBaseView*."""
        # pragma pylint: disable=protected-access
        selection = []
        import salome
        import SMESH
        for i in range(get_salome_gui().SelectedCount()):
            entry = get_salome_gui().getSelected(i)
            sobject = salome.myStudy.FindObjectID(entry)
            if sobject is None or not sobject.GetAllAttributes():
                continue
            group = sobject.GetObject()
            if group and isinstance(group, SMESH._objref_SMESH_GroupBase): # pragma pylint: disable=protected-access
                selection.append(sobject.GetName().rstrip())
        return selection

    def fitObjects(self, meshfile, meshname, groups, grtype):
        """Redefined from *MeshBaseView*."""
        if not behavior().show_mesh_view:
            return False

        if hasattr(get_salome_gui(), 'FitIObjects'):
            self.getMeshSObj(meshfile, meshname)

            entries = []
            for group in groups:
                sobject = self.find_group_by_name(meshfile, meshname,
                                                  group, grtype)
                if sobject is None:
                    continue
                entries.append(sobject.GetID())

            if entries:
                get_salome_gui().FitIObjects(entries) # pragma pylint: disable=no-member
                return True
        return False

    def _updateNormalsVisibility(self):
        """Redefined from *MeshBaseView*."""
        sm_gui = get_smesh_gui()
        if not self.isFeatureSupported('normals'):
            return

        if behavior().grp_global_cmd:
            import salome
            import SMESH
            for dentry in self._displayed_entry:
                sobject = salome.myStudy.FindObjectID(dentry)
                if sobject is None:
                    continue
                tag = sobject.GetFather().Tag()
                if tag not in (SMESH.Tag_FaceGroups, SMESH.Tag_VolumeGroups):
                    continue
                # pragma pylint: disable=no-member
                sm_gui.setOrientationShown(dentry, self.allNormalsShown(),
                                           self._vtk_viewer)

    def _redisplay(self):
        """Redisplay all mesh data."""
        all_groups = dict.copy(self._displayed_groups)
        normals = dict.copy(self._displayed_normals)
        meshfile, meshname, opacity = self._displayed_mesh

        self._displayed_mesh = (None, None, 1.0)

        if meshfile is None or meshname is None:
            return

        self.displayMEDFileName(meshfile, meshname, opacity)
        for grtype, groups in all_groups.items():
            for group, visible in groups.items():
                if visible:
                    self.displayMeshGroup(meshfile, meshname, group, grtype,
                                          force=True)
                else:
                    self.undisplayMeshGroup(meshfile, meshname, group, grtype,
                                            force=True)
        for group, visible in normals.items():
            self.showNormals(meshfile, meshname, group, visible)
        self._updateNormalsVisibility()

    def _selectionChanged(self):
        if behavior().show_mesh_view:
            self.selectionChanged.emit()
