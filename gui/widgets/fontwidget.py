

"""
Font widget
-----------

The module implements dedicated control to set-up font properties.
This widget is used in Preferences dialog.

For more details refer to *ShrinkingComboBox* class.

"""


from PyQt5 import Qt as Q

from ...common import connect

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class FontWidget(Q.QWidget):
    """A widget to control font properties."""

    def __init__(self, parent=None):
        """
        Create widget.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        super().__init__(parent)

        self._family = Q.QFontComboBox(self)
        self._family.setSizePolicy(Q.QSizePolicy.Expanding,
                                   Q.QSizePolicy.Fixed)

        self._size = Q.QComboBox(self)
        self._size.setInsertPolicy(Q.QComboBox.NoInsert)
        self._size.setEditable(True)
        self._size.setValidator(Q.QIntValidator(1, 250, self._size))
        self._size.setSizeAdjustPolicy(Q.QComboBox.AdjustToContents)
        self._size.setSizePolicy(Q.QSizePolicy.Minimum, Q.QSizePolicy.Fixed)

        self.setLayout(Q.QHBoxLayout())
        self.layout().addWidget(self._family)
        self.layout().addWidget(self._size)

        connect(self._family.currentFontChanged, self._fontChanged)

        self._fontChanged()

    def setValue(self, font):
        """
        Set font to the widget.

        Arguments:
            font (QFont): Font value.
        """
        self._family.setCurrentFont(font)
        self._setFontSize(font.pointSize())
        self._fontChanged()

    def value(self):
        """
        Get font from the widget.

        Returns:
            QFont: Font value.
        """
        font = self._family.currentFont()
        font.setPointSize(int(self._size.currentText()))
        return font

    @Q.pyqtSlot()
    def _fontChanged(self):
        """
        Called when font family is changed, to fill the list of available
        sizes.
        """
        blocked = self._size.blockSignals(True)
        old_size = self._size.currentText()
        family = self._family.currentFont().family()
        sizes = Q.QFontDatabase().pointSizes(family)
        sizes = [str(size) for size in sizes]
        self._size.clear()
        self._size.addItems(sizes)
        self._setFontSize(old_size)
        self._size.blockSignals(blocked)

    def _setFontSize(self, size):
        """
        Set font size value.
        """
        value = str(size)
        idx = self._size.findText(value)
        if idx != -1:
            self._size.setCurrentIndex(idx)
        else:
            self._size.setEditText(value)
