

"""
Concepts editor
---------------

The module implements an editor for concepts of the text stage.

"""


import re
from collections import OrderedDict

from PyQt5 import Qt as Q

# from .. import translate_command
from ...common import connect, load_icon, translate
from ...datamodel import CATA
from ...datamodel.command import Comment, Hidden, Variable, deleted_by
from ...datamodel.general import CataMixing, ConversionLevel

__all__ = ["ConceptsEditor"]

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class Opts:
    """Options for Concepts editor."""
    # Table columns
    ColumnName = 0         # Name of concept
    ColumnCommand = 1      # Command creating concept
    ColumnType = 2         # Type of concept
    # Options
    RowHeight = 20         # Height of table's row


class Table(Q.QTableView):
    """Concepts table."""

    def __init__(self, parent):
        """Create table."""
        super().__init__(parent)
        connect(self.verticalHeader().sectionCountChanged,
                self.updateRowsHeight)

    def updateRowsHeight(self, _, new_count):
        """Set fixed height for all rows in the table."""
        for i in range(new_count):
            self.setRowHeight(i, Opts.RowHeight)


class NameItem(Q.QStandardItem):
    """Custom table item to manage concept's name."""


class CommandItem(Q.QStandardItem):
    """Custom table item to manage concept's command."""

    def __init__(self, title=None):
        """
        Create item.

        Arguments:
            title (str): Command's catalog title.
        """
        super().__init__()
        self.title = title

    def data(self, role):
        """Get data. Reimplemented from *QStandardItem*."""
        value = None
        if role in (Q.Qt.DisplayRole,):
            if self.title == '_CONVERT_VARIABLE':
                value = translate('ConceptsEditor', 'Variable')
            elif self.title:
                value = command_title(self.title)
        elif role in (Q.Qt.EditRole,):
            value = self.title
        else:
            value = super().data(role)
        return value

    def setData(self, value, role):
        """Set data. Reimplemented from *QStandardItem*."""
        if role in (Q.Qt.EditRole,):
            self.title = value
            self.emitDataChanged()


class TypeItem(Q.QStandardItem):
    """Custom table item to manage concept's type."""

    def __init__(self, typ=None):
        """
        Create item.

        Arguments:
            typ (str): Command's result type.
        """
        super().__init__()
        self.typ = typ

    def data(self, role):
        """Get data. Reimplemented from *QStandardItem*."""
        value = None

        # Variable types are shown by their human-readable names
        # Usual functions' types are displayed using type_title()
        if role in (Q.Qt.DisplayRole,):
            left_sibling_index = self.model().index(self.index().row(), Opts.ColumnCommand)
            if left_sibling_index.data(Q.Qt.EditRole) == '_CONVERT_VARIABLE':
                return {
                    'I':   translate('ConceptsEditor', 'Integer'),
                    'R':   translate('ConceptsEditor', 'Real'),
                    'TXM': translate('ConceptsEditor', 'Text'),
                }.get(self.typ)
            if self.typ:
                value = type_title(self.typ)

        elif role in (Q.Qt.EditRole,):
            value = self.typ

        else:
            value = super().data(role)

        return value

    def setData(self, value, role):
        """Get data. Reimplemented from *QStandardItem*."""
        if role in (Q.Qt.EditRole,):
            self.typ = value
            self.emitDataChanged()


class NameDelegate(Q.QStyledItemDelegate):
    """Custom delegate for concept's name input."""

    def createEditor(self, parent, option, index):
        """Create editor. Reimplemented from QStyledItemDelegate."""
        editor = super().createEditor(parent, option, index)
        editor.setObjectName('name_delegate_editor')
        validator = Q.QRegExpValidator(Q.QRegExp(r"[a-zA-Z]\w{1,7}"))
        editor.setValidator(validator)
        return editor


class UserDataDelegate(Q.QStyledItemDelegate):
    """Delegate which creates editor basing on custom role."""

    def setEditorData(self, editor, index): # pragma pylint: disable=no-self-use
        """
        Set data from model to editor.
        Reimplemented from QStyledItemDelegate.
        """
        item = editor.findData(index.data(Q.Qt.EditRole))
        if item != -1:
            editor.setCurrentIndex(item)

    def setModelData(self, editor, model, index): # pragma pylint: disable=no-self-use
        """
        Set data from editor to model.
        Reimplemented from QStyledItemDelegate.
        """
        data = editor.currentData()
        if data:
            model.setData(index, data, Q.Qt.EditRole)


