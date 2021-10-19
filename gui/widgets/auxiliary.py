

"""
Auxiliary widgets
-----------------

The module implements different auxiliary widgets.

"""


from PyQt5 import Qt as Q

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class HLine(Q.QFrame):
    """Helper class to create horizontal line frame widget."""

    def __init__(self, parent=None):
        """
        Create line widget.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        super().__init__(parent)
        self.setFrameStyle(Q.QFrame.HLine | Q.QFrame.Sunken)
