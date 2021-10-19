

"""
Tree widget
-----------

The module implements general purpose tree widget class.

For more details refer to *TreeWidget* class.

"""


from PyQt5 import Qt as Q

from ...common import to_list
from .. import Role

__all__ = ["TreeDelegate", "TreeWidget"]

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


def find_tree_data(parent, value, column, role, full=False):
    """
    Find child tree items that satisfy given condition.

    Arguments:
        parent (QTreeWidgetItem): Parent item.
        value (any): Data being searched.
        column (int): Search column.
        role (Qt.ItemDataRole): Data role.
        full (Optional[bool]): Search criteria: *True* - get all
            matching items; *False* - get first matching item.
    """
    result = []
    for i in range(parent.childCount()):
        item = parent.child(i)
        if item and item.data(column, role) == value:
            result.append(item)
        if result and not full:
            break
        result += find_tree_data(item, value, column, role, full)
    return result


class TreeDelegate(Q.QStyledItemDelegate):
    """
    Custom delegate class, used to restrict data edition by specific
    model columns.
    """

    def __init__(self, columns, parent):
        """
        Create delegate.

        See `setEditColumns()` for more details about *columns*
        parameter.

        Arguments:
            columns (int, list[int]): Editable column(s).
            parent: Parent object.
        """
        super().__init__(parent)
        self.columns = None
        self.setEditColumns(columns)

    def createEditor(self, parent, option, index):
        """
        Returns the widget used to edit the item specified by index for
        editing.

        Arguments:
            parent (QWidget): Parent widget.
            option (QStyleOptionViewItem): Style option.
            index (QModelIndex): Model index object.

        Returns:
            QWidget: Editor widget.
        """
        if index.isValid() and \
                (self.columns is None or index.column() in self.columns):
            return super().createEditor(parent, option, index)
        return None

    def setEditColumns(self, columns):
        """
        Specify editable columns.

        Specify -1 as parameter to enable edition in all model columns.

        Arguments:
            columns (int, list[int]): Editable column(s).
        """
        if columns == -1:
            self.columns = None
        else:
            columns = to_list(columns)
            self.columns = columns if columns else None

    def paint(self, painter, option, index):
        """
        Render item.

        Arguments:
            painter (QPainter): Painter object.
            option (QStyleOptionViewItem): Style option.
            index (QModelIndex): Model index.
        """
        if index.isValid():
            data = index.data(Role.ValidityRole)
            valid = data is None or data
            if not valid:
                option.palette.setBrush(Q.QPalette.Text, Q.Qt.red)
                option.palette.setBrush(Q.QPalette.Highlight, Q.Qt.red)
                option.palette.setBrush(Q.QPalette.HighlightedText, Q.Qt.white)

            data = index.data(Role.ActivityRole)
            active = data is None or data
            if not active:
                option.palette.setBrush(Q.QPalette.Text, Q.Qt.gray)
                option.palette.setBrush(Q.QPalette.Highlight, Q.Qt.gray)
                option.palette.setBrush(Q.QPalette.HighlightedText, Q.Qt.white)
                option.font.setStrikeOut(True)

            data = index.data(Role.HighlightRole)
            hlt = data is not None and data
            if hlt:
                option.palette.setBrush(Q.QPalette.HighlightedText,
                                        Q.Qt.yellow)

        super().paint(painter, option, index)


class TreeWidget(Q.QTreeWidget):
    """Tree widget class that handles mouse double click event."""

    def __init__(self, parent=None):
        """
        Create widget.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        super().__init__(parent)
        self.setItemDelegate(TreeDelegate(-1, self))
        self.setEditTriggers(Q.QTreeWidget.NoEditTriggers)

    def findData(self, value, role, full=False):
        """
        Find child items.

        Arguments:
            value (any): Data being searched.
            role (Qt.ItemDataRole): Data role.
            full (Optional[bool]): Search criteria: *True* - get all
                matching items; *False* - get first matching item.
        """
        return find_tree_data(self.invisibleRootItem(), value, 0, role, full)
