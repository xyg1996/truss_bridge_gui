


#


"""
AsterStudy GUI
--------------

Implementation of base AsterStudy GUI.

"""


import os
import tempfile
from collections import OrderedDict
from functools import partial
from subprocess import call
from configparser import ConfigParser, Error

from PyQt5.Qt import (QApplication, QClipboard, QDesktopServices, QDialog,
                      QFileSystemWatcher, QInputDialog, QMessageBox, QObject,
                      Qt, QUrl, pyqtSignal, pyqtSlot)

from . import (ActionType, Context, Entity, MenuGroup, NodeType, Panel, ResourceDir,
               ResourceType, UrlHandler, WorkingMode, check_selection, clipboard_text,
               get_node_type)
from ..common import (CFG, bold, clean_text, debug_message, debug_mode,
                      get_absolute_dirname, italic, load_icon, load_icon_set,
                      not_implemented, preformat, read_file, to_list,
                      translate, wait_cursor, enable_autocopy)

from .actions import Action
from .behavior import Behavior, behavior
# from .controller import Controller
from .meshview import MeshBaseView
# from .popupmanager import ContextMenuMgr
from .prefmanager import tab_position
# from .widgets import MessageBox
from .workspace import Workspace

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name
# pragma pylint: disable=too-many-lines

# pragma pylint: disable=too-many-public-methods


