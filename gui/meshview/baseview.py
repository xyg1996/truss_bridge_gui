


#


"""
Mesh base view
--------------

Implementation of dummy mesh view for standalone AsterStudy application.

"""


from PyQt5 import Qt as Q

from ...common import debug_mode
# from .. grouppanel import GroupPanel

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name

# pragma pylint: disable=no-self-use,unused-argument


class MeshBaseView(Q.QSplitter):
    """Base widget to display mesh data."""

    selectionChanged = Q.pyqtSignal()
    """Signal: emitted when selection is changed in a view."""

    infoHidden = Q.pyqtSignal()
    """Signal: emitted when summary panel is hidden."""

    def __init__(self, astergui, parent=None):
        """
        Create view.

        Arguments:
            astergui (AsterGui): AsterGui instance.
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        super().__init__(Q.Qt.Vertical, parent)
        self._astergui = astergui
        self._all_normals_shown = False
        self._features = []

        self.setChildrenCollapsible(False)

        self._viewer = Q.QWidget(self)
        self._viewer.setLayout(Q.QVBoxLayout())
        self._viewer.layout().setContentsMargins(0, 0, 0, 0)
        self._viewer.setSizePolicy(Q.QSizePolicy.Expanding, Q.QSizePolicy.Expanding)
        self.addWidget(self._viewer)
        self.setStretchFactor(0, 1)
        # self._summary = GroupPanel(astergui, self)
        # self._summary.hidden.connect(self.infoHidden)
        # self.addWidget(self._summary)

        if debug_mode():
            self._debugWidget = Q.QTableView(self)
            self._debugWidget.setObjectName('BaseView_DebugWidget')
            self._debugWidget.setModel(Q.QStandardItemModel(self))
            self._debugWidget.model().setColumnCount(3)
            self._viewer.layout().addWidget(self._debugWidget)

    def isFeatureSupported(self, feature):
        """
        Check if given feature is supported by view.
        """
        return feature in self._features

    def sizeHint(self):
        """
        Get size hint for the view.

        Returns:
            QSize: Size hint.
        """
        desktop = Q.QApplication.desktop().availableGeometry(self)
        return Q.QSize(desktop.width(), desktop.height())

    def activate(self):
        """
        Activate mesh view.

        Default implementation does nothing.
        """

    def deactivate(self):
        """
        Deactivate mesh view.

        Default implementation does nothing.
        """

    def alreadyOnDisplay(self, meshfile, meshname, group=None, grtype=None):
        """
        Check if a mesh or group is already displayed.

        Arguments:
            meshfile (str): name of the mesh file (a MED format).
            meshname (str): name of mesh within file.
            group (Optional[str]): Mesh group name.
            grtype (Optional[int]): Type (nodes or elements), see *MeshGroupType*.

        Returns *True* if object is already displayed.
        """
        return False

    @Q.pyqtSlot(str, str, float, bool)
    def displayMEDFileName(self, meshfile, meshname=None,
                           opacity=1.0, erase=False):
        """
        Display the mesh in `meshfile` with name `meshname`.

        Default implementation does nothing.

        Arguments:
            meshfile (str): MED file name.
            meshname (Optional[str]): Mesh name. If empty, first mesh
                is used. Defaults to *None*.
            opacity (Optional[float]): Opacity of mesh presentation.
                Defaults to 1.0.
            erase (Optional[bool]): Erase all presentation in a view
                before displaying mesh presentation.
                Defaults to *False*.
        """

    @Q.pyqtSlot(str, str, str, int)
    def displayMeshGroup(self, meshfile, meshname, group, grtype,
                         rgb=None, force=False):
        """
        Display mesh group.

        Default implementation does nothing.

        Arguments:
            meshfile (str): MED file name.
            meshname (str): Mesh name.
            group (str): Mesh group name.
            grtype (int): Type (nodes or elements), see *MeshGroupType*.
            rgb (float[3]): RGB definition of the color in (0,1)
            force (Optional[bool]): Force group redisplay even if it is
                already displayed. Defaults to *False*.
        """
        if debug_mode():
            model = self._debugWidget.model()
            item = self.find_group_by_name(meshfile, meshname, group, grtype)
            if not item:
                item = Q.QStandardItem('{}/{}'.format(grtype, group))
                item.setData(meshfile, Q.Qt.UserRole + 1)
                item.setData(meshname, Q.Qt.UserRole + 2)
                item.setData(group, Q.Qt.UserRole + 3)
                item.setData(grtype, Q.Qt.UserRole + 4)
                model.appendRow(item)
                model.sort(0)
            model.setData(model.index(item.row(), 1), 'Visible')
            if rgb:
                color = Q.QColor.fromRgbF(rgb[0], rgb[1], rgb[2])
                model.setData(model.index(item.row(), 2), color)
                model.setData(model.index(item.row(), 2), color, Q.Qt.ForegroundRole)
            else:
                model.setData(model.index(item.row(), 2), None)
                model.setData(model.index(item.row(), 2), None, Q.Qt.ForegroundRole)
            return True

        return False

    @Q.pyqtSlot(str, str, str, int)
    def undisplayMeshGroup(self, meshfile, meshname, group, grtype,
                           force=False):
        """
        Erase mesh group.

        Default implementation does nothing.

        Arguments:
            meshfile (str): MED file name.
            meshname (str): Mesh name.
            group (str): Mesh group name.
            grtype (int): Type (nodes or elements), see *MeshGroupType*.
            force (Optional[bool]): Force group erasing even if it is
                has been previously scheduled for erasing. Defaults to *False*.
        """
        if debug_mode():
            model = self._debugWidget.model()
            item = self.find_group_by_name(meshfile, meshname, group, grtype)
            if item:
                model.setData(model.index(item.row(), 1), 'Hidden')
                model.setData(model.index(item.row(), 2), None)
                return True

        return False

    def find_group_by_name(self, meshfile, meshname, groupname, grtype):
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
        if debug_mode():
            model = self._debugWidget.model()
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.data(Q.Qt.UserRole + 1) == meshfile \
                and item.data(Q.Qt.UserRole + 2) == meshname \
                and item.data(Q.Qt.UserRole + 3) == groupname \
                and item.data(Q.Qt.UserRole + 4) == grtype:
                    return item
        return None

    def normalsShown(self, meshfile, meshname, group):
        """
        Check if face orientation normals are shown for specified
        mesh group.

        Note:
            If normals feature is not supported, the method
            return *None*.

        Default implementation returns *None*.

        Arguments:
            meshfile (str): MED file name.
            meshname (str): Mesh name.
            group (str): Mesh group name.

        Returns:
            bool: *True* if normals are shown; *False* otherwise.
        """
        return None

    def showNormals(self, meshfile, meshname, group, visible):
        """
        Show/hide face orientation normals for given mesh group.

        Note:
            If normals feature is not supported, the method
            does nothing.

        Default implementation does nothing.

        Arguments:
            meshfile (str): MED file name.
            meshname (str): Mesh name.
            group (str): Mesh group name.
            visible (bool): Visibility flag.
        """

    def allNormalsShown(self):
        """Get 'Show all normals flag' option's value."""
        return self._all_normals_shown

    def setAllNormalsShown(self, visible):
        """Set 'Show all normals flag' option's value."""
        if self._all_normals_shown == visible:
            return
        self._all_normals_shown = visible
        self._updateNormalsVisibility()

    def setSelected(self, selection):
        """
        Set selection to view.

        Default implementation does nothing.

        Arguments:
            selection (list): Items to select (mesh groups).
        """

    def getSelected(self):
        """
        Get selection from view.

        Default implementation returns empty list.

        Returns:
            list: Selected items (mesh groups).
        """
        return []

    def fitObjects(self, meshfile, meshname, groups, grtype):
        """Fit view contents to given groups."""
        return False

    def _updateNormalsVisibility(self):
        """
        Update normals visibility.

        Called from `setAllNormalsShown()`.
        Default implementation does nothing.
        """
