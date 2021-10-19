


#


"""
Load database Widget
--------------------

Implementation of the widget used to load a database.
"""

import os.path as osp
import traceback

from PyQt5 import Qt as Q

from ...common import get_directory, translate, wait_cursor
# from ...datamodel.usages import load_database

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class LoadDatabaseWindow(Q.QDialog):
    """Widget for loading a database."""

    def __init__(self, history, parent, init_path):
        super().__init__(parent)
        self.setWindowTitle(translate("AsterStudy", "Restart from a database"))
        self._history = history

        lbl1 = Q.QLabel(translate("AsterStudy", "Database path"))
        self._edit = Q.QLineEdit(self)
        fmtr = self._edit.fontMetrics()
        width = fmtr.boundingRect(" " * 40 * 2).width()
        self._edit.setMinimumWidth(width)
        if osp.isdir(init_path):
            self._edit.setText(init_path)
        self._edit.setEnabled(False)
        self._browse = Q.QToolButton(self)
        self._browse.setText("...")
        self._browse.clicked.connect(self._browseClicked)

        lbl2 = Q.QLabel(translate("AsterStudy", "Extract available objects"))
        self._cbox = Q.QCheckBox()
        self._cbox.setChecked(True)
        ttip = translate("AsterStudy", "code_aster will be executed to "
                         "extract the database content.")
        lbl2.setToolTip(ttip)
        self._cbox.setToolTip(ttip)

        self._status = Q.QLabel()
        self._status.setAlignment(Q.Qt.AlignHCenter)

        frame = Q.QWidget(self)
        grid = Q.QGridLayout(frame)
        grid.addWidget(lbl1, 0, 0)
        grid.addWidget(self._edit, 0, 1)
        grid.addWidget(self._browse, 0, 2)
        grid.addWidget(lbl2, 1, 0)
        grid.addWidget(self._cbox, 1, 1)
        grid.addWidget(self._status, 2, 0, -1, 0)

        bbox = Q.QDialogButtonBox(Q.Qt.Horizontal, self)
        self._go = Q.QPushButton("Load")
        bbox.addButton(self._go, Q.QDialogButtonBox.AcceptRole)
        bbox.addButton(Q.QDialogButtonBox.Cancel)
        self._go.setDefault(True)
        cancel_button = bbox.button(Q.QDialogButtonBox.Cancel)

        toplevel = Q.QVBoxLayout(self)
        toplevel.addWidget(frame)
        toplevel.addWidget(bbox)

        self._go.clicked.connect(self.execute)
        cancel_button.clicked.connect(self.reject)
        self.updateState()

    @property
    def _path(self):
        """Return the selected path."""
        return self._edit.text()

    @Q.pyqtSlot()
    def _browseClicked(self):
        """Select the format according to the file path."""
        path = get_directory(self, self._path, True)
        if path:
            self._edit.setText(path)
            self.updateState()

    @Q.pyqtSlot()
    def updateState(self):
        """Update the widget."""
        self.setText("")
        self._go.setEnabled(bool(self._path))

    def setText(self, message):
        """Fill the status message."""
        self._status.setText(message)

    def setEnabled(self, value):
        """Enable/disable input widgets."""
        wait_cursor(not value)
        self._browse.setEnabled(value)

    @Q.pyqtSlot()
    def execute(self):
        """*Accept* the dialog."""
        self.setEnabled(False)
        self.setText("Loading database content. Please wait...")
        Q.QTimer.singleShot(50, self._execute)

    def _execute(self):
        """Execute the conversion."""
        exc = None

        self.setEnabled(True)
        if exc:
            self.setText(str(exc))
            # Expect a change before allow restart
            self._go.setEnabled(False)
        else:
            self.accept()
