


#


"""

Splitter
--------

Custom splitter that draws handle with the gradient background.
"""


from PyQt5 import Qt as Q

__all__ = ['Splitter']

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class Handle(Q.QSplitterHandle):
    """Handle with gradient background."""

    def setColor(self, color):
        """
        Set handle main color.

        Arguments:
            color (QColor): Title main color.
        """
        palette = self.palette()
        palette.setColor(Q.QPalette.Highlight, color)
        self.setPalette(palette)

    def paintEvent(self, event):
        """Redefined from *QSplitterHandle*."""
        base = self.rect()
        if self.orientation() == Q.Qt.Vertical:
            gradient = Q.QLinearGradient(base.topLeft(), base.topRight())
        else:
            gradient = Q.QLinearGradient(base.topLeft(), base.bottomLeft())
        gradient.setColorAt(0, self.palette().color(Q.QPalette.Highlight))
        gradient.setColorAt(1, self.palette().color(Q.QPalette.Window))
        painter = Q.QPainter(self)
        painter.fillRect(base, gradient)
        super().paintEvent(event)


class Splitter(Q.QSplitter):
    """Spltter that draws handles with gradient background."""

    def createHandle(self):
        """Redefined from *QSplitter*."""
        return Handle(self.orientation(), self)
