

"""
CustomTable: generic customized QTableView with extra features
"""

from PyQt5 import Qt as Q
from ..utils import dbg_print

# pragma pylint: disable=invalid-name


class CustomTable(Q.QTableView):
    """
    Overloaded QTableView class providing the following features:
    1) Extra copy-paste capabilities;
    2) Data validation methods.
    """

    def __init__(self, *args):
        Q.QTableView.__init__(self, *args)

        self.setSelectionMode(Q.QTableView.ExtendedSelection)
        self.installEventFilter(self)

        self.menu = None
        self.editing = None

        self.setHorizontalScrollBarPolicy(Q.Qt.ScrollBarAlwaysOff)

        font = Q.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.setFont(font)

    def setReadOnly(self, state):
        """
        Enable/disable read only state.

        Arguments:
            state (bool): Read only state.
        """
        # editTriggers = Q.QAbstractItemView.DoubleClicked |\
        #     Q.QAbstractItemView.SelectedClicked |\
        #     Q.QAbstractItemView.AnyKeyPressed

        editTriggers = Q.QAbstractItemView.AllEditTriggers
        if state:
            editTriggers = Q.QAbstractItemView.NoEditTriggers
        self.setEditTriggers(editTriggers)

    def isReadOnly(self):
        """ Check that read only state is enabled. """
        return self.editTriggers() ==\
            Q.QAbstractItemView.NoEditTriggers

    def setRowSize(self, size):
        """
        Set default height of the table rows.

        Arguments:
            size (int): Row height.
        """
        self.verticalHeader().setDefaultSectionSize(size)

    def eventFilter(self, source, event):
        """ Event filter. """
        if (event.type() == Q.QEvent.KeyPress and
                event.matches(Q.QKeySequence.Copy)):
            self.copySelection()
            return True

        if (event.type() == Q.QEvent.KeyPress and
                event.matches(Q.QKeySequence.Paste)):
            self.pasteSelection()
            return True

        return self.viewport().eventFilter(source, event)

    def copySelection(self, csvFormat=True):
        """ TODO """
        import io
        import csv
        selection = self.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data(Q.Qt.EditRole)
            stream = io.StringIO()

            csv.writer(stream).writerows(table)
            if csvFormat:
                Q.QGuiApplication.clipboard().setText(stream.getvalue())
            else:
                Q.QGuiApplication.clipboard().setText(
                    stream.getvalue().replace(',', '\t'))

    def pasteSelection(self):
        """TODO : some errors with pasting persist, we seem to overlap
           columns/rows"""

        if self.isReadOnly():
            return

        model = self.model()
        pasteString = str(
            Q.QGuiApplication.clipboard().text()).replace(
                '\r', '').strip()

        splitter = ','
        if '\t' in pasteString:
            splitter = '\t'

        rows = pasteString.split('\n')
        numRows = len(rows)
        numCols = rows[0].count(splitter) + 1

        selectionRanges = self.selectionModel().selection()

        # make sure we only have one selection range and not non-contiguous
        # selections
        if len(selectionRanges) == 1:
            topLeftIndex = selectionRanges[0].topLeft()
            selColumn = topLeftIndex.column()
            selRow = topLeftIndex.row()
            if selColumn + numCols > model.columnCount():
                # the number of columns we have to paste, starting at the
                # selected cell, go beyond how many columns exist.
                # insert the amount of columns we need to accomodate the paste
                model.insertColumns(
                    model.columnCount(),
                    numCols - (model.columnCount() - selColumn))

            # if selRow+numRows>model.rowCount():
            #     #the number of rows we have to paste, starting at the
            #     #selected cell, go beyond how many rows exist.
            #     #insert the amount of rows we need to accomodate the paste
            #    model.insertRows(model.rowCount(),
            #                     numRows-(model.rowCount()-selRow))

            # block signals so that the "dataChanged" signal from setData
            # doesn't update the view for every cell we set
            model.blockSignals(True)

            if '\t' in rows[0]:
                splitter = '\t'
            else:
                splitter = ','

            for row in range(numRows):
                columns = rows[row].split(splitter)
                for col, value in enumerate(columns):
                    currColumn = selColumn + col
                    currRow = selRow + row

                    validator = model.params.validators[currColumn]
                    if isinstance(validator, type((1, 2))):
                        outcome = validator[0](value, validator[1])
                    else:
                        outcome = validator(value)

                    if outcome[0] is True:
                        model.setData(
                            model.createIndex(
                                currRow, currColumn), outcome[1])
                    else:
                        dbg_print(('Invalid Data |%s| encountered column #%d' %
                                   (value, currColumn + 1)))

            # unblock the signal and emit dataChangesd ourselves to update all
            # the view at once
            model.blockSignals(False)
            model.dataChanged.emit(
                model.createIndex(selRow, selColumn),
                model.createIndex(selRow + numRows, selColumn + numCols))

    def addRow(self):
        """ TODO """
        model = self.model()
        if not model:
            return
        model.insertRow(model.rowCount() - 1)

    def insertRow(self, add=0):
        """ TODO """
        model = self.model()
        if not model:
            return
        selection = self.selectedIndexes()
        if selection:
            if add > 0:
                maxRow = 0
                for index in selection:
                    if maxRow < index.row():
                        maxRow = index.row()
                model.insertRows(maxRow + add, 1)
            else:
                minRow = self.model().rowCount() - 1
                for index in selection:
                    if minRow > index.row():
                        minRow = index.row()
                model.insertRows(minRow + add, 1)
        else:
            self.addRow()

    def removeRows(self):
        """ TODO """
        model = self.model()
        if not model:
            return
        selection = self.selectedIndexes()
        if selection:
            for index in selection:
                model.removeRows(index.row())

    def selection(self):
        """ Returns list of selected objects. """
        # TODO
        # pragma pylint: disable=no-self-use
        return []

    def contextMenuEvent(self, _, extraActions=None):
        """ TODO """
        extraActions = extraActions or []

        if not self.selectedIndexes():
            return

        self.menu = Q.QMenu(self)
        self.menu.setFont(self.font())

        # Specific extra actions, careful that here
        # we can not check if this is ok with the
        # readonly status of the table !
        if extraActions:
            for action in extraActions:
                self.menu.addAction(action)
            self.menu.addSeparator()

        if not self.isReadOnly():
            insertAction = Q.QAction('Insert above', self)
            insertAction.triggered.connect(self.insertRow)

            insertBelowAction = Q.QAction('Insert below', self)
            insertBelowAction.triggered.connect(lambda: self.insertRow(add=1))

            removeAction = Q.QAction('Remove', self)
            removeAction.triggered.connect(self.removeRows)

            self.menu.addAction(insertAction)
            self.menu.addAction(insertBelowAction)
            self.menu.addAction(removeAction)
            self.menu.addSeparator()

        copyAction = Q.QAction('Copy', self)
        copyAction.triggered.connect(self.copySelection)
        self.menu.addAction(copyAction)

        self.menu.popup(Q.QCursor.pos())

    def setModel(self, model):
        """Associates a model to the view"""
        Q.QTableView.setModel(self, model)
        model.setView(self)

        self.doubleClicked.connect(self.doubleClickTable)
        self.setColumnDimensions()

    def setColumnDimensions(self):
        """
        Sets convenient column dimensions based on the model parameters
        """

        params = self.model().params
        total_width = self.width() - 25
        widths, uniform = params.col_widths()

        if uniform:
            self.horizontalHeader().setSectionResizeMode(Q.QHeaderView.Stretch)
        else:
            self.horizontalHeader().setSectionResizeMode(Q.QHeaderView.Fixed)

            for i, w in enumerate(widths):
                w = w if (isinstance(w, int) or w > 1) else w * total_width
                widths[i] = w

            sum_widths = sum(widths)
            if sum_widths != total_width:
                ind_max = widths.index(max(widths))
                widths[ind_max] = max(
                    [100, widths[ind_max] + total_width - sum_widths])

            for i, width in enumerate(widths):
                self.setColumnWidth(i, width)
                self.setItemDelegateForColumn(i, GenericLineDelegate(self))

    def mousePressEvent(self, event):
        """Callback to the mouse press event"""

        # self.clearSelection()

        # Hack to close any persisting editor in the table
        if self.editing:
            self.closePersistentEditor(self.editing)

        Q.QTableView.mousePressEvent(self, event)

    @Q.pyqtSlot()
    # pragma pylint: disable=no-self-use
    def doubleClickTable(self):
        """Callback to double clicking a cell in the table"""
        return


