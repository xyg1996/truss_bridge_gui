

"""
Shrinking combo box
-------------------

The module implements combo box that fits to size of its first item.

This widget is used in custom list actions used to represent
categories of commands in the AsterStudy toolbar.

For more details refer to *ShrinkingComboBox* class.

"""


from PyQt5 import Qt as Q

from .. import Role, behavior

__all__ = ["ShrinkingComboBox"]

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class ShrinkingComboBox(Q.QComboBox):
    """Combo-box which size fits to its first item."""

    def sizeHint(self):
        """
        Get size hint for the combo box.

        Returns:
            QSize: Widget's size hint.
        """
        shint = super().sizeHint()
        fmetrics = self.fontMetrics()
        itext = self.itemText(0) if self.count() > 0 else ""
        textwidth = fmetrics.boundingRect(itext).width()
        iconwidth = self.iconSize().width() + 4 \
            if self.itemIcon(0) is not None else 0
        shint.setWidth(textwidth + iconwidth)
        opt = Q.QStyleOptionComboBox()
        self.initStyleOption(opt)
        shint = self.style().sizeFromContents(Q.QStyle.CT_ComboBox,
                                              opt, shint, self)
        return shint

    def minimumSizeHint(self):
        """
        Get minimal size hint for the combo box.

        Returns:
            QSize: Widget's minimum size hint.
        """
        return self.sizeHint()

    def addSeparator(self, text):
        """
        Add separator item.

        Arguments:
            text (str): Separator's text.
        """
        idx = self.count()
        if behavior().show_separators_in_combobox:
            self.insertSeparator(idx)
            idx += 1

        self.addItem(text)
        font = self.font()
        font.setItalic(True)
        font.setBold(True)
        palette = self.palette()
        brush = palette.brush(Q.QPalette.Midlight)
        self.setItemData(idx, True, Role.CustomRole)
        self.setItemData(idx, font, Q.Qt.FontRole)
        if not behavior().show_separators_in_combobox:
            self.setItemData(idx, brush, Q.Qt.BackgroundRole)
        idx += 1

        if behavior().show_separators_in_combobox:
            self.insertSeparator(idx)

    def isSeparator(self, index):
        """
        Check if given item is a separator.

        Arguments:
            index (int): Item's index.

        Returns:
            bool: *True* if item is a separator; *False* otherwise.
        """
        return self.itemData(index, Role.CustomRole) is True