class CommandDelegate(UserDataDelegate):
    """Custom delegate for concept's command selector."""

    def createEditor(self, parent, option, index): # pragma pylint: disable=unused-argument,no-self-use
        """Create editor. Reimplemented from QStyledItemDelegate."""
        commands = []
        for category in CATA.get_categories('showall'):
            commands.extend(CATA.get_category(category))
        commands.sort()
        editor = Q.QComboBox(parent)
        editor.setObjectName('command_delegate_editor')
        for command in commands:
            if CataMixing.possible_types(command):
                editor.addItem(command_title(command), command)
        editor.addItem(translate('ConceptsEditor', 'Variable'), '_CONVERT_VARIABLE')
        return editor


class TypeDelegate(UserDataDelegate):
    """Custom delegate for concept's type selector."""

    def createEditor(self, parent, option, index): # pragma pylint: disable=unused-argument,no-self-use
        """Create editor. Reimplemented from QStyledItemDelegate."""
        editor = None
        if index.isValid():
            command_index = index.sibling(index.row(),
                                          Opts.ColumnCommand)
            command = command_index.data(Q.Qt.EditRole)
            if command:
                editor = Q.QComboBox(parent)
                editor.setObjectName('type_delegate_editor')

                if command == '_CONVERT_VARIABLE':
                    editor.addItem(translate('ConceptsEditor', 'Integer'), 'I')
                    editor.addItem(translate('ConceptsEditor', 'Real'), 'R')
                    editor.addItem(translate('ConceptsEditor', 'Text'), 'TXM')
                else:
                    types = CataMixing.possible_types(command)
                    for typ in types:
                        editor.addItem(type_title(typ), typ)
        return editor