class GenericLineDelegate(Q.QItemDelegate):
    """
    Generic line edit delegate enforcing verification methods
    """

    def __init__(self, owner):
        super(GenericLineDelegate, self).__init__(owner)

        self.owner = owner
        self.editor = None

    # pragma pylint: disable=unused-argument
    def createEditor(self, parent, option, index):
        """ TODO """
        self.editor = Q.QLineEdit(parent)

        self.editor.setAlignment(Q.Qt.AlignHCenter)
        self.editor.setStyleSheet('background-color:white;')
        self.owner.editing = index

        return self.editor

    # pragma pylint: disable=no-self-use,unused-argument
    def setEditorData(self, editor, index):
        """ TODO """
        editor.blockSignals(True)

        data = index.model().data(index, Q.Qt.DisplayRole)
        editor.setText(nicer_numerics(data))

        editor.blockSignals(False)

    @classmethod
    def setModelData(cls, editor, model, index):
        """ TODO """
        value = editor.text()

        colName = model.params.headers[index.column()]
        validator = model.params.validators[index.column()]
        if isinstance(validator, (list, tuple)):
            outcome = validator[0](value, validator[1])
        else:
            outcome = validator(value)

        if outcome[0] is False:
            dbg_print(('Invalid Data |%s| for column |%s|' % (value, colName)))
            if len(outcome) == 1:
                return
        value = outcome[1]

        model.setData(index, value, Q.Qt.EditRole)


