

"""
Elided label
------------

The module implements label that shows elided text.

For more details refer to *ElidedLabel* class.

"""


from PyQt5 import Qt as Q

__all__ = ["ElidedLabel"]

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class WrapStyle(Q.QStyle):
    """Override given style behaviour."""

    def __init__(self, style):
        """
        Create style wrapper.

        Arguments:
            style (QStyle): Style being wrapped.
        """
        super().__init__()
        self._base_style = style

    def drawComplexControl(self, control, option, painter, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        if self._base_style is not None:
            self._base_style.drawComplexControl(control, option,
                                                painter, widget)
        else:
            super().\
                drawComplexControl(control, option, painter, widget)

    def drawControl(self, element, option, painter, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        if self._base_style is not None:
            self._base_style.drawControl(element, option, painter, widget)
        else:
            super().\
                drawControl(element, option, painter, widget)

    def drawItemText(self, painter, rect, flags, pal, enabled,
                     text, textRole=Q.QPalette.NoRole):
        """See Qt5 documentation for `QStyle` class."""
        if self._base_style is not None:
            self._base_style.drawItemText(painter, rect, flags, pal,
                                          enabled, text, textRole)
        else:
            super().\
                drawItemText(painter, rect, flags, pal,
                             enabled, text, textRole)

    def drawItemPixmap(self, painter, rectangle, alignment, pixmap):
        """See Qt5 documentation for `QStyle` class."""
        if self._base_style is not None:
            self._base_style.drawItemPixmap(painter, rectangle,
                                            alignment, pixmap)
        else:
            super().\
                drawItemPixmap(painter, rectangle, alignment, pixmap)

    def drawPrimitive(self, element, option, painter, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        if self._base_style is not None:
            self._base_style.drawPrimitive(element, option, painter, widget)
        else:
            super().\
                drawPrimitive(element, option, painter, widget)

    def generatedIconPixmap(self, iconMode, pixmap, option):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.generatedIconPixmap(iconMode,
                                                       pixmap, option)
        else:
            res = super().\
                generatedIconPixmap(iconMode, pixmap, option)
        return res

    def hitTestComplexControl(self, control, option, position, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.hitTestComplexControl(control, option,
                                                         position, widget)
        else:
            res = super().\
                hitTestComplexControl(control, option, position, widget)
        return res

    def itemPixmapRect(self, rectangle, alignment, pixmap):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.itemPixmapRect(rectangle, alignment, pixmap)
        else:
            res = super().\
                itemPixmapRect(rectangle, alignment, pixmap)
        return res

    def itemTextRect(self, metrics, rectangle, alignment, enabled, text):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.itemTextRect(metrics, rectangle,
                                                alignment, enabled, text)
        else:
            res = super().\
                itemTextRect(metrics, rectangle, alignment, enabled, text)
        return res

    def layoutSpacing(self, control1, control2,
                      orientation, option=None, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.layoutSpacing(control1, control2,
                                                 orientation, option, widget)
        else:
            res = super().\
                layoutSpacing(control1, control2, orientation, option, widget)
        return res

    def pixelMetric(self, metric, option=None, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.pixelMetric(metric, option, widget)
        else:
            res = super().\
                pixelMetric(metric, option, widget)
        return res

    def sizeFromContents(self, ctype, option, contentsSize, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.sizeFromContents(ctype, option,
                                                    contentsSize, widget)
        else:
            res = super().\
                sizeFromContents(ctype, option, contentsSize, widget)
        return res

    def standardIcon(self, standardIcon, option=None, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.standardIcon(standardIcon, option, widget)
        else:
            res = super().\
                standardIcon(standardIcon, option, widget)
        return res

    def standardPalette(self):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.standardPalette()
        else:
            res = super().standardPalette()
        return res

    def styleHint(self, hint, option=None, widget=None, returnData=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.styleHint(hint, option, widget, returnData)
        else:
            res = super().\
                styleHint(hint, option, widget, returnData)
        return res

    def subControlRect(self, control, option, subControl, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.subControlRect(control, option,
                                                  subControl, widget)
        else:
            res = super().\
                subControlRect(control, option, subControl, widget)
        return res

    def subElementRect(self, element, option, widget=None):
        """See Qt5 documentation for `QStyle` class."""
        res = None
        if self._base_style is not None:
            res = self._base_style.subElementRect(element, option, widget)
        else:
            res = super().\
                subElementRect(element, option, widget)
        return res

    def polish(self, obj):
        """See Qt5 documentation for `QStyle` class."""
        if self._base_style is not None:
            self._base_style.polish(obj)
        else:
            super().polish(obj)

    def unpolish(self, obj):
        """See Qt5 documentation for `QStyle` class."""
        if self._base_style is not None:
            self._base_style.unpolish(obj)
        else:
            super().unpolish(obj)


class Style(WrapStyle):
    """Override drawItemText() behaviour."""

    def drawItemText(self, painter, rect, flags, pal, enabled, text, textRole=Q.QPalette.NoRole):
        """Redefined from QStyle."""
        astr = Q.QFontMetrics(painter.font()).\
            elidedText(text, Q.Qt.ElideRight, rect.width())
        super().drawItemText(painter, rect, flags, pal, enabled, astr, textRole)


class ElidedLabel(Q.QLabel):
    """Label with possibility to display long text elided."""

    def __init__(self, text, parent=None):
        """
        Create label.

        Arguments:
            text (str): Label's text.
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        super().__init__(parent)
        self.setTextFormat(Q.Qt.PlainText)
        clrflags = Q.Qt.TextSelectableByMouse | Q.Qt.TextSelectableByKeyboard
        self.setTextInteractionFlags(self.textInteractionFlags() & ~clrflags)
        self.setStyle(Style(self.style()))
        self.setText(text)
