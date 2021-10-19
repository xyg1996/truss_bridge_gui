

"""
Overlay bar
------------

A generic overlay bar, to be used in the results tab of the
AsterStudy application.

"""

from PyQt5 import Qt as Q


class OverlayBar(Q.QWidget):
    """
    Implementation of the OverlayBar
    """

    def __init__(self, parent, pos=(0, 0), height=50, relwidth=1.0,
                 color=(25, 35, 45), opacity=1.0,
                 botline=None):
        """
        Create a new overlay zone above parent
        """
        super(OverlayBar, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(Q.Qt.FramelessWindowHint)

        self._relwidth = relwidth
        self._height = height
        self._pos = pos
        self._botline = (botline if isinstance(botline, (tuple, list))
                         else False)

        op_value = (int(opacity * 255) if (0.0 <= opacity <= 1.0)
                    else 255)
        self.fill = Q.QColor(color[0], color[1], color[2], op_value)
        self.pen = Q.QColor(color[0], color[1], color[2], 0)

        self.repaint()
        self.move(pos[0], pos[1])

    def get_size(self):
        """Returns updated size"""
        _size = self.parent().size()
        return (int(self._relwidth * _size.width() - self._pos[0]),
                self._height)

    def get_pos(self):
        """return the current position on the screen"""
        return self._pos

    def repaint(self):
        """Upon widget repaint"""
        _size = self.get_size()
        self.resize(*_size)

        pos = self.get_pos()

        painter = Q.QPainter(self)
        painter.setRenderHint(Q.QPainter.Antialiasing, True)
        painter.setBrush(self.fill)
        painter.setPen(self.pen)
        painter.drawRect(0, 0, _size[0], _size[1])

        if self._botline:
            cred, cgreen, cblue, lthick = self._botline
            pen = Q.QPen(Q.QColor(cred, cgreen, cblue, 255))
            pen.setWidth(lthick)
            painter.setPen(pen)
            level = pos[1] + self._height - lthick
            painter.drawLine(pos[0], level, pos[0] + _size[0], level)

    # pragma pylint: disable=invalid-name
    def resizeEvent(self, _):
        """Resize the widget."""
        self.repaint()

    # pragma pylint: disable=invalid-name
    def paintEvent(self, _):
        """Draws the content of the bar overlay"""
        self.repaint()