class GenericTableModel(Q.QAbstractTableModel):
    """Generic Table Model that is associated to the CustomTables
       in the ui Controls and refreshes the ui for a generic
       tab in DataEntry."""

    itemsChanged = Q.pyqtSignal()
    """
    Signal: emitted when one or several rows are added to deleted
    """

    def __init__(self, params, basis, parent=None):
        """Create Generic Table Model."""
        Q.QAbstractTableModel.__init__(self, parent)

        self.view = None
        self.params = params
        self.basis = basis

    # pragma pylint: disable=unused-argument
    def rowCount(self, parent=None):
        """Returns the number of rows under given parent."""
        return len(self.basis)

    # pragma pylint: disable=unused-argument
    def columnCount(self, parent=None):
        """Returns the number of columns under given parent."""
        return len(self.params.headers)

    def setView(self, tableView):
        """Set current table view."""
        self.view = tableView

    def flags(self, index):
        """Returns the item flags for the given table index."""
        flags = Q.Qt.ItemIsEditable |\
            Q.Qt.ItemIsEnabled |\
            Q.Qt.ItemIsSelectable

        column = index.column()
        columnHeader = self.params.headers[column]
        if columnHeader[0] == '_':
            flags ^= Q.Qt.ItemIsEditable  # non-editable

        return flags

    def data(self, index, role):
        """Returns the data stored under the given role
           for the item referred to by the index."""
        row = index.row()
        column = index.column()
        columnHeader = self.params.headers[column]

        if role == Q.Qt.TextAlignmentRole:
            return Q.Qt.AlignCenter

        if role == Q.Qt.EditRole:
            out = self.basis[row][column]
            if out is None:
                out = '-'
            return str(out)

        if role == Q.Qt.DecorationRole:
            out = None

            if columnHeader == '_Color':
                value = Q.QColor(self.basis[row][column])
                pixmap = Q.QPixmap(26, 26)
                pixmap.fill(value)
                out = Q.QIcon(pixmap)
            return out

        if role == Q.Qt.DisplayRole:
            out = self.basis[row][column]
            if columnHeader[0] == '_':
                out = ''
            elif out is None:
                out = ''
            return nicer_numerics(out)

        return None

    def setData(self, index, value, role=Q.Qt.EditRole):
        """Sets the role data for the item at index to value."""
        if role == Q.Qt.EditRole:
            row = index.row()
            column = index.column()
            if column > len(self.params.headers) - 1:
                return False
            if row > len(self.basis) - 1:
                return False

            self.basis[row][column] = value
            self.itemsChanged.emit()
            return True

        return False

    def headerData(self, section, orientation, role):
        """Returns the data for the given role and
           section in the header with the specified orientation."""
        if role == Q.Qt.DisplayRole:
            if orientation == Q.Qt.Horizontal:
                if section < len(self.params.headers):
                    header = self.params.headers[section]
                    if header[0] == '_':
                        return ''
                    return self.params.headers[section]
                return 'not implemented'
            return section + 1
        return None

    def insertRows(self, position, rows, parent=Q.QModelIndex()):
        """Inserts count rows into the model before the given row."""
        self.beginInsertRows(parent, position, position + rows - 1)

        entry = self.basis[position - 1] + \
            [] if position > 0 else self.basis[-1] + []
        self.basis.insert(position, entry)

        self.endInsertRows()

        # Workaround for scrolling down upon insertion of rows at the
        # end of the table
        if position == 0:
            self.view.scrollToBottom()
        else:
            self.view.scrollTo(self.index(position, 0),
                               Q.QAbstractItemView.EnsureVisible)

        self.itemsChanged.emit()
        return True

    # pragma pylint: disable=unused-argument
    def removeRows(self, row, rows=1, parent=Q.QModelIndex()):
        """Removes count rows starting with the given row
           under the given parent from the model."""
        dbg_print('Automatically selecting indices for row removal')
        if not self.view:
            dbg_print('No tableview found')
            return False

        selected = self.view.selectionModel().selectedIndexes()
        dbg_print(('Selected indices detected : %s' % selected))

        counter = 0
        removedRows = []
        for index in selected:
            row = index.row()
            if row not in removedRows:
                # dbg_print(('Requesting removal of row  : %d' % index.row()))
                removedRows.append(index.row())
                self.singleRowRemoval(index.row() - counter)
                counter += 1
        if counter <= 0:
            return False

        self.itemsChanged.emit()
        return True

    def clear(self):
        """Clear the model."""
        r = self.rowCount()
        for _ in range(r):
            self.singleRowRemoval(0)

    def singleRowRemoval(self, row):
        """Removes the given row from the model."""
        if row == self.rowCount() - 1:
            return

        # dbg_print(('>> Effective Removal of 1 row at #%d' % (row)))
        self.beginRemoveRows(Q.QModelIndex(), row, row)

        self.basis.pop(row)

        self.endRemoveRows()

    def values(self):
        """
        Returns the values in the basis, excludes
        columns starting with '__'
        """
        vals = []
        cslice = []
        for i, col in enumerate(self.params.headers):
            if col[:2] != '__':
                cslice.append(i)
        for l in self.basis:
            vals.append([l[i] for i in cslice])
        return vals


def nicer_numerics(value):
    """
    Provides a human friendly representation of a numerical value
    """
    if isinstance(value, str):
        return str(value)
    return "{:1.3E}".format(value)


def ok_validator(value):
    """
    Dummy (always True) validator
    """
    return [True, value]


def float_validator(value):
    """
    Data validator function for float inputs.

    Returns:
        [bool, float(Optional)]:
        - [False] if the data is not valid;
        - [True, proposedValue] if the data is valid.
    """
    try:
        v = float(value)
    # pragma pylint: disable=broad-except
    except BaseException:
        return [False]
    return [True, v]


class TableParams():
    """
    Table parameter class which allows defining column headers
    and some representation parameters
    """
    headers = validators = column_widths = None

    def __init__(self):
        self.headers = []
        self.validators = []
        self.column_widths = []  # Optionnal

    def col_widths(self):
        """
        Returns the column widths if they have been defined,
        otherwise a uniform unitary repartition of the widths
        among columns
        """
        if not self.column_widths:
            nbcols = len(self.headers)
            return [1. / nbcols] * nbcols, True
        return self.column_widths + [], False
