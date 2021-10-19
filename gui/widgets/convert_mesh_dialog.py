


#


"""
Convert Mesh Widget
-------------------

Implementation of the widget used for mesh conversion.
"""


import os
import os.path as osp
import traceback
from collections import OrderedDict

from PyQt5 import Qt as Q

from ...common import get_extension, translate, wait_cursor
from ...datamodel.usages import EXTENSIONS, convert_mesh
from ..salomegui_utils import publish_meshes

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class ConvertMeshWindow(Q.QDialog):
    """Widget for mesh file conversion."""

    defaultName = "Mesh"
    idx = 0

    def __init__(self, node, parent=None):
        """The dialog for mesh files conversion.

        Arguments:
            node (*File*): Object hold by the *Data Files* panel.
            parent (QWidget): Parent widget.
        """
        super().__init__(parent)
        self._node = node
        self._path = node.filename
        self._mesh = None
        self.setWindowTitle(translate("AsterStudy", "Mesh converter ({0})")
                            .format(osp.basename(self._path)))

        gform = Q.QGroupBox(translate("AsterStudy", "Input mesh format"))
        types = ("mail", "gmsh", "ideas", "gibi")
        self._radio = OrderedDict([(i, Q.QRadioButton(i, gform))
                                   for i in types])
        lay_fmt = Q.QHBoxLayout(gform)
        for button in self._radio.values():
            lay_fmt.addWidget(button)
            button.toggled.connect(self.updateState)
        gform.setLayout(lay_fmt)

        gname = Q.QGroupBox(translate("AsterStudy", "Ouput mesh name"))
        lay_name = Q.QVBoxLayout(gname)
        self._outname = Q.QLineEdit(gname)
        self._outname.setText(self.defaultName + str(self.idx))
        ConvertMeshWindow.idx += 1
        self._outname.setToolTip(translate("AsterStudy",
                                           "It will be the SMESH object name"))
        self._outname.textChanged.connect(self.updateState)
        lay_name.addWidget(self._outname)
        gname.setLayout(lay_name)

        useit = Q.QWidget(self)
        lay_use = Q.QHBoxLayout(useit)
        self._cbox = Q.QCheckBox(useit)
        self._cbox.setChecked(True)
        lbl = Q.QLabel(translate("AsterStudy", "Replace input file usage by "
                                 "the new Mesh object in commands."))
        lay_use.addWidget(self._cbox)
        lay_use.addWidget(lbl)

        self._status = Q.QLabel()
        self._status.setAlignment(Q.Qt.AlignHCenter)
        self._status.setEnabled(False)

        bbox = Q.QDialogButtonBox(Q.Qt.Horizontal, self)
        self._go = Q.QPushButton(translate("AsterStudy", "Convert"))
        bbox.addButton(self._go, Q.QDialogButtonBox.AcceptRole)
        bbox.addButton(Q.QDialogButtonBox.Cancel)
        self._go.setDefault(True)
        cancel_button = bbox.button(Q.QDialogButtonBox.Cancel)

        frame = Q.QWidget(self)
        content = Q.QVBoxLayout(frame)
        content.addWidget(gform)
        content.addWidget(gname)
        content.addWidget(useit)
        content.addWidget(self._status)

        toplevel = Q.QVBoxLayout(self)
        toplevel.addWidget(frame)
        toplevel.addWidget(bbox)

        self._go.clicked.connect(self.execute)
        cancel_button.clicked.connect(self.reject)
        self._setInputFormat()
        self.updateState()

    @property
    def _format(self):
        """Return the selected format."""
        for fmt, button in self._radio.items():
            if button.isChecked():
                return fmt
        return ""

    @property
    def _name(self):
        """Return the output mesh name."""
        return self._outname.text()

    def _setInputFormat(self):
        """Select the format according to the file path."""
        fmt = EXTENSIONS.get(get_extension(self._path), "")
        if self._radio.get(fmt):
            self._radio[fmt].setChecked(True)

    @Q.pyqtSlot()
    def updateState(self):
        """Update the widget."""
        self.setText("")
        format_ok = bool(self._format)
        if not format_ok:
            self.setText(translate("AsterStudy",
                                   "Please select the input file format."))

        self._outname.setText(self._name.strip())
        name_ok = _valid_name(self._name)
        if not name_ok:
            self.setText(translate("AsterStudy",
                                   "Invalid mesh object name."))

        self._go.setEnabled(format_ok and name_ok)

    def setText(self, message):
        """Fill the status message."""
        self._status.setText(message)

    def setEnabled(self, value):
        """Enable/disable input widgets."""
        for button in self._radio.values():
            button.setEnabled(value)
        self._outname.setEnabled(value)
        self._cbox.setEnabled(value)

    def starting(self, message):
        """Starting background command."""
        self.setText(message)
        wait_cursor(True)
        self.setEnabled(False)
        self._go.setEnabled(False)

    def finalize(self, is_ok):
        """Finalize the execution with given status."""
        self.setEnabled(True)
        # Expect a change before allow restart if not ok
        self._go.setEnabled(is_ok)
        wait_cursor(False)

    @Q.pyqtSlot()
    def execute(self):
        """*Accept* the dialog."""
        self.starting(translate("AsterStudy",
                                "Converting mesh file. Please wait..."))
        Q.QTimer.singleShot(50, self._execute)

    def _execute(self):
        """Execute the conversion."""
        exc = None
        try:
            medfile = convert_mesh(self._path, self._format, self._name)
            self._mesh = publish_meshes(medfile)
            os.remove(medfile)
        except Exception as exc: # pylint: disable=broad-except
            traceback.print_exc()
        finally:
            self.updateState()

        is_ok = not bool(exc)
        self.finalize(is_ok)
        if not is_ok:
            self.setText(str(exc))
            return

        self.starting(translate("AsterStudy",
                                "Updating commands using the input file..."))
        Q.QTimer.singleShot(50, self._replace_in_command)

    def _replace_in_command(self):
        """Replace the usage of the input file by the SMESH object."""
        is_ok = len(self._mesh) == 1
        if not is_ok:
            self.setText(translate("AsterStudy", "More than one mesh: "
                                   "commands will not be changed!"))
        else:
            import salome
            mesh = self._mesh[0]
            sobject = salome.ObjectToSObject(mesh.mesh) # pragma pylint: disable=no-member
            uid = sobject.GetID()
            unit = self._node.unit
            info = self._node.stage.handle2info[unit]
            read_mesh = [cmd for cmd in info.commands
                         if cmd.title == "LIRE_MAILLAGE"]
            if read_mesh:
                info.filename = uid
                for cmd in read_mesh:
                    if cmd.title == "LIRE_MAILLAGE":
                        cmd["FORMAT"] = "MED"

        self.finalize(is_ok)
        if not is_ok:
            self.setText(translate("AsterStudy",
                                   "Can not update commands!"))
        else:
            self.accept()


def _valid_name(name):
    """Is it a valid python variable?"""
    try:
        exec(name + " = 0") # pragma pylint: disable=exec-used
    except SyntaxError:
        return False
    return len(name) <= 8
