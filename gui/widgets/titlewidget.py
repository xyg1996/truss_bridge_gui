


#


"""

Title widget
------------

The module implements a widget that draws a gradient as a background;
it can be used to implement title label.
"""


from PyQt5 import Qt as Q

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name

from .. import behavior


class TitleWidget(Q.QWidget):
    """Title widget."""

    MAIN_COLOR = Q.QColor('#414F80')
    HIGHLIGHT_COLOR = Q.QColor("#008080")

    Left = 0
    Right = 1

    def __init__(self, text='', parent=None):
        """
        Create widget.

        Arguments:
            text (str): Title text.
            parent (QWidget): Parent widget.
        """
        super().__init__(parent)
        self.setLayout(Q.QHBoxLayout())
        self.layout().setContentsMargins(5, 0, 5, 0)

        self._label = Q.QLabel(self)
        self._label.setObjectName('label')
        self._label.setForegroundRole(Q.QPalette.Base)
        self._label.setSizePolicy(Q.QSizePolicy.Expanding, Q.QSizePolicy.Fixed)
        self._label.setText(text)
        self.layout().addWidget(self._label)

        self._toolbar = Q.QToolBar(self)
        self._toolbar.setObjectName('toolbar')
        bsize = behavior().title_button_size
        self._toolbar.setIconSize(Q.QSize(bsize, bsize))
        self._toolbar.setToolButtonStyle(Q.Qt.ToolButtonIconOnly)
        self.layout().addWidget(self._toolbar)

        self.highlight(False)

    def text(self):
        """
        Get title text.

        Returns:
            str: Title text.
        """
        return self._label.text()

    def setText(self, text):
        """
        Set title text.

        Arguments:
            text (str): Title text.
        """
        self._label.setText(text)

    def addWidget(self, widget, position):
        """
        Add widget.

        Arguments:
            widget (QWidget): Child widget being added.
            position (int): Where to add the widget.
                Can be `TitleWidget.Left` or `TitleWidget.Right`.
        """
        if position == self.Left:
            index = self.layout().indexOf(self._toolbar)
            self.layout().insertWidget(index, widget)
        elif position == self.Right:
            self.layout().addWidget(widget)
        else:
            raise ValueError(position)

    def toolbar(self):
        """
        Toolbar to which you can add your own actions and widgets.

        Returns:
            Q.QToolBar
        """
        return self._toolbar

    def highlight(self, highlight):
        """Highlight this title widget."""
        palette = self.palette()
        palette.setColor(Q.QPalette.Highlight,
                         self.HIGHLIGHT_COLOR if highlight else self.MAIN_COLOR)
        self.setPalette(palette)

        font = self._label.font()
        font.setBold(highlight)
        self._label.setFont(font)

    def paintEvent(self, _):
        """Redefined from *QWidget.*"""
        base = self.rect().adjusted(0, -1, 0, -1)
        gradient = Q.QLinearGradient(base.topLeft(), base.topRight())
        gradient.setColorAt(0, self.palette().color(Q.QPalette.Highlight))
        gradient.setColorAt(1, self.palette().color(Q.QPalette.Window))
        painter = Q.QPainter(self)
        painter.fillRect(base, gradient)

    def minimumSizeHint(self):
        """Redefined from *QWidget.*"""
        shint = super().minimumSizeHint()
        icon_size = self._toolbar.iconSize().height()
        margin = self._toolbar.layout().contentsMargins().top()+2
        height = max(shint.height(), icon_size+margin*2)
        shint.setHeight(height)
        return shint