class AsterGui(QObject, Behavior):
    """Base AsterStudy GUI implementation."""

    selectionChanged = pyqtSignal(int)
    """
    Signal: emitted when selection is changed.

    Arguments:
        context (int): Selection context (see `Context`).
    """

    preferencesChanged = pyqtSignal(object)
    """
    Signal: emitted when application's preferences are changed.

    Arguments:
        pref_mgr (object): Application's preferences manager.
    """

    favoritesChanged = pyqtSignal()
    """
    Signal: emitted when the list of favorite commands is changed.
    """

    # _favoritesMgr = None
    """Instance of favorites manager."""

    def __init__(self):
        """Create GUI wrapper."""
        super().__init__()
        self.main_window = None
        self.work_space = None
        self.actions = {}
        self.cmd_actions = OrderedDict()
        self.aster_study = None
        self.gui_tester = None

        # QApplication.clipboard().changed.connect(self._updateActions)
        # QApplication.clipboard().dataChanged.connect(self._updateActions)

        # template_dir = self.resourceDir(ResourceDir.Templates, ResourceType.User)
        # if not os.path.isdir(template_dir):
        #     os.makedirs(template_dir)
        # template_watcher = QFileSystemWatcher([template_dir], self)
        # template_watcher.directoryChanged.connect(self._updateTemplates)

        # assistant_dir = self.resourceDir(ResourceDir.Assistant, ResourceType.User)
        # if not os.path.isdir(assistant_dir):
        #     os.makedirs(assistant_dir)
        # assistant_watcher = QFileSystemWatcher([assistant_dir], self)
        # assistant_watcher.directoryChanged.connect(self._updateAssistants)

    def initialize(self):
        """Initialize GUI."""
        self._createMainWindow()
        # self._createActions()
        # self._createMenus()
        # self._createToolbars()
        # self._updateActions()

    @staticmethod
    def resourceDir(rcdir, rctype):
        """
        Get location of additional resource files.

        Arguments:
            rcdir (int): Resource directory (see `ResourceDir`).
            rctype (int): Resource type (see `ResourceType`).
        Returns:
            str: Resource directory path.
        """
        rc_dir = CFG.rcdir if rctype == ResourceType.Application \
            else get_absolute_dirname(CFG.userrc)
        dir_name = "assistants" if rcdir == ResourceDir.Assistant else "templates"
        if rctype != ResourceType.Application:
            dir_name = "asterstudy_" + dir_name
        return os.path.join(rc_dir, dir_name)

    def mainWindow(self):
        """
        Get main window.

        Returns:
           QMainWindow: Application's main window.
        """
        return self.main_window

    def workSpace(self):
        """
        Get workspace.

        Returns:
            Workspace: Workspace of AsterStudy GUI.
        """
        return self.work_space

    def workingMode(self):
        """
        Get current working mode.

        Returns:
            int: Current working mode (see `WorkingMode`).
        """
        return self.work_space.workingMode() if self.work_space else None

    def setWorkingMode(self, wmode):
        """
        Set current working mode.

        Arguments:
            wmode (int): Current working mode (see `WorkingMode`).
        """
        if self.workSpace() is not None:
            self.workSpace().setWorkingMode(wmode)

    def selected(self, context=None):
        """
        Get current selection.

        Arguments:
            context (int): Selection context (see `Context`).
                If `None`, then for ``WorkingMode.HistoryMode`` it will use ``Context.Cases``,
                and for ``WorkingMode.CaseMode`` it will use ``Context.DataSettings``.

        Returns:
            list[Entity]: Selected items.
        """
        if not self.work_space:
            return []
        if context:
            return self.work_space.selected(context)
        if self.workingMode() == WorkingMode.HistoryMode:
            return self.work_space.selected(Context.Cases)
        if self.workingMode() == WorkingMode.CaseMode:
            return self.work_space.selected(Context.DataSettings)
        return None

    def view(self, context):
        """
        Get view window.

        Arguments:
            context (int): View type (see `Context`).

        Returns:
            QWidget: View window.
        """
        return self.work_space.view(context) \
            if self.work_space else None

    def study(self):
        """
        Get study.

        Returns:
            Study: Current study.
        """
        return self.aster_study

    def isNullStudy(self, message=None):
        """
        Check if the study is not initialized.

        Arguments:
            message (Optional[str]): Warning message to show. Defaults
                to *None*.

        Returns:
            bool: *True* if current study is *None*; *False* otherwise.
        """
        result = False
        if self.study() is None:
            result = True
            null_message = translate("AsterStudy", "Null study") \
                if message is None else message
            QMessageBox.critical(self.mainWindow(),
                                 "AsterStudy",
                                 null_message)
        return result

    def showMessage(self, msg, timeout=5000):
        """
        Show the message in the status bar with specified timeout.

        Arguments:
            msg (str): Status bar message.
            timeout (Optional[int]): Timeout in milliseconds for
                automatic message clear. Use 0 to show permanent
                message. Defaults to 5000 (5 seconds).
        """
        if self.mainWindow() is not None:
            self.mainWindow().statusBar().showMessage(msg, timeout)

    def clearMessage(self):
        """
        Clear the message in the status bar.
        """
        if self.mainWindow() is not None:
            self.mainWindow().statusBar().clearMessage()

    # pragma pylint: disable=unused-argument,no-self-use
    def showNotification(self, text, timeout=-1):
        """
        Show notification.

        Notification can be removed with hideNotification()
        method.

        Arguments:
            text (str): Notification text.
            timeout (Optional[int]): Timeout after which notification
                should be removed (in seconds). To show permanent
                message, pass 0. Negative value means default behavior
                as controlled by application. Defaults to -1.

        Returns:
            int: Notification's UID.
        """
        print('NOTIFY:', text)
        return -1

    # pragma pylint: disable=unused-argument,no-self-use
    def hideNotification(self, textorid):
        """
        Remove notification with given message or id.

        Arguments:
            textorid (str, int): Notification text or UID.
        """
        print('HIDE:', textorid)

    def createAction(self, text, tooltip, statustip,
                     icon, shortcut, slot, ident, parent, *args):
        """
        Create action.

        Each action is associated with the unique identifier. Action can
        have tooltip, status tip text, icon and shortcut key combination
        and can be connected to the dedicated slot function.

        Arguments:
            text (str): Menu text.
            tooltip (str): Tooltip text.
            statustip (str): Status tip text.
            icon (QIcon): Icon.
            shortcut (str): Shortcut key.
            slot (method): Slot for the action.
            ident (int): Unique identifier (see `ActionType`).
            parent (QObject): Owner of the action.
            *args: Optional list of contexts where action should be
                additionally added.

        Returns:
            QAction: Created action.

        Raises:
            RuntimeError: If action with specified identifier has been
                already added.

        See also:
            `action()`
        """
        if ident and ident in self.actions:
            raise RuntimeError("Action %d already presents in map" % ident)
        action = Action(text, parent)
        if icon and not icon.isNull():
            action.setIcon(icon)
        if shortcut:
            action.setShortcut(shortcut)
            action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
            tooltip = preformat("{0} ({1})".format(tooltip, bold(shortcut)))
        action.setToolTip(tooltip)
        action.setStatusTip(statustip)
        if slot is not None:
            action.triggered.connect(slot)
        if ident:
            self.actions[ident] = action

        if not args:
            parent.mainWindow().addAction(action)
        else:
            for context in args:
                if self.workSpace() is not None:
                    self.workSpace().view(context).addAction(action)

        return action

    def action(self, ident):
        """
        Get action by identifier.

        Arguments:
            ident (int): Action's identifier (see `ActionType`).

        Returns:
           QAction: Action associated with the given identifier.

        See also:
            `createAction()`, `actionId()`
        """
        return self.actions.get(ident)

    def actionId(self, action):
        """
        Get action's identifier.

        Arguments:
            action (QAction): Action.

        Returns:
           int: Action's UID; *None* if action is unknown.

        See also:
            `creatAction()`, `action()`
        """
        uid = None
        for key, value in self.actions.items():
            if value == action:
                uid = key
        return uid

    # pragma pylint: disable=unused-argument,no-self-use
    def createMenu(self, text, parent=-1, group=-1):
        """
        Create menu item in the main menu of application.

        Default implementation raises exception; the method should be
        implemented in successor classes.

        Menu item is specified by its label. If there is already a menu
        with given text, its identifier is returned.

        Parent menu is specified via the identifier; -1 means top-level
        menu.

        Menu items are combined into groups; -1 means most bottom (last)
        group.

        Arguments:
            text (str): Text label of menu item.
            parent (Optional[int]): Parent menu item. Defaults to -1.
            group (Optional[int]): Menu group. Defaults to -1.

        Returns:
            int: Menu item's unique identifier.

        Raises:
            NotImplementedError: The method should be implemented in
                sub-classes.

        See also:
            `addMenuAction()`
        """
        raise NotImplementedError("Method should be implemented in successors")

    def menu(self, *args):
        """
        Get menu by path.

        Menu can be searched by the path which is a string or a list of
        strings.

        Arguments:
            *args: Menu title path: list of strings.

        Returns:
           QMenu: Menu object (None if menu is not found).

        See also:
            `createMenu()`
        """
        path = list(args)
        path.reverse()

        root = self.mainWindow().menuBar()
        menu = None

        while path:
            item = path.pop()
            actions = root.actions()
            found_menu = None
            for action in actions:
                if action.menu() is None:
                    continue
                if clean_text(action.text()) == clean_text(item):
                    found_menu = action.menu()
                    break
            if found_menu is None:
                break
            elif path:
                root = found_menu
            else:
                menu = found_menu
        return menu

    # pragma pylint: disable=unused-argument,no-self-use
    def addMenuAction(self, action, parent, group=-1):
        """
        Add action to the menu.

        Default implementation raises exception; the method should be
        implemented in successor classes.

        Similarly to menu items, actions are combined into groups;
        see `createMenu()` for more details.

        Arguments:
            action (QAction): Menu action.
            parent (int): Parent menu item.
            group (Optional[int]): Menu group. Defaults to -1.

        Raises:
            NotImplementedError: The method should be implemented in
                sub-classes.

        See also:
            `createMenu()`
        """
        raise NotImplementedError("Method should be implemented in successors")

    # pragma pylint: disable=unused-argument,no-self-use
    def createToolbar(self, text, name):
        """
        Create toolbar.

        Default implementation raises exception; the method should be
        implemented in successor classes.

        Toolbar is specified by its label and name.
        Label normally is specified as a text translated to the current
        application's language, while name should not be translated - it
        is used to properly save and restore positions of toolbars.

        Arguments:
            text (str): Text label of toolbar.
            name (str): Unique name of toolbar.

        Returns:
            int: Toolbar's unique identifier.

        Raises:
            NotImplementedError: The method should be implemented in
                sub-classes.

        See also:
            `addToolbarAction()`
        """
        raise NotImplementedError("Method should be implemented in successors")

    # pragma pylint: disable=unused-argument,no-self-use
    def addToolbarAction(self, action, parent):
        """
        Add action to the toolbar.

        Default implementation raises exception; the method should be
        implemented in successor classes.

        Arguments:
            action (QAction): Toolbar action.
            parent (int): Parent toolbar.

        Raises:
            NotImplementedError: The method should be implemented in
                sub-classes.

        See also:
            `createToolbar()`
        """
        raise NotImplementedError("Method should be implemented in successors")

    @pyqtSlot(bool)
    def activateCommand(self):
        """[Edit | Activate] action's slot."""
        self.toggleCommand(True,
                           translate("AsterStudy", "Activate command"))

    @pyqtSlot(bool)
    def deactivateCommand(self):
        """[Edit | Deactivate] action's slot."""
        self.toggleCommand(False,
                           translate("AsterStudy", "Deactivate command"))

    @pyqtSlot(bool)
    def duplicate(self):
        """[Edit | Duplicate] action's slot."""
        if self.isNullStudy():
            return

        selected = self.selected(Context.DataSettings)
        if check_selection(selected, size=1, typeid=NodeType.CutCopyItems):
            node = self.study().node(selected[0])
            new_nodes = to_list(self.study().duplicate(node))
            if new_nodes:
                self.update(autoSelect=new_nodes[-1],
                            context=Context.DataSettings)

    @pyqtSlot(bool)
    def copy(self):
        """[Edit | Copy] action's slot."""
        if self.isNullStudy():
            return

        selected = self.selected(Context.DataSettings)
        if check_selection(selected, typeid=NodeType.CutCopyItems):
            nodes = [self.study().node(i) for i in selected]
            cnt = self.study().copy(nodes)
            if cnt is not None:
                QApplication.clipboard().setText(cnt, QClipboard.Selection)
                QApplication.clipboard().setText(cnt, QClipboard.Clipboard)

    @pyqtSlot(bool)
    def cut(self):
        """[Edit | Cut] action's slot."""
        if self.isNullStudy():
            return

        selected = self.selected(Context.DataSettings)
        if check_selection(selected, typeid=NodeType.CutCopyItems):
            nodes = [self.study().node(i) for i in selected]
            cnt = self.study().cut(nodes)
            if cnt is not None:
                QApplication.clipboard().setText(cnt, QClipboard.Selection)
                QApplication.clipboard().setText(cnt, QClipboard.Clipboard)
            self.update()

    @pyqtSlot(bool)
    def paste(self):
        """[Edit | Paste] action's slot."""
        if self.isNullStudy():
            return

        selected = self.selected(Context.DataSettings)
        if check_selection(selected, size=1, typeid=NodeType.PasteItems):
            stage = self.study().node(selected[0])
            if get_node_type(stage) not in (NodeType.Stage,):
                stage = stage.stage

            cnt = clipboard_text()
            if cnt:
                new_nodes = to_list(self.study().paste(stage, cnt))
                if new_nodes:
                    self.update(autoSelect=new_nodes[0],
                                context=Context.DataSettings)

    @pyqtSlot(bool)
    @pyqtSlot(int)
    def delete(self, context=None):
        """[Edit | Delete] action's slot."""
        if self.isNullStudy():
            return

        context = context if isinstance(context, int) else None
        nodes = [self.study().node(i) for i in self.selected(context)]
        nodes = [i for i in nodes if i is not None]

        is_active_case = False
        for n in nodes:
            if n == self.study().activeCase:
                is_active_case = True
                break

        if nodes and self.study().delete(nodes):
            if is_active_case:
                self._activateCase(self.study().history.current_case)
        self.update()

    @pyqtSlot(bool)
    def find(self):
        """[Edit | Find] action's slot."""
        self.workSpace().view(Context.DataSettings).find()

    @pyqtSlot(bool)
    def newCase(self):
        """[Operations | New case] action's slot."""
        if self.isNullStudy():
            return
        case = self.study().newCase()
        if case is not None:
            self.update(autoSelect=case, context=Context.Cases)

    @pyqtSlot(bool)
    def newCaseFromDB(self):
        """[Operations | New case from database] action's slot."""
        if self.isNullStudy():
            return
        path = ''
        selected = self.selected()
        if check_selection(selected, size=1, typeid=NodeType.Case):
            stages = self.study().node(selected[0]).stages
            if stages:
                path = stages[-1].database_path
        case = self.study().newCaseFromDB(path)
        if case is not None:
            self.update(autoSelect=case, context=Context.Cases)

    @pyqtSlot(bool)
    def importCase(self):
        """[Operations | Import case] action's slot."""
        if self.isNullStudy():
            return
        case, params = self.study().importCase()
        if case is not None:
            self.workSpace().view(Context.RunPanel).updateCachedParams(params)
            self.update(autoSelect=case, context=Context.DataSettings,
                        autoExpand=True)
        wait_cursor(False)

    @pyqtSlot(bool)
    def recoveryMode(self):
        """[Operations | Recovery mode] action's slot."""
        if self.isNullStudy():
            return
        case, params = self.study().importCase(filter="ajs")
        if case is not None:
            self.workSpace().view(Context.RunPanel).updateCachedParams(params)
            self.update(autoSelect=case, context=Context.DataSettings,
                        autoExpand=True)
        wait_cursor(False)

    @pyqtSlot(bool)
    def importCaseTest(self):
        """[Operations | Import testcase] action's slot."""
        if self.isNullStudy():
            return
        case, params = self.study().importCaseTest()
        if case is not None:
            self.workSpace().view(Context.RunPanel).updateCachedParams(params)
            self.update(autoSelect=case, context=Context.DataSettings,
                        autoExpand=True)
        wait_cursor(False)

    @pyqtSlot(bool)
    def exportCaseTest(self):
        """[Operations | Export case] action's slot."""
        if self.isNullStudy():
            return
        selected = self.selected()
        if check_selection(selected, size=1, typeid=NodeType.Case):
            node = self.study().node(selected[0])
            if self.study().exportCaseTest(node):
                self.update()
        wait_cursor(False)

    @pyqtSlot(bool)
    def newStage(self):
        """[Operations | Add stage] action's slot."""
        if self.isNullStudy():
            return
        stage = self.study().newStage()
        if stage is not None:
            self.update(autoSelect=stage, context=Context.DataSettings)
            wait_cursor(False)

    @pyqtSlot(bool)
    def insertStage(self):
        """[Operations | Insert stage] action's slot."""
        if self.isNullStudy():
            return
        selected = self.selected(Context.DataSettings)
        if check_selection(selected, size=1, typeid=NodeType.Stage):
            node = self.study().node(selected[0])
            stage = self.study().newStage(node.number - 1)
            if stage is not None:
                self.update(autoSelect=stage, context=Context.DataSettings)
        wait_cursor(False)

    @pyqtSlot(bool)
    def importStage(self, force_text=False):
        """[Operations | Add stage from file] action's slot."""
        if self.isNullStudy():
            return
        stage = self.study().importStageFromFile(file_name=None,
                                                 force_text=force_text)
        if stage is not None:
            self.update(autoSelect=stage, context=Context.DataSettings,
                        autoExpand=True)
        wait_cursor(False)

    @pyqtSlot(str)
    def importStageFromTemplate(self, template, force_text=False):
        """[Operations | Add stage from template] action's slot."""
        if not os.path.isfile(template):
            return

        stage = self.study().importStageFromFile(file_name=template,
                                                 force_text=force_text)
        if stage is not None:
            self.update(autoSelect=stage, context=Context.DataSettings,
                        autoExpand=True)
        wait_cursor(False)

    @pyqtSlot(bool)
    def exportStage(self):
        """[Operations | Add stage from file] action's slot."""
        if self.isNullStudy():
            return
        selected = self.selected(Context.DataSettings)
        if check_selection(selected, size=1, typeid=NodeType.Stage):
            node = self.study().node(selected[0])
            if self.study().exportStage(node):
                self.update()
        wait_cursor(False)

    @pyqtSlot(bool)
    def reRun(self):
        """[Operations | Re-Run] action's slot."""
        self.setWorkingMode(WorkingMode.HistoryMode)
        self.update(autoSelect=self.study().activeCase, context=Context.Cases)
        dashboard = self.view(Context.Dashboard)
        if dashboard is not None:
            dashboard.reRun()

    @pyqtSlot(bool)
    def rename(self):
        """[Edit | Rename] action's slot."""
        selected = self.selected()
        if check_selection(selected, size=1, typeid=NodeType.Case):
            # if it's running the menu entry is hidden but not the F2 shortcut
            if self.study().node(selected[0]).is_running():
                return
        if check_selection(selected, size=1, typeid=NodeType.RenameItems):
            if self.workingMode() == WorkingMode.HistoryMode:
                self.workSpace().edit(Context.Cases, selected[0])
            elif self.workingMode() == WorkingMode.CaseMode:
                self.workSpace().edit(Context.DataSettings, selected[0])


    @pyqtSlot(bool)
    def groupsInvolved(self):
        """Show involved groups on the right panel."""
        selected = self.selected(Context.DataSettings)
        if check_selection(selected, size=1, typeid=NodeType.Command):
            node = self.study().node(selected[0])
            self.workSpace().panel(Panel.View).showInfo(command=node)

    @pyqtSlot(bool)
    def analysisSummary(self):
        """Summary of involved groups in the analysis."""
        selected = self.selected(Context.DataSettings)
        if check_selection(selected, size=1, typeid=NodeType.Command):
            node = self.study().node(selected[0])
            self.workSpace().panel(Panel.View).showInfo(command=node, is_analysis=True)

    @pyqtSlot(str)
    def addCommand(self, command_type):
        """
        Add a command to the study.

        Arguments:
            command_type (str): Type of the Command being added.
        """
        if self.isNullStudy():
            return
        selected = self.selected(Context.DataSettings)
        if check_selection(selected, size=1, typeid=NodeType.PasteItems):
            stage = self.study().node(selected[0])
            if get_node_type(stage) not in (NodeType.Stage,):
                stage = stage.stage
            command = self.study().addCommand(stage, command_type)
            if command is not None:
                self.update(autoSelect=command, context=Context.DataSettings)
                msg = translate("AsterStudy",
                                "Command with type '{}' successfully added")
                msg = msg.format(command_type)
                self.showMessage(msg)
                if behavior().auto_edit:
                    self.edit()

    @pyqtSlot(bool)
    def backUp(self):
        """[Operations | Back Up] action's slot."""
        if self.isNullStudy():
            return

        wait_cursor(True)
        case = self.study().backUp()
        if case is not None:
            self.update()
        wait_cursor(False)

    @pyqtSlot(bool)
    def copyAsCurrent(self):
        """[Operations | Copy as current] action's slot."""
        if self.isNullStudy():
            return

        selected = self.selected()
        if selected is not None and len(selected) == 1:
            if selected[0].type == NodeType.Case:
                node = self.study().node(selected[0])

                wait_cursor(True)
                if node is not None and self.study().copyAsCurrent(node):
                    self.update()
                wait_cursor(False)

    @pyqtSlot(bool)
    def caseActivation(self):
        """[Operations | View case] action's slot."""
        self.activateCase()

    def activateCase(self, to_case=None):
        """Activate the specified or selected case"""
        if self.isNullStudy():
            return

        selected = self.selected() #if to_case is None else [to_case]
        if selected is not None and len(selected) == 1:
            if selected[0].type == NodeType.Case:
                if AsterGui.prepare_for_new_operation():
                    wait_cursor(True)
                    ctr = Controller(translate("AsterStudy", "Activate case"), self)
                    ctr.controllerStart()
                    node = self.study().node(selected[0])
                    self._activateCase(node)
                    self.setWorkingMode(WorkingMode.CaseMode)
                    wait_cursor(False)
                    ctr.controllerCommit()


    @pyqtSlot(bool)
    def browse(self, context=None):
        """[Operations | Browse] action's slot."""
        if self.isNullStudy():
            return

        selected = self.selected(context)
        if check_selection(selected, size=1, typeid=NodeType.Dir):
            node = self.study().node(selected[0])
            path = node.directory
            QDesktopServices.openUrl(QUrl(path))
        if check_selection(selected, size=1, typeid=NodeType.Unit):
            node = self.study().node(selected[0])
            if node.filename is not None:
                path = os.path.dirname(node.filename)
                QDesktopServices.openUrl(QUrl(path))
        if check_selection(selected, size=1, typeid=NodeType.Case):
            node = self.study().node(selected[0])
            if node.folder is not None:
                QDesktopServices.openUrl(QUrl(node.folder))

    @pyqtSlot(bool)
    def openInParavis(self):
        """[Operations | Open in ParaVis] action's slot."""
        not_implemented(self.mainWindow())

    @pyqtSlot(bool)
    def showResults(self):
        """[Operations | Show Results] action's slot."""
        not_implemented(self.mainWindow())

    @pyqtSlot(bool)
    def showMeshView(self):
        """[View | Show Mesh View] action's slot."""
        view = self.workSpace().panels[Panel.View]
        if view is not None and view.isFeatureSupported("switchable"):
            view.setViewVisible(self.sender().isChecked())

    @classmethod
    def preferencesMgr(cls):
        """
        Get preferences manager.

        Returns:
            object: Application's Preferences manager.

        Raises:
            NotImplementedError: The method should be implemented in
                sub-classes.
        """
        raise NotImplementedError("Method should be implemented in successors")

    def update(self, **kwargs):
        """
        Update application's status: widgets, actions, etc.

        Additional arguments can be passed, to perform specific actions:
            autoSelect: Automatically scroll data browser to given item
                and select it.

        Arguments:
            **kwargs: Keyword arguments.
        """
        if "actions_only" not in kwargs:
            self._updateWindows()
            if "autoSelect" in kwargs and "context" in kwargs:
                node = kwargs["autoSelect"]
                context = kwargs["context"]
                entity = Entity(node.uid)
                self.workSpace().ensureVisible(context, entity, True)
                if "autoExpand" in kwargs and behavior().auto_expand:
                    self.workSpace().expand(context, entity)
        self._updateActions()

    # @pyqtSlot(int, "QPoint")
    # def showContextMenu(self, context, pos):
    #     """
    #     Show context menu.

    #     Arguments:
    #         context (int): Context requesting menu (see `Context`).
    #         pos (QPoint): Mouse cursor position.
    #     """
    #     self._updateActions()
    #     view = self.workSpace().view(context)
    #     if context is not Context.Unknown and view is not None:
    #         popup_mgr = ContextMenuMgr(self, context)
    #         popup_mgr.showContextMenu(view, pos)

    def canAddCommand(self):
        """
        Check if the command can be added to the selected stage.

        This method returns *True* if:

        - GUI is in the Case View;
        - Stage, Category or Command is selected;
        - Parent Stage is in the Graphical Mode.

        Returns:
            *True* if a command can be added to the selected stage;
            *False* otherwise.
        """
        result = False
        if self.study() and self.workingMode() == WorkingMode.CaseMode:
            selected = self.selected(Context.DataSettings)
            if check_selection(selected, size=1, typeid=NodeType.PasteItems):
                stage = self.study().node(selected[0])
                if stage is not None and \
                        get_node_type(stage) not in (NodeType.Stage,):
                    stage = stage.stage
                result = stage is not None and stage.is_graphical_mode()
        return result

    def chooseVersion(self):
        """
        Select version of code_aster to use.

        Returns:
            str: code_aster version.
        """
        result = None
        option = behavior().code_aster_version
        default_version = CFG.default_version
        versions = CFG.options("Versions")
        if not debug_mode():
            versions = [i for i in versions if i != "fake"]
        if option == 'default' or len(versions) < 2:
            result = default_version
        else: # 'ask' and there are more than 1 version
            idx = versions.index(default_version) \
                if default_version in versions else -1
            msg = translate("AsterStudy", "Choose code_aster version")
            choice, ok = QInputDialog.getItem(self.mainWindow(), "AsterStudy",
                                              msg, versions, idx, False)
            if ok:
                result = choice
        return result

    def hasModule(self, name):
        """
        Check if given SALOME module is available.

        Default implementation always returns *False* (no SALOME modules in
        standalone AsterStudy application).

        Returns:
            bool: *True* if module is available; *False* otherwise.
        """
        return False

    def createMeshView(self, parent=None):
        """
        Create Mesh View widget to be inserted into central area of
        workspace.

        Default implementation creates dummy widget (no actual MeshView
        in standalone AsterStudy application).

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
        """
        return MeshBaseView(self, parent)

    def _createMainWindow(self):
        """
        Initialize main window of application.

        This function is called as a part of GUI initialization procedure.

        Default implementation raises exception; the method should be
        implemented in successor classes.

        Raises:
            NotImplementedError: The method should be implemented in
                sub-classes.
        """
        raise NotImplementedError("Method should be implemented in successors")

    def _createWorkspace(self, parent_widget):
        """
        Create workspace.

        Arguments:
            parent_widget (QWidget): Parent widget.

        Returns:
            Workspace: Workspace object.

        See also:
            `workSpace()`
        """
        tbposition = behavior().workspace_tab_position
        workspace_state = self.preferencesMgr().value("workspace_state")
        work_space = Workspace(parent_widget)
        ###
        # try:
        #     work_space.restoreState(workspace_state)
        # except TypeError:
        #     print("_createWorkspace failed")

        # self._connectWorkspace()

        return work_space

    def _connectWorkspace(self):
        """Connect workspace to study."""
        if self.workSpace() is None:
            return

        if self.study() is None:
            return

        view = self.workSpace().view(Context.DataFiles)
        # view.setModel(self.aster_study.dataFilesModel())


    def _createMenus(self):
        """
        Create menus.

        This function is called as a part of GUI initialization procedure.
        """

        # "Edit" menu
        menu_edit = self.createMenu(translate("AsterStudy", "&Edit"),
                                    -1, MenuGroup.Edit)
        self.addMenuAction(self.action(ActionType.Undo), menu_edit)
        self.addMenuAction(self.action(ActionType.Redo), menu_edit)
        self.addMenuAction(None, menu_edit)
        self.addMenuAction(self.action(ActionType.Copy), menu_edit)
        self.addMenuAction(self.action(ActionType.Cut), menu_edit)
        self.addMenuAction(self.action(ActionType.Paste), menu_edit)
        self.addMenuAction(None, menu_edit)
        self.addMenuAction(self.action(ActionType.Edit), menu_edit)
        self.addMenuAction(self.action(ActionType.EditConcepts), menu_edit)
        self.addMenuAction(self.action(ActionType.View), menu_edit)
        self.addMenuAction(None, menu_edit)
        self.addMenuAction(self.action(ActionType.Rename), menu_edit)
        self.addMenuAction(self.action(ActionType.Duplicate), menu_edit)
        self.addMenuAction(self.action(ActionType.Delete), menu_edit)
        self.addMenuAction(None, menu_edit)
        self.addMenuAction(self.action(ActionType.ActivateCommand), menu_edit)
        self.addMenuAction(self.action(ActionType.DeactivateCommand),
                           menu_edit)
        self.addMenuAction(None, menu_edit)
        self.addMenuAction(self.action(ActionType.Find), menu_edit)
        self.addMenuAction(None, menu_edit)
        self.addMenuAction(self.action(ActionType.LinkToDoc), menu_edit)

        # "View" menu
        menu_view = self.createMenu(translate("AsterStudy", "&View"),
                                    -1, MenuGroup.View)
        self.addMenuAction(None, menu_view)
        self.addMenuAction(self.action(ActionType.ShowMeshView), menu_view)
        self.addMenuAction(self.action(ActionType.HideUnused), menu_view)
        self.addMenuAction(self.action(ActionType.CommandGroups), menu_view)

        # "Operations" menu
        menu_operations = self.createMenu(translate("AsterStudy",
                                                    "&Operations"),
                                          -1, MenuGroup.Operations)
        self.addMenuAction(self.action(ActionType.AddCase), menu_operations)
        self.addMenuAction(self.action(ActionType.AddCaseFromDB),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ActivateCase),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.AddStage), menu_operations)
        self.addMenuAction(self.action(ActionType.ImportStage),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ImportTextStage),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.ImportStageFromTemplate),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ImportTextStageFromTemplate),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.AddStageUsingAssistant),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.InsertStage),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ExportStage),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.StageToGraphical),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.StageToText),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.RepairCase),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ValidityReport),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.UnusedConcepts),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.Browse),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.ImportCase), menu_operations)
        self.addMenuAction(self.action(ActionType.ImportCaseTest),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.RecoveryMode),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ExportCaseTest),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ExportToOpenTurns),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.BackUp),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.CopyAsCurrent),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.ReRun),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.EditDescription),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.DeleteResults),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.SetupDirs),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ConnectServers),
                           menu_operations)
        self.addMenuAction(None, menu_operations)
        self.addMenuAction(self.action(ActionType.ShowResults),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.ShowExternalResults),
                           menu_operations)
        self.addMenuAction(self.action(ActionType.LinkToTranslator),
                           menu_operations)

        # "Commands" menu
        menu_commands = self.createMenu(translate("AsterStudy", "&Commands"),
                                        -1, MenuGroup.Commands)
        self.addMenuAction(self.action(ActionType.AddVariable), menu_commands)
        self.addMenuAction(None, menu_commands)
        self.addMenuAction(self.action(ActionType.ShowAll), menu_commands)
        self.addMenuAction(None, menu_commands)
        self.addMenuAction(self.action(ActionType.EditComment), menu_commands)
        self.addMenuAction(None, menu_commands)
        for action in self.cmd_actions.values():
            self.addMenuAction(action, menu_commands)

    def _createToolbars(self):
        """
        Create toolbars.

        This function is called as a part of GUI initialization procedure.
        """

        # "Operations" toolbar
        toolbar_ops = self.createToolbar(translate("AsterStudy",
                                                   "&Operations"),
                                         "OperationsToolbar")
        self.addToolbarAction(self.action(ActionType.UndoList), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.RedoList), toolbar_ops)
        self.addToolbarAction(None, toolbar_ops)
        self.addToolbarAction(self.action(ActionType.Copy), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.Cut), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.Paste), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.Duplicate), toolbar_ops)
        self.addToolbarAction(None, toolbar_ops)
        self.addToolbarAction(self.action(ActionType.Edit), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.EditConcepts),
                              toolbar_ops)
        self.addToolbarAction(self.action(ActionType.View), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.Delete), toolbar_ops)
        self.addToolbarAction(None, toolbar_ops)
        self.addToolbarAction(self.action(ActionType.ShowMeshView), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.HideUnused), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.CommandGroups), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.LinkToDoc), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.LinkToTranslator),
                              toolbar_ops)
        self.addToolbarAction(None, toolbar_ops)
        self.addToolbarAction(self.action(ActionType.AddCase), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.ImportCase), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.AddStage), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.ImportStage), toolbar_ops)
        self.addToolbarAction(self.action(ActionType.ExportStage), toolbar_ops)
        self.addToolbarAction(None, toolbar_ops)
        self.addToolbarAction(self.action(ActionType.StageToGraphical),
                              toolbar_ops)
        self.addToolbarAction(self.action(ActionType.StageToText), toolbar_ops)
        self.addToolbarAction(None, toolbar_ops)
        self.addToolbarAction(self.action(ActionType.ReRun), toolbar_ops)

        # "Commands" toolbar
        toolbar_cmds = self.createToolbar(translate("AsterStudy", "&Commands"),
                                          "CommandsToolbar")
        self.addToolbarAction(self.action(ActionType.AddVariable),
                              toolbar_cmds)
        self.addToolbarAction(self.action(ActionType.ShowAll), toolbar_cmds)
        self.addToolbarAction(None, toolbar_cmds)
        self.addToolbarAction(self.action(ActionType.EditComment),
                              toolbar_cmds)
        self.addToolbarAction(None, toolbar_cmds)
        for action in self.cmd_actions.values():
            self.addToolbarAction(action, toolbar_cmds)

    def _updateWindows(self):
        """Update windows: data browser, etc."""
        if self.workSpace() is not None:
            self.workSpace().updateViews()

    def updateUndoRedo(self):
        """Update Undo/Redo actions."""
        has_study = self.study() is not None
        # Undo
        undo_list = self.study().undoMessages() if has_study else []
        self.action(ActionType.UndoList).setItems(undo_list)
        self.action(ActionType.Undo).setEnabled(len(undo_list) > 0)
        self.action(ActionType.UndoList).setEnabled(len(undo_list) > 0)
        self.action(ActionType.Undo).setVisible(has_study)
        self.action(ActionType.UndoList).setVisible(has_study)
        # Redo
        redo_list = self.study().redoMessages() if has_study else []
        self.action(ActionType.RedoList).setItems(redo_list)
        self.action(ActionType.Redo).setEnabled(len(redo_list) > 0)
        self.action(ActionType.RedoList).setEnabled(len(redo_list) > 0)
        self.action(ActionType.Redo).setVisible(has_study)
        self.action(ActionType.RedoList).setVisible(has_study)

    # pragma pylint: disable=too-many-locals, too-many-statements, too-many-branches
    def _updateActions(self):
        """Update state of actions, menus, toolbars, etc."""
        has_study = self.study() is not None
        is_history_mode = False
        is_case_mode = False
        selected = []
        if has_study:
            if self.workingMode() == WorkingMode.HistoryMode:
                is_history_mode = True
                is_case_mode = False
                selected = self.selected(Context.Cases)
            elif self.workingMode() == WorkingMode.CaseMode:
                is_history_mode = False
                is_case_mode = True
                selected = self.selected(Context.DataSettings)
            elif self.workingMode() == WorkingMode.ResultsMode:
                is_history_mode = False
                is_case_mode = False
                selected = self.selected(Context.Results)
            elif self.workingMode() == WorkingMode.ResultsMode:
                is_history_mode = False
                is_case_mode = False
                selected = self.selected(Context.Results)
            elif self.workingMode() == WorkingMode.ResultsMode:
                is_history_mode = False
                is_case_mode = False
                selected = self.selected(Context.Results)
        is_current = not has_study or self.study().isCurrentCase()
        mesh_view = self.workSpace().panels[Panel.View] \
            if has_study and self.workSpace() is not None else None
        is_mesh_view_enabled = self.workSpace().meshViewEnabled() \
            if has_study and self.workSpace() is not None else False
        current_case = self.study().history.current_case if has_study else None
        is_single = len(selected) < 2
        sel_obj = selected[0] if len(selected) == 1 else None
        sel_node = self.study().node(sel_obj) \
            if has_study and sel_obj is not None else None
        sel_type = sel_obj.type if sel_obj is not None else NodeType.Unknown
        sel_types = NodeType.Unknown
        for s in selected:
            sel_types = sel_types | s.type
        is_text_stage = False
        is_graphic_stage = False
        if sel_type == NodeType.Stage:
            is_text_stage = sel_node.is_text_mode()
            is_graphic_stage = sel_node.is_graphical_mode()

        is_current_selected = False
        for s in selected:
            if self.study().node(s) == current_case:
                is_current_selected = True
                break

        is_not_current_selected = False
        for s in selected:
            if s.type == NodeType.Case and \
                    self.study().node(s) != current_case:
                is_not_current_selected = True
                break

        # Undo / Redo
        self.updateUndoRedo()

        # Business-Oriented Language &Helper
        self.action(ActionType.LinkToTranslator).setVisible(has_study)

        # LinkToDoc
        is_ok = self._commandForDoc() is not None and is_current
        self.action(ActionType.LinkToDoc).setVisible(is_case_mode)
        self.action(ActionType.LinkToDoc).setEnabled(is_ok)

        # Activate & Deactivate
        self.action(ActionType.ActivateCommand).setVisible(is_case_mode)
        self.action(ActionType.DeactivateCommand).setVisible(is_case_mode)

        has_deact = False
        has_act = False
        is_ready = is_case_mode and sel_types and \
            (sel_types & NodeType.ActivateItems == sel_types) and is_current
        if is_ready:
            for s in selected:
                node = self.study().node(s)
                if node:
                    active = node.active
                    has_deact |= not active
                    has_act |= active
        self.action(ActionType.ActivateCommand).setEnabled(has_deact)
        self.action(ActionType.DeactivateCommand).setEnabled(has_act)

        # Duplicate
        is_ok = is_case_mode and sel_types and \
            (sel_types & NodeType.CutCopyItems == sel_types) and is_current
        self.action(ActionType.Duplicate).setVisible(is_case_mode)
        self.action(ActionType.Duplicate).setEnabled(is_ok)

        # Copy & Cut
        is_ok = is_case_mode and sel_types and \
            (sel_types & NodeType.CutCopyItems == sel_types) and is_current
        self.action(ActionType.Copy).setVisible(is_case_mode)
        self.action(ActionType.Copy).setEnabled(is_ok)
        self.action(ActionType.Cut).setVisible(is_case_mode)
        self.action(ActionType.Cut).setEnabled(is_ok)

        # Paste
        is_ok = is_case_mode and \
            (sel_type & NodeType.PasteItems) and \
            is_current and len(clipboard_text())
        self.action(ActionType.Paste).setVisible(is_case_mode)
        self.action(ActionType.Paste).setEnabled(is_ok)

        # Delete
        is_ok1 = is_case_mode and sel_types and \
            (sel_types & NodeType.DeleteItems == sel_types) and is_current
        is_ok2 = is_history_mode and \
            check_selection(selected, typeid=NodeType.Case) and \
            not is_current_selected
        self.action(ActionType.Delete).setVisible(has_study)
        self.action(ActionType.Delete).setEnabled(is_ok1 or is_ok2)

        # Find
        is_ok = is_case_mode
        self.action(ActionType.Find).setVisible(is_case_mode)
        self.action(ActionType.Find).setEnabled(is_ok)

        # Rename
        is_ok1 = is_case_mode and \
            check_selection(selected, size=1, flags=Qt.ItemIsEditable) \
            and is_single and is_current
        is_ok2 = is_history_mode and \
            check_selection(selected, size=1, typeid=NodeType.Case) and \
            not is_current_selected and is_single and \
            not sel_node.is_running()

        self.action(ActionType.Rename).setVisible(has_study)
        self.action(ActionType.Rename).setEnabled(is_ok1 or is_ok2)

        # Edit / View
        is_ok = (sel_type & NodeType.CutCopyItems) or is_text_stage
        self.action(ActionType.Edit).setVisible(is_ok and is_current and not has_deact)
        self.action(ActionType.EditConcepts).setVisible(is_ok and is_current)
        self.action(ActionType.View).setVisible(is_ok and not is_current)
        self.action(ActionType.Edit).setEnabled(is_ok and is_current and not has_deact)
        self.action(ActionType.EditConcepts).setEnabled(is_ok and is_current and is_text_stage)
        self.action(ActionType.View).setEnabled(is_ok and not is_current)

        # Add new stage, Add stage from file
        is_ok = is_case_mode and is_current
        for action_type in (ActionType.AddStage,
                            ActionType.ImportStage,
                            ActionType.ImportTextStage,
                            ActionType.ImportStageFromTemplate,
                            ActionType.ImportTextStageFromTemplate,
                            ActionType.AddStageUsingAssistant):
            self.action(action_type).setVisible(is_case_mode)
            self.action(action_type).setEnabled(is_ok)

        # Insert stage
        is_ok = is_case_mode and sel_type in (NodeType.Stage,)
        self.action(ActionType.InsertStage).setVisible(is_case_mode)
        self.action(ActionType.InsertStage).setEnabled(is_ok)

        # Export stage
        is_ok = is_case_mode and sel_type in (NodeType.Stage,)
        self.action(ActionType.ExportStage).setVisible(is_case_mode)
        self.action(ActionType.ExportStage).setEnabled(is_ok)

        # Show all
        is_ok = is_case_mode and self.study().hasStages() and is_current
        self.action(ActionType.ShowAll).setVisible(is_case_mode)
        self.action(ActionType.ShowAll).setEnabled(is_ok)

        # Add variable
        is_ok = is_case_mode and self.study().hasStages() and is_current
        self.action(ActionType.AddVariable).setVisible(is_case_mode)
        self.action(ActionType.AddVariable).setEnabled(is_ok)

        # Edit comment
        is_ok = is_case_mode and sel_type in (NodeType.Command, NodeType.Variable) and is_current
        self.action(ActionType.EditComment).setVisible(is_case_mode)
        self.action(ActionType.EditComment).setEnabled(is_ok)

        # Graphical mode
        is_ok = is_case_mode and is_text_stage and is_single and is_current
        self.action(ActionType.StageToGraphical).setVisible(is_case_mode)
        self.action(ActionType.StageToGraphical).setEnabled(is_ok)

        # Text mode
        is_ok = is_case_mode and is_graphic_stage and is_single and is_current
        self.action(ActionType.StageToText).setVisible(is_case_mode)
        self.action(ActionType.StageToText).setEnabled(is_ok)

        # Repair commands
        is_ok = is_case_mode and is_current and is_single and not is_text_stage
        self.action(ActionType.RepairCase).setVisible(is_case_mode)
        self.action(ActionType.RepairCase).setEnabled(is_ok)

        # Validity report
        is_ok = is_case_mode and is_current and is_single \
            and (sel_type in (NodeType.Case,) or is_graphic_stage)
        self.action(ActionType.ValidityReport).setVisible(is_case_mode)
        self.action(ActionType.ValidityReport).setEnabled(is_ok)

        # Unused concepts
        is_ok = is_case_mode and is_current and is_single and sel_type in (NodeType.Case,)
        self.action(ActionType.UnusedConcepts).setVisible(is_case_mode)
        self.action(ActionType.UnusedConcepts).setEnabled(is_ok)

        # Run case
        is_ok = is_case_mode and \
            is_current_selected and current_case.can_be_ran() and \
            self.study().url() is not None
        self.action(ActionType.ReRun).setVisible(is_case_mode)
        self.action(ActionType.ReRun).setEnabled(is_ok)

        # Add case
        self.action(ActionType.AddCase).setVisible(is_history_mode)
        self.action(ActionType.AddCase).setEnabled(is_history_mode and is_current)

        # Add case from database
        self.action(ActionType.AddCaseFromDB).setVisible(is_history_mode)
        self.action(ActionType.AddCaseFromDB).setEnabled(is_history_mode)

        # Import case
        self.action(ActionType.ImportCase).setVisible(is_history_mode)
        self.action(ActionType.ImportCase).setEnabled(is_history_mode and is_current)

        # Back up
        self.action(ActionType.BackUp).setVisible(has_study)

        # Import case from a testcase
        self.action(ActionType.ImportCaseTest).setVisible(has_study)
        self.action(ActionType.ImportCaseTest).setEnabled(is_current)

        # Recover the CurrentCase from a Study that can not be loaded
        self.action(ActionType.RecoveryMode).setVisible(has_study)
        self.action(ActionType.RecoveryMode).setEnabled(is_current)

        # Export case for testcase
        self.action(ActionType.ExportCaseTest).setVisible(has_study)
        is_ok = has_study and sel_type in (NodeType.Case,)
        self.action(ActionType.ExportCaseTest).setEnabled(is_ok)

        # Copy as current
        self.action(ActionType.CopyAsCurrent).setVisible(is_history_mode)
        is_ok = is_history_mode and is_not_current_selected
        self.action(ActionType.CopyAsCurrent).setEnabled(is_ok)

        # Edit case's description
        self.action(ActionType.EditDescription).setVisible(has_study)
        is_ok = has_study and is_not_current_selected
        self.action(ActionType.EditDescription).setEnabled(is_ok)

        # Delete results
        is_ok = is_history_mode and \
            check_selection(selected, typeid=NodeType.Case) and \
            not is_current_selected
        if is_ok and self.study() is not None:
            node = self.study().node(selected[0])
            is_ok = node is not None
            if is_ok:
                is_ok = os.path.isdir(node.folder) and \
                        not node.is_used_by_others()
        self.action(ActionType.DeleteResults).setVisible(has_study)
        self.action(ActionType.DeleteResults).setEnabled(is_ok)

        # Activate case
        action = self.action(ActionType.ActivateCase)
        action.setVisible(is_history_mode)
        action.setEnabled(is_history_mode)
        if is_current_selected:
            action.setText(translate("AsterStudy", "&Edit Case"))
            action.setToolTip(translate("AsterStudy", "Edit case"))
            action.setStatusTip(translate("AsterStudy",
                                          "Edit selected Case"))
        else:
            action.setText(translate("AsterStudy", "&View Case (read-only)"))
            action.setToolTip(translate("AsterStudy", "View case (read-only)"))
            action.setStatusTip(translate("AsterStudy",
                                          "View selected case "
                                          "(read-only)"))

        # Set-up input / output directories
        self.action(ActionType.SetupDirs).setVisible(has_study)
        is_ok = has_study and is_current_selected
        self.action(ActionType.SetupDirs).setEnabled(is_ok)

        # Browse
        is_ok = is_history_mode and \
            check_selection(selected, typeid=NodeType.Case) and \
            not is_current_selected
        self.action(ActionType.Browse).setVisible(has_study)
        self.action(ActionType.Browse).setEnabled(is_ok)

        # Show Results
        is_ok = is_case_mode and self.hasModule('PARAVIS')
        self.action(ActionType.ShowResults).setVisible(is_ok)
        is_ok = is_case_mode and sel_type in (NodeType.Unit,) \
            and sel_node.for_paravis
        self.action(ActionType.ShowResults).setEnabled(is_ok)

        # Show External Results
        is_ok = is_case_mode and self.hasModule('PARAVIS')
        self.action(ActionType.ShowExternalResults).setVisible(is_ok)
        self.action(ActionType.ShowExternalResults).setEnabled(is_ok)

        # Export to OpenTurns
        is_ok = debug_mode() or (is_case_mode and self.hasModule('OPENTURNS'))
        self.action(ActionType.ExportToOpenTurns).setVisible(is_ok)
        is_ok = is_case_mode and sel_type in (NodeType.Case,)
        self.action(ActionType.ExportToOpenTurns).setEnabled(is_ok)

        # Show Mesh View
        is_ok = is_case_mode and mesh_view is not None \
            and mesh_view.isFeatureSupported("switchable")
        self.action(ActionType.ShowMeshView).setVisible(is_ok)
        self.action(ActionType.ShowMeshView).setEnabled(is_mesh_view_enabled)


    @pyqtSlot(Entity, str)
    def _itemRenamed(self, entity, value):
        """
        Called when object is renamed.

        Arguments:
            entity (Entity): Selection entity.
            value (str): New item's value.
        """
        if self.isNullStudy():
            return

        node = self.study().node(entity)
        self.study().rename(node, value)
        self.update()

    def _selectionChanged(self, context):
        """
        Called when selection is changed.

        Emits `selectionChanged(int)` signal.

        Arguments:
            context (int): Selection context (see `Context`).
        """
        self._updateActions()

        if context == Context.Dashboard:
            targets = Context.Cases, Context.RunPanel, Context.DataFilesSummary
        elif context == Context.Cases:
            targets = Context.Dashboard, Context.RunPanel, Context.DataFilesSummary
        elif context == Context.DataSettings:
            targets = Context.DataFiles, Context.Information
        else:
            targets = ()

        for target in targets:
            self.workSpace().setSelected(target, self.workSpace().selected(context))
        self.selectionChanged.emit(context)

    def _mkTmpFile(self, text, suffix):
        """
        Create temporary file with the text.

        Arguments:
            text: text to be stored.

        Returns:
            created file name.
        """
        file_name = ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_f:
            tmp_f.write(text)
            file_name = tmp_f.name
        return file_name

    def _activateCase(self, case):
        """
        Activate specified case.

        Arguments:
            case (Case): Case to be active.
        """
        if self.isNullStudy() or case is None:
            return

        if self.study().activeCase != case:
            self.study().activeCase = case
            self.update()

