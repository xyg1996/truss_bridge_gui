

"""
Directory widget
----------------

The module implements a widget managing code_aster catalogs
in SALOME Preferences dialog.

For more details refer to *DirWidget* class.

"""


import PyQt5.Qt as Q
import SalomePyQt

from . catalogsview import CatalogsView

class DirWidget(SalomePyQt.UserDefinedContent):
    """Custom preference item for user's catalogs set-up."""

    widget = None

    def __init__(self):
        """Create widget."""
        super().__init__()
        self.editor = CatalogsView()
        self.setLayout(Q.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.editor)

    def store(self):
        """Store settings."""
        self.editor.store()

    def retrieve(self):
        """Restore settings."""
        self.editor.restore()

    @staticmethod
    def instance():
        """Get singleton widget object."""
        if DirWidget.widget is None:
            DirWidget.widget = DirWidget()
        return DirWidget.widget