class ConceptsEditor(Q.QWidget):
    """
    Editor for concepts of the text stage.
    """

    modified = Q.pyqtSignal()
    """
    Signal: emitted when the list of concepts to add or to remove is modified.
    """

    def __init__(self, stage, parent=None, **kwargs):
        """
        Create editor.

        Arguments:
            stage (Stage): Stage to edit.
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
            **kwargs: Keyword arguments.
        """
        super().__init__(parent, **kwargs)

        # ---------
        # Main data
        # ---------

        self.stage = stage
        self.preceding_commands = OrderedDict()
        self.is_modified = False
        self.model = Q.QStandardItemModel(self)
        connect(self.model.dataChanged, self.cellChanged)

        # ------------------------
        # Widgets: concepts to add
        # ------------------------

        # - label
        label_add = Q.QLabel(translate("ConceptsEditor", "Concepts to add"),
                             self)
        label_add.setObjectName('concept_editor_add_lab')

        # - toolbar
        self.toolbar = Q.QToolBar(self)
        self.toolbar.setObjectName('concept_editor_add_toolbar')
        self.toolbar.setToolButtonStyle(Q.Qt.ToolButtonIconOnly)

        # -- 'add concept' button
        action = Q.QAction(load_icon("as_pic_add_row.png"),
                           translate("ConceptsEditor", "&Add Concept"),
                           self)
        action.setToolTip(translate("ConceptsEditor", "Add concept"))
        action.setStatusTip(translate("ConceptsEditor", "Add concept"))
        connect(action.triggered, self.add)
        self.toolbar.addAction(action)

        # -- 'remove concept' button
        action = Q.QAction(load_icon("as_pic_remove_row.png"),
                           translate("ConceptsEditor",
                                     "&Remove Concepts"),
                           self)
        action.setToolTip(translate("ConceptsEditor", "Remove concepts"))
        action.setStatusTip(translate("ConceptsEditor", "Remove selected concepts"))
        connect(action.triggered, self.remove)
        self.toolbar.addAction(action)

        # - table of concepts to add
        self.table = Table(self)
        self.table.setObjectName('concept_editor_add_table')
        self.table.setModel(self.model)
        header_labels = [translate("ConceptsEditor", "Concept"),
                         translate("ConceptsEditor", "Command"),
                         translate("ConceptsEditor", "Type")]
        self.model.setHorizontalHeaderLabels(header_labels)
        header = self.table.horizontalHeader()
        for column in range(len(header_labels)):
            header.setSectionResizeMode(column, Q.QHeaderView.Stretch)
        self.table.verticalHeader().hide()
        self.table.setItemDelegateForColumn(Opts.ColumnName,
                                            NameDelegate(self))
        self.table.setItemDelegateForColumn(Opts.ColumnCommand,
                                            CommandDelegate(self))
        self.table.setItemDelegateForColumn(Opts.ColumnType,
                                            TypeDelegate(self))

        # ---------------------------
        # Widgets: concepts to delete
        # ---------------------------

        # - label
        label_delete = Q.QLabel(translate("ConceptsEditor",
                                          "Existing concepts to delete"),
                                self)
        label_delete.setObjectName('concept_editor_del_lab')

        # - list of concepts
        self.list_widget = Q.QListWidget(self)
        self.list_widget.setObjectName('concept_editor_del_table')
        connect(self.list_widget.itemChanged, self.setModified)

        # ---------------
        # Arrange widgets
        # ---------------

        layout = Q.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(label_add, 0, 0)
        layout.addWidget(self.toolbar, 0, 1)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(label_delete, 2, 0, 1, 2)
        layout.addWidget(self.list_widget, 3, 0, 1, 2)
        layout.setColumnStretch(1, 1)

        # ------------------
        # Initialize widgets
        # ------------------

        self.initialize()

    def initialize(self):
        """
        Initialize GUI controls using the stage and list of catalogue commands.
        """
        # ----------------------------------------------
        # Fill in table of commands defined in the stage
        # ----------------------------------------------

        commands = [i for i in self.stage.commands if is_editable_command(i)]
        blocked = self.table.blockSignals(True)
        already_seen = set()
        for command in commands:
            name = command.name
            typ = command.printable_type
            if name in already_seen:
                continue
            already_seen.add(name)
            if not typ:
                typ = command.gettype(ConversionLevel.NoFail)
                if typ is not None:
                    typ = typ.__name__
            if typ:
                title = None

                if isinstance(command, Hidden):
                    parent = command.model.get_node(command.parent_id)
                    if parent is not None:
                        title = parent.title
                else:
                    title = command.title

                if isinstance(command, Variable):
                    typ = command.gettype()

                if name and title and typ:
                    row = [NameItem(name),
                           CommandItem(title),
                           TypeItem(typ)]
                    self.model.appendRow(row)
        self.table.blockSignals(blocked)

        # ---------------------------------------------------------
        # Fill in table of commands existing in preceding stages
        # including those which are marked as removed by this stage
        # ---------------------------------------------------------

        self.preceding_commands.clear()

        for command in self.stage.preceding_commands(None,
                                                     only_preceding=True):
            if is_editable_command(command):
                self.preceding_commands[command.name] = [command, False]

        preceding_stages = self.stage.preceding_stages
        for stage in preceding_stages:
            for command in stage.commands:
                if is_editable_command(command):
                    name = command.name
                    if name not in self.preceding_commands:
                        self.preceding_commands[name] = [command, False]

        for command in self.stage.commands:
            for cmd in deleted_by(command):
                name = cmd.name
                if name in self.preceding_commands:
                    self.preceding_commands[name][1] = True

        blocked = self.list_widget.blockSignals(True)
        for name, data in self.preceding_commands.items():
            item = Q.QListWidgetItem(name)
            item.setCheckState(Q.Qt.Checked if data[1] else Q.Qt.Unchecked)
            self.list_widget.addItem(item)
        self.list_widget.blockSignals(blocked)

    def setReadOnly(self, on):
        """
        Enable/disable read-only mode for the editor.

        Arguments:
            on (bool): Mode to be set.
        """
        self.toolbar.setVisible(not on)
        if on:
            self.table.setEditTriggers(Q.QAbstractItemView.NoEditTriggers)
        else:
            self.table.setEditTriggers(Q.QAbstractItemView.DoubleClicked |\
                                       Q.QAbstractItemView.EditKeyPressed |\
                                       Q.QAbstractItemView.AnyKeyPressed)

    @Q.pyqtSlot()
    def setModified(self):
        """Set 'modified' flag. Emits `modified()` signal."""
        self.is_modified = True
        self.modified.emit()

    def isApplyAllowed(self):
        """
        Check that the Apply operation is allowed.

        Returns:
            bool: *True* if the Apply operation is allowed; *False* otherwise.
        """
        if not self.is_modified:
            return False
        row_count = self.model.rowCount()
        column_count = self.model.columnCount()
        for row in range(row_count):
            for column in range(column_count):
                item = self.model.item(row, column)
                if not item or not item.text():
                    return False
        return True

    def updateTranslations(self):
        """Update translations in GUI elements."""
        self.table.update()

    @Q.pyqtSlot("QModelIndex")
    def cellChanged(self, index):
        """
        Slot called when the data in the table cell is changed.

        Arguments:
            index (QModelIndex): Data model index
        """
        if index.isValid() and index.column() == Opts.ColumnCommand:
            command = index.data(Q.Qt.EditRole)
            types = CataMixing.possible_types(command) if command else []
            type_index = index.sibling(index.row(), Opts.ColumnType)
            type_current = type_index.data(Q.Qt.EditRole)
            if type_current not in types:
                blocked = self.blockSignals(True)
                type_new = types[0] if types else None
                self.model.setData(type_index, type_new, Q.Qt.EditRole)
                self.blockSignals(blocked)
        self.setModified()

    @Q.pyqtSlot()
    def add(self):
        """
        Slot called when the button *Add concept* is clicked.
        """
        row = [NameItem(), CommandItem(), TypeItem()]
        self.model.appendRow(row)
        blocked = self.table.blockSignals(True)
        self.table.scrollToBottom()
        index = self.model.index(self.model.rowCount()-1, 0)
        self.table.setCurrentIndex(index)
        self.table.blockSignals(blocked)
        self.table.setFocus()
        self.setModified()

    @Q.pyqtSlot()
    def remove(self):
        """
        Slot called when the button *Remove selected concepts* is clicked.
        """
        selected = [i.row() for i in self.table.selectedIndexes()]
        selected = sorted(set(selected), reverse=True)
        if not selected:
            return
        blocked = self.table.blockSignals(True)
        for row in selected:
            self.model.removeRow(row)
        if self.model.rowCount() > 0:
            row_to_select = min(selected[0], self.model.rowCount()-1)
            index = self.model.index(row_to_select, 0)
            self.table.setCurrentIndex(index)
        self.table.blockSignals(blocked)
        self.table.setFocus()
        self.setModified()

    def applyChanges(self):
        """
        Apply changes.
        """
        defs = [(self.model.index(row, Opts.ColumnName).data(),
                 self.model.index(row, Opts.ColumnCommand).data(Q.Qt.EditRole),
                 self.model.index(row, Opts.ColumnType).data(Q.Qt.EditRole))
                for row in range(self.model.rowCount())]
        # Update the commands returned by the stage
        self.stage.update_commands(defs)

        # Process concepts to delete
        dels = []
        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            if item.checkState() == Q.Qt.Checked:
                name = item.text()
                dels.append(name)

        self.stage.delete_commands(dels)

        self.is_modified = False


def is_editable_command(command):
    """
    Check that the command is editable (can be added or removed).

    Arguments:
        command (Command): Command object.

    Returns:
        bool: *True* if the the command is editable; *False* otherwise.
    """
    return not isinstance(command, Comment) and CATA.expects_result(command.cata)


# def command_title(title):
#     """
#     Get granslated title of command.

#     Arguments:
#         title (str): Command's catalog title.

#     Returns:
#         str: Translated title.
#     """
#     value = translate_command(title)
#     if value != title:
#         value = value + " ({})".format(title)
#     return value


def type_title(title):
    """
    Get translated result type.

    Arguments:
        title (str): Typename,

    Returns:
        str: Translated title.
    """
    return re.sub(r'_sdaster$', '', title)
