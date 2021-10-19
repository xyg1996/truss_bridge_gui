

"""
Catalogs view
-------------

The module implements user catalogs view.

For more details refer to *CatalogsView* class.

"""


import os

from PyQt5 import Qt as Q

from ...common import CFG, Configuration, load_icon, translate
from .dialog import Dialog

__all__ = ["CatalogsView"]

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class CatalogsView(Q.QWidget):
    """Catalogs view."""

    def __init__(self, parent=None, unittest=False):
        """
        Create widget.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to *None*.
            unittest (bool): Used for unittest (default: *False*).
        """
        super().__init__(parent)
        self._unittest = unittest
        self.items = []

        btn = Q.QPushButton(translate("CatalogsView", "Add catalog"), self)
        btn.setObjectName('cataview_add_btn')

        frame = Q.QScrollArea(self)
        frame.setObjectName('cataview_frame')
        frame.setFrameStyle(Q.QFrame.Panel | Q.QFrame.Sunken)
        frame.setHorizontalScrollBarPolicy(Q.Qt.ScrollBarAlwaysOff)
        frame.setWidgetResizable(True)
        frame.setSizePolicy(Q.QSizePolicy.Minimum, Q.QSizePolicy.Expanding)
        frame.setMinimumHeight(100)
        frame.setWidget(Q.QWidget(frame))
        frame.widget().setObjectName('cataview_wg')
        frame.widget().setLayout(Q.QVBoxLayout())
        frame.widget().layout().setContentsMargins(0, 0, 0, 0)

        self.box = Q.QWidget(frame.widget())
        self.box.setObjectName('cataview_box')
        self.box.setLayout(Q.QGridLayout())
        frame.widget().layout().addWidget(self.box)
        frame.widget().layout().addStretch()

        self.setLayout(Q.QGridLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(btn, 0, 0)
        self.layout().addWidget(frame, 1, 0, 1, 2)
        self.layout().setColumnStretch(1, 5)

        btn.clicked.connect(self._add)

    def _critical(self, parent, title, message):
        """Alternative to *QMessageBox* for unit testing."""
        if not self._unittest:
            Q.QMessageBox.critical(parent, title, message)
        else:
            raise ValueError(message)

    def store(self):
        """Store user's catalogs to the Preferences file."""
        items = self._items()
        cfg = Configuration(True)
        old_versions = cfg.options('Versions') \
            if cfg.has_section('Versions') else []
        new_versions = [i[0] for i in items]
        for label in old_versions:
            if label not in new_versions:
                cfg.remove_option('Versions', label)
                if CFG.has_option('Versions', label):
                    CFG.remove_option('Versions', label)
        for label, path in items:
            if not cfg.has_section('Versions'):
                cfg.add_section('Versions')
            cfg.set('Versions', label, path)
            CFG.set('Versions', label, path)
        with open(cfg.userrc, 'w') as pref:
            cfg.write(pref)

    def restore(self):
        """Restore user's catalogs to the Preferences file."""
        self._clear()

        cfg = Configuration(True)
        versions = cfg.options('Versions') \
            if cfg.has_section('Versions') else []
        for label in versions:
            path = cfg.get('Versions', label)
            self._addItem(label, path)

    def checkLabel(self, label, dlg):
        """
        Validate catalog's label entered by the user.

        Arguments:
            label (str): Catalog's label.
            dlg (QDialog): Calling dialog.

        Returns:
            bool: *True* if label is valid; *False* otherwise.
        """
        for internal in ['stable', 'testing']:
            if label == internal:
                title = translate("CatalogsView", "Error")
                message = translate("CatalogsView",
                                    "Label '{}' is reserved for internal use")
                self._critical(dlg, title, message.format(label))
                return False

        items = self._items()
        item = [i for i in items if i[0] == label]
        if item:
            title = translate("CatalogsView", "Error")
            message = translate("CatalogsView", "Label '{}' is already in use")
            self._critical(dlg, title, message.format(label))
            return False

        return True

    def checkPath(self, path, dlg):
        """
        Validate catalog's path entered by the user.

        Arguments:
            path (str): Catalog's path.
            dlg (QDialog): Calling dialog.

        Returns:
            bool: *True* if path is valid; *False* otherwise.
        """
        full_path = os.path.join(path, 'code_aster')
        if not os.path.exists(full_path):
            title = translate("CatalogsView", "Error")
            message = translate("CatalogsView",
                                "Path does not exist:\n{}\n\n"
                                "You must select a directory that contains "
                                "a 'code_aster' subdirectory.")
            self._critical(dlg, title, message.format(full_path))
            return False

        items = self._items()
        item = [i for i in items if i[1] == path]
        if item:
            title = translate("CatalogsView", "Error")
            message = translate("CatalogsView", "Path '{}' is already in use")
            self._critical(dlg, title, message.format(path))
            return False

        return True

    @Q.pyqtSlot()
    def _add(self):
        """Called when user presses 'Add catalog' button."""
        dlg = SetupCatalog(self)
        dlg.setObjectName('cataview_setup_catalog')
        path = os.path.join(os.getenv('HOME', '/'), 'dev', 'codeaster',
                            'install', 'std', 'lib', 'aster')
        dlg.setData('dev', path)
        if dlg.exec_():
            label, path = dlg.data()
            self._addItem(label, path)

    @Q.pyqtSlot()
    def _delete(self):
        """Called when catalog item is removed."""
        item = self.sender()
        if item in self.items:
            self.items.remove(item)

    def _addItem(self, label, path):
        """Add item with given *label* and *path*."""
        item = Item(label, path, self.box)
        item.deleted.connect(self._delete)
        self.items.append(item)

    def _clear(self):
        """Remove all items."""
        for item in reversed(self.items):
            item.remove()

    def _items(self):
        """Get all catalog items."""
        return [item.data() for item in self.items]


class Item(Q.QObject):
    """Single item in the *Catalogs* view."""

    deleted = Q.pyqtSignal()
    """
    Signal: emitted when item is deleted.
    """

    def __init__(self, label, path, view):
        """Create item."""
        super().__init__()
        self.view = view

        self.label = Q.QLineEdit(view)
        self.label.setObjectName('cataview_item_{}_title'.format(label))
        self.label.setReadOnly(True)
        self.label.setSizePolicy(Q.QSizePolicy.Minimum, Q.QSizePolicy.Fixed)

        self.path = Q.QLineEdit(view)
        self.path.setObjectName('cataview_item_{}_path'.format(label))
        self.path.setReadOnly(True)
        self.path.setMinimumWidth(150)

        self.btn = Q.QPushButton(view)
        self.btn.setObjectName('cataview_item_{}_btn'.format(label))
        self.btn.setIcon(load_icon("as_pic_delete.png"))

        gl = view.layout()
        row = gl.rowCount()
        gl.addWidget(self.label, row, 0)
        gl.addWidget(self.path, row, 1)
        gl.addWidget(self.btn, row, 2)

        self.btn.clicked.connect(self.remove)

        self.label.setText(label)
        self.label.home(False)
        self.label.setToolTip(label)
        self.path.setText(path)
        self.path.home(False)
        self.path.setToolTip(path)

    def data(self):
        """Get item's data: *label*, *path*."""
        return self.label.text(), self.path.text()

    @Q.pyqtSlot()
    def remove(self):
        """Remove item."""
        self.view.layout().removeWidget(self.label)
        self.view.layout().removeWidget(self.path)
        self.view.layout().removeWidget(self.btn)
        self.label.deleteLater()
        self.path.deleteLater()
        self.btn.deleteLater()
        self.deleted.emit()


class SetupCatalog(Dialog):
    """Catalog's definition dialog."""

    def __init__(self, parent=None):
        """
        Create dialog.
        """
        super().__init__(parent)

        title = translate("CatalogsView", "Set-up catalogue")
        self.setWindowTitle(title)

        gl = Q.QGridLayout(self.main())
        gl.setContentsMargins(0, 0, 0, 0)

        title = translate("CatalogsView", "Label")
        gl.addWidget(Q.QLabel(title, self.main()), 0, 0)

        self.label = Q.QLineEdit(self.main())
        self.label.setObjectName('cataview_setup_catalog_title')
        gl.addWidget(self.label, 0, 1)

        title = translate("CatalogsView", "Location")
        gl.addWidget(Q.QLabel(title, self.main()), 1, 0)

        self.path = Q.QLineEdit(self.main())
        self.path.setObjectName('cataview_setup_catalog_path')
        self.path.setMinimumWidth(200)
        self.path.setCompleter(Q.QCompleter())
        model = Q.QDirModel()
        model.setFilter(Q.QDir.Drives | Q.QDir.Dirs | Q.QDir.NoDotAndDotDot)
        self.path.completer().setModel(model)
        gl.addWidget(self.path, 1, 1, 1, 2)

        title = translate("AsterStudy", "Browse...")
        btn = Q.QPushButton(title, self.main())
        btn.setObjectName('cataview_setup_catalog_browse_btn')
        gl.addWidget(btn, 1, 3)

        gl.setColumnStretch(2, 5)

        btn.clicked.connect(self._browse)

        self.label.setFocus()

    def data(self):
        """Get catalog's data: *label* and *path*."""
        label = self.label.text().strip().lower()
        path = os.path.abspath(os.path.normpath(self.path.text().strip()))
        return label, path

    def setData(self, label, path):
        """Set catalog's data: *label* and *path*."""
        self.label.setText(label)
        self.label.home(False)
        self.path.setText(path)
        self.path.home(False)

    def accept(self):
        """Called when user presses 'OK' button."""
        label, path = self.data()
        if not self.parent().checkLabel(label, self):
            return
        if not self.parent().checkPath(path, self):
            return
        super().accept()

    @Q.pyqtSlot()
    def _browse(self):
        """Open dialog to browse directory."""
        path = self.path.text().strip()
        title = translate("CatalogsView", "Select directory")
        path = Q.QFileDialog.getExistingDirectory(self, title, path)
        if path:
            self.path.setText(path)
            self.path.home(False)
