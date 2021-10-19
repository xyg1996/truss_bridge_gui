


#


"""
Color selection button
----------------------

The module implements a color selection control.

For more details refer to *ColorButton* class.

"""


from PyQt5 import Qt as Q

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class ColorButton(Q.QToolButton):
    """Color selection button."""

    def __init__(self, parent=None):
        """
        Create button.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        super().__init__(parent)
        self.setCheckable(False)
        self.color = Q.QColor()
        self.clicked.connect(self._selectColor)
        self._update()

    def value(self):
        """
        Get color from the widget.

        Returns:
            QColor: Color value.
        """
        return self.color

    def setValue(self, color):
        """
        Get color to the widget.

        Arguments:
            color (QColor): Color value.
        """
        self.color = color
        self._update()

    def _selectColor(self):
        color = Q.QColorDialog.getColor(self.value(), self)
        if color.isValid():
            self.setValue(color)

    def _update(self):
        palette = self.palette()
        palette.setColor(Q.QPalette.Button, self.value())
        self.setPalette(palette)
