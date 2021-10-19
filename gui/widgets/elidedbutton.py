

"""
Elided button
-------------

The module implements button that shows elided text.

For more details refer to *ElidedButton* class.

"""


from PyQt5 import Qt as Q

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class ElidedButton(Q.QPushButton):
    """Button with possibility to display long text elided."""

    def __init__(self, text, parent=None):
        """Constructor."""
        super().__init__(text, parent)
        self.setForegroundRole(Q.QPalette.ButtonText)
        self.setFlat(True)

    def minimumSizeHint(self):
        """Not allow to great increase button size with long text."""
        sz = super().minimumSizeHint()
        sz.setWidth(min(sz.width(), 50))
        return sz

    def sizeHint(self):
        """Not allow to great increase button size with long text."""
        sz = super().sizeHint()
        sz.setWidth(min(sz.width(), 100))
        return sz

    # pragma pylint: disable=unused-argument
    def paintEvent(self, event):
        """Displayed long text as elided."""
        p = Q.QStylePainter(self)
        option = Q.QStyleOptionButton()
        self.initStyleOption(option)
        width = self.style().subElementRect(Q.QStyle.SE_PushButtonContents,
                                            option, self).width()
        bm = self.style().pixelMetric(Q.QStyle.PM_ButtonMargin, option, self)
        fw = self.style().pixelMetric(Q.QStyle.PM_DefaultFrameWidth, option, self) * 2
        width -= (bm + fw)
        option.text = self.fontMetrics().elidedText(self.text(), Q.Qt.ElideRight, width)
        p.drawControl(Q.QStyle.CE_PushButton, option)
