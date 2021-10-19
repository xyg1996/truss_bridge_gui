

"""
Category view
-------------

The module implements *Category view* used in *Show All* dialog
of AsterStudy application.

For more details refer to *CategoryView* class.

"""


from PyQt5 import Qt as Q

from .. import Role
from ...common import translate
from .filterpanel import FilterWidget

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class CategoryView(FilterWidget):
    """
    Category view.

    Category view is a widget that contains a button and list with child
    items. Pressing on a button collapses/expandes the list box showing
    or hiding child items.

    The items are added to the view via the `addItem()` method.
    Each item can have assiciated identifier. If an identifier is
    assigned to an item, it is passed as a parameter of `selected()`
    and `doubleClicked()` signals; otherwise these signals pass item's
    text as parameter. Method `selection()` that returns a selected
    item, behaves similarly.
    """

    selected = Q.pyqtSignal(str)
    """
    Signal: emitted when selection in the list view is changed.

    Arguments:
        text (str): Selected text (empty if selection is cleared).
    """

    doubleClicked = Q.pyqtSignal(str)
    """
    Signal: emitted when item in the list view is double-clicked.

    Arguments:
        text (str): Item being double-clicked.
    """

    SubCategoryId = -1

    def __init__(self, title, **kwargs):
        """
        Create widget.

        Arguments:
            title (str): Category title.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)
        self._title = title
        self._expanded = True
        self._button = Q.QToolButton(self)
        self._button.setToolButtonStyle(Q.Qt.ToolButtonTextBesideIcon)
        self._button.setSizePolicy(Q.QSizePolicy.MinimumExpanding,
                                   Q.QSizePolicy.Fixed)
        self._list = Q.QListWidget(self)
        self._list.setTextElideMode(Q.Qt.ElideMiddle)
        self._list.setHorizontalScrollBarPolicy(Q.Qt.ScrollBarAlwaysOff)
        self._list.setVerticalScrollBarPolicy(Q.Qt.ScrollBarAlwaysOff)
        v_layout = Q.QVBoxLayout(self)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)
        v_layout.addWidget(self._button)
        v_layout.addWidget(self._list)
        self._button.clicked.connect(self._toggled)
        self._list.itemSelectionChanged.connect(self._selectionChanged)
        self._list.itemDoubleClicked.connect(self._doubleClicked)
        self._adjustSize()
        self._updateState()

    def addItem(self, text, ident=None, subcategory=None):
        """
        Add item into the view.

        Arguments:
            text (str): Item's text.
            ident (Optional[str]): Item's identifier.
        """
        palette = self._list.palette()
        brush = palette.brush(Q.QPalette.Midlight)

        row = 0
        for i in range(self._list.count()):
            if self._list.item(i).data(Role.CustomRole) == subcategory:
                row = i+1

        if subcategory and row == 0:
            item = Q.QListWidgetItem(subcategory)
            font = item.font()
            font.setItalic(True)
            font.setBold(True)
            flags = item.flags()
            flags = flags & ~Q.Qt.ItemIsSelectable
            item.setFont(font)
            item.setTextAlignment(Q.Qt.AlignCenter)
            item.setFont(font)
            item.setFlags(flags)
            item.setBackground(brush)
            item.setData(Role.IdRole, CategoryView.SubCategoryId)
            item.setData(Role.CustomRole, CategoryView.SubCategoryId)
            self._list.addItem(item)
            row = self._list.count()

        item = Q.QListWidgetItem(text)
        item.setData(Role.CustomRole, subcategory)
        if ident is not None:
            item.setData(Role.IdRole, ident)
        self._list.insertItem(row, item)

        self._adjustSize()
        self._updateState()

    def count(self, with_subcategories=False):
        """
        Get number of items in view.

        Returns:
            int: Number of items.
        """
        items = [self._list.item(i) for i in range(self._list.count())]
        if not with_subcategories:
            items = [i for i in items if i.data(Role.IdRole) \
                         != CategoryView.SubCategoryId]
        return len(items)

    def clear(self):
        """
        Remove all items.
        """
        self._list.clear()
        self._adjustSize()
        self._updateState()

    def visibleCount(self, with_subcategories=False):
        """
        Get number of visible (unfiltered) items in view.

        Returns:
            int: Number of visible items.
        """
        items = [self._list.item(i) for i in range(self._list.count())]
        items = [i for i in items if not i.isHidden()]
        if not with_subcategories:
            items = [i for i in items if i.data(Role.IdRole) \
                         != CategoryView.SubCategoryId]
        return len(items)

    def filter(self, text):
        """
        Apply filter.

        Arguments:
            text (str): Regular expression.
        """
        regex = Q.QRegExp(text, Q.Qt.CaseInsensitive)
        visible = 0
        subcategories = {}
        for i in range(self._list.count()):
            item = self._list.item(i)
            if item.data(Role.IdRole) == CategoryView.SubCategoryId:
                subcategories[item.text()] = [item, 0]
                continue
            hidden = False
            if text:
                item_data = item.data(Role.IdRole)
                item_text = item.text()
                hidden = regex.indexIn(item_text) == -1
                if item_data is not None:
                    hidden = hidden and regex.indexIn(item_data) == -1
            item.setHidden(hidden)
            subcategory = item.data(Role.CustomRole)
            if not hidden:
                visible = visible + 1
                if subcategory in subcategories:
                    subcategories[subcategory][1] += 1
            if item.isSelected() and hidden:
                item.setSelected(False)
        for subcategory in subcategories:
            hidden = subcategories[subcategory][1] == 0
            subcategories[subcategory][0].setHidden(hidden)
        self.setHidden(visible == 0)
        self._adjustSize()
        self._updateState()

    def selection(self):
        """
        Get selected item.

        Returns:
            str: Selected item (*None* if there is no selection).
        """
        items = [self._list.item(i) for i in range(self._list.count())]
        items = [i for i in items if i.isSelected() and \
                     i.data(Role.IdRole) != CategoryView.SubCategoryId]
        result = None
        if items:
            item = items[0]
            data = item.data(Role.IdRole)
            result = data if data is not None else item.text()
        return result

    def clearSelection(self):
        """Clear selection."""
        blocked = self._list.blockSignals(True)
        self._list.clearSelection()
        self._list.blockSignals(blocked)

    def select(self, index):
        """
        Set selection to item with given index.

        Note:
            Only viisible items are taken into account.

        Arguments:
            index (int): Item's index
        """
        items = [self._list.item(i) for i in range(self._list.count())]
        items = [i for i in items if not i.isHidden() and \
                     i.data(Role.IdRole) != CategoryView.SubCategoryId]
        if 0 <= index < len(items):
            items[index].setSelected(True)

    def expand(self):
        """Expand widget."""
        self._expanded = True
        self._updateState()

    def collapse(self):
        """Collapse widget."""
        self._expanded = False
        self._updateState()

    @Q.pyqtSlot()
    def _toggled(self):
        """Called when switch button is pressed."""
        self._expanded = not self._expanded
        self._updateState()

    def _updateState(self):
        """Update widget's state."""
        total = self.count()
        visible = self.visibleCount()
        text = translate("CategoryView", "{visible} of {total} items shown") \
            if total != visible else translate("CategoryView", "{total} items")
        text = text.format(**{"total": total, "visible": visible})
        if self._title:
            text = "%s [%s]" % (self._title, text)
        self._button.setText(text)
        self._button.setArrowType(Q.Qt.DownArrow if self._expanded \
                                      else Q.Qt.RightArrow)
        font = self._button.font()
        font.setBold(total != visible)
        self._button.setFont(font)
        self._list.setVisible(self._expanded)

    def _adjustSize(self):
        """Adjust widget's size to its content."""
        delegate = self._list.itemDelegate()
        option = Q.QStyleOptionViewItem()
        size_hint = delegate.sizeHint(option, Q.QModelIndex())
        height = size_hint.height() * self.visibleCount(True)
        if height:
            height = height + 2
        self._list.setFixedHeight(height)

    @Q.pyqtSlot()
    def _selectionChanged(self):
        """
        Called when selection in a view is changed.

        Emits `selected(str)` signal.
        """
        text = ""
        for i in range(self._list.count()):
            if self._list.item(i).isSelected():
                data = self._list.item(i).data(Role.IdRole)
                if data == CategoryView.SubCategoryId:
                    continue
                text = data if data is not None else self._list.item(i).text()
        self.selected.emit(text)

    @Q.pyqtSlot("QListWidgetItem*")
    def _doubleClicked(self, item):
        """
        Called when item in a view is double-clicked.

        Emits `doubleClicked(str)` signal.

        Arguments:
            item (QListWidgetItem): List item being double-clicked.
        """
        if item:
            data = item.data(Role.IdRole)
            if data == CategoryView.SubCategoryId:
                return
            text = data if data is not None else item.text()
            self.doubleClicked.emit(text)
