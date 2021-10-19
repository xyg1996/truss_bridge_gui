


#


"""
Implementation of GUI for AsterStudy application.

Common GUI services
-------------------

Basic data types of AsterStudy GUI.

"""


import os
from abc import ABCMeta, abstractproperty
from subprocess import call

from PyQt5 import Qt as Q
from ..common import from_words, load_icon, to_list, to_type, translate

from .behavior import behavior

# from .salomegui import LoadingMessage
# from .salomegui import BackgroundLoading

class NodeType:
    """
    Enumerator for node type.

    Enumeration items are specified as bit flags, so they may be XORed
    and used in bitwise operators.

    Attributes:
        Unknown: Unknown entity.
        History: *History* node.
        Case: *Case* node.
        Stage: *Stage* node.
        Category: *Category* node.
        Command: *Command* node.
        Variable: *Variable* node.
        Comment: *Comment* node.
        Unit: *File* node.
        Macro: Result of macro.
        Dir: *Directory* node.
        Result: *Result* node.
        NoChildrenItems: Items which do not have children in data tree.
        ValidityItems: Items which show validity status in data tree.
        EditItems: Items for which *Edit* is applicable.
        DeleteItems: Items for which *Delete* is applicable.
        RenameItems: Items for which *Rename* is applicable.
        CutCopyItems: Items for which *Cut* & *Copy* are applicable.
        PasteItems: Items for which *Paste* is applicable.
        DMItems: Items which correspond to a node in the datamodel.
    """

    Unknown = 0x0000
    History = 0x0001
    Case = 0x0002
    Stage = 0x0004
    Category = 0x0008
    Command = 0x0010
    Variable = 0x0020
    Comment = 0x0040
    Unit = 0x0080
    Macro = 0x0100
    Dir = 0x0200
    Result = 0x0400
    NoChildrenItems = Command | Variable | Comment | Macro
    ValidityItems = Command | Variable | Macro | Category | Stage | Case
    EditItems = Command | Variable | Comment | Stage | Dir
    DeleteItems = Command | Variable | Comment | Category | Stage | Dir
    RenameItems = Case | Stage | Command | Variable
    CutCopyItems = Command | Variable | Comment
    PasteItems = Command | Variable | Comment | Macro | Category | Stage
    DMItems = History | Case | Stage | Command | Variable | Comment
    ActivateItems = Command | Variable
    # add new values before this line; don't forget to add docstring above

    @staticmethod
    def value2str(value):
        """
        Get title for given node type.

        Arguments:
            value (int): Node type (*NodeType*).

        Returns:
            str: Node type's title.
        """
        text = translate("AsterStudy", "Unknown")
        if value == NodeType.History:
            text = translate("AsterStudy", "History")
        elif value == NodeType.Case:
            text = translate("AsterStudy", "Case")
        elif value == NodeType.Stage:
            text = translate("AsterStudy", "Stage")
        elif value == NodeType.Category:
            text = translate("AsterStudy", "Category")
        elif value == NodeType.Command:
            text = translate("AsterStudy", "Command")
        elif value == NodeType.Variable:
            text = translate("AsterStudy", "Variable")
        elif value == NodeType.Comment:
            text = translate("AsterStudy", "Comment")
        elif value == NodeType.Unit:
            text = translate("AsterStudy", "File")
        elif value == NodeType.Macro:
            text = translate("AsterStudy", "Macro")
        elif value == NodeType.Dir:
            text = translate("AsterStudy", "Directory")
        return text


class Role:
    """
    Enumerator for custom data role.

    Attributes:
        IdRole: Item's identifier.
        TypeRole: Item's type.
        ExpandedRole: Expanded status.
        ValidityRole: Validity status.
        VisibilityRole: Visibility status.
        SortRole: Used for custom sorting.
        HighlightRole: Used for highlighting found items
        ReferenceRole: Used to store 'is reference' attribute.
        ActivityRole: Used to store 'active' attribute.
        CustomRole: Can be used for custom purposes.
    """

    IdRole = Q.Qt.UserRole + 1
    TypeRole = Q.Qt.UserRole + 2
    ExpandedRole = Q.Qt.UserRole + 3
    ValidityRole = Q.Qt.UserRole + 4
    VisibilityRole = Q.Qt.UserRole + 5
    SortRole = Q.Qt.UserRole + 6
    HighlightRole = Q.Qt.UserRole + 7
    ReferenceRole = Q.Qt.UserRole + 8
    ActivityRole = Q.Qt.UserRole + 9
    CustomRole = Q.Qt.UserRole + 10
    # add new values before this line; don't forget to add docstring above


class WorkingMode:
    """
    Enumerator for working mode.
    Workspace下所有tab标签页的序号

    Attributes:
        JianmoMode:    第0页，参数化几何建模页(包含OCC视窗)
        SettingMode:   第1页，前处理(包含SMESH模块VTK视窗)
        QianchuliMode: 第2页，求解器计算所需参数的交互
        KongzhiMode:   第3页，计算控制与监视
        ResultsMode:   第4页，后处理(包含Paraview视窗)
    """

    StartMode = 0
    JianmoMode = 1
    SettingMode = 2
    QianchuliMode = 3
    KongzhiMode = 4
    ResultsMode = 5
    
    # add new values before this line; don't forget to add docstring above

    @staticmethod
    def value2pref(value):
        """
        Get preference item for given working mode.

        Arguments:
            value (int): Working mode (*WorkingMode*).

        Returns:
            str: Preference item.
        """
        pref = ""
        if value == WorkingMode.HistoryMode:
            pref = "history_view"
        elif value == WorkingMode.CaseMode:
            pref = "case_view"
        else:
            raise TypeError("Invalid working mode: {}".format(value))
        return pref

    @staticmethod
    def pref2value(pref):
        """
        Get working mode for given preference item.

        Arguments:
            pref (str): Preference item.

        Returns:
            int: Working mode (*WorkingMode*).
        """
        value = -1
        if pref == "history_view":
            value = WorkingMode.HistoryMode
        elif pref == "case_view":
            value = WorkingMode.CaseMode
        else:
            raise TypeError("Invalid preference: {}".format(pref))
        return value


class Panel:
    """
    Enumerator for Workspace's panel.

    Attributes:
        Data: *Data* panel.
        View: *View* panel.
        Edit: *Edition* panel.
    """

    Data = 1
    View = 2
    Edit = 3
    # add new values before this line; don't forget to add docstring above


class Context:
    """
    Enumerator for GUI context.

    Attributes:
        Unknown: Unknown context.
        DataSettings: *Case* working mode: *Data Settings* view.
        DataFiles: *Case* working mode: *Data Files* view.
        Information: *Case* working mode: *Information* view.
        Cases: *History* working mode: *Cases* view.
        Dashboard: *History* working mode: *Dashboard* view.
        RunPanel: *History* working mode: *Run parameters* view.
        DataFilesSummary: *History* working mode: *Data File Summary* view.
        Results : *Results* working mode: *Results list and postpro view*
    """

    Unknown = 0
    DataSettings = 1
    DataFiles = 2
    Information = 3
    Cases = 4
    Dashboard = 5
    RunPanel = 6
    DataFilesSummary = 7
    Results = 8
    # add new values before this line; don't forget to add docstring above


class ActionType:
    """
    Enumerator for GUI actions.

    Attributes:
        NewStudy: Create study.
        OpenStudy: Open study from file.
        SaveStudy: Save study.
        SaveStudyAs: Save study to another file.
        CloseStudy: Close study.
        Exit: Exit application.
        Options: Show *Preferences* dialog.
        UserGuide: Show *User's Guide*.
        AboutApp: Show *About* dialog.
        Undo: Undo last operation.
        UndoList: Undo set of operations.
        Redo: Redo last undone operation.
        RedoList: Redo several operations.
        Duplicate: Duplicate object.
        Delete: Delete object(s).
        Rename: Rename object.
        Edit: Edit object.
        AddStage: Add new stage.
        ImportStage: Import stage from *COMM* file.
        ExportStage: Export stage to *COMM* file.
        ShowAll: Add commands from catalog.
        StageToGraphical: Convert stage to graphical mode.
        StageToText: Convert stage to text mode.
        AddCase: Add new case.
        CopyAsCurrent: Copy selected *Run case* into *Current case*.
        ActivateCase: Set selected case as active one.
        View: View object.
        ImportCase: Add new case by importing from file.
        LinkToDoc: Show documentation of selected object.
        AddVariable: Create variable.
        Copy: Copy to clipboard.
        Cut: Cut to clipboard.
        Paste: Paste from clipboard.
        EditComment: Edit comment.
        HideUnused: Show/hide unused keywords.
        AddFile: Add file to study.
        EmbedFile: Embed/unembed data file to/from study.
        GoTo: Browse to selected object.
        OpenInParaVis: Open MED file in ParaVis module.
        OpenInEditor: Open file in text editor.
        BackUp: Back up case.
        EditDescription: Edit description.
        ReRun: Execute case with previous parameters.
        DeleteResults: Delete results of selected *Run case*.
        Find: Find data.
        SetupDirs: Set-up input and output directories.
        Remove: Remove file or directory from disk.
        Browse: Open file or directory in a browser.
        ImportTextStage: Import text stage from *COMM* file.
        ExportCaseTest: Export the current case to make a testcase.
        ImportCaseTest: Add new case by importing a testcase.
        LinkToTranslator: Open url to code_aster language translator.
        ExportToOpenTurns: Export data to OpenTurns module.
        ValidityReport: Show dialog with validity report for stage.
        ImportStageFromTemplate: Import graphical stage from template.
        ImportTextStageFromTemplate: Import text stage from template.
        OpenWith: Open file with selected program.
        ShowMeshView: Show / hide mesh view.
        ActivateCommand: Activate the selected command.
        DeactivateCommand: Deactivate the selected command.
        EditConcepts: Edit concepts of text stage.
        InsertStage: Insert a stage at the current position.
        ConnectServers: Connect remote servers.
        AddStageUsingAssistant: Add a stage using the calculation asssistant.
        GroupsInvolved: View involved mesh groups in a command definition.
        AnalysisSummary: View a recap of mesh groups for an analysis command.
        AddCaseFromDB: Init a new Case from a database.
        ConvertMesh: Convert a mesh file into a SMesh object.
        UnusedConcepts: Detect unused concepts.
        RecoveryMode: Recover the CurrentCase of a Study.
        RepairCase: Repair commands dependency in a Stage.
        CommandGroups: View involved mesh groups in a command (Parameters panel).
        ShowResults: Show results from MED file in AsterStudy results tab.
        ShowExternalResults: Show results from an external MED file.

        ShowConsole: Show / hide embedded console (debug mode only).
        ExecScript: Execute script in embedded console (debug mode only).
    """

    NewStudy = 1
    OpenStudy = 2
    SaveStudy = 3
    SaveStudyAs = 4
    CloseStudy = 5
    Exit = 6
    Options = 7
    UserGuide = 8
    AboutApp = 9
    Undo = 10
    UndoList = 11
    Redo = 12
    RedoList = 13
    Duplicate = 14
    Delete = 15
    Rename = 16
    Edit = 17
    AddStage = 18
    ImportStage = 19
    ExportStage = 20
    ShowAll = 21
    StageToGraphical = 22
    StageToText = 23
    AddCase = 24
    CopyAsCurrent = 25
    ActivateCase = 26
    View = 27
    ImportCase = 28
    LinkToDoc = 29
    AddVariable = 30
    Copy = 31
    Cut = 32
    Paste = 33
    EditComment = 34
    HideUnused = 35
    AddFile = 36
    EmbedFile = 37
    GoTo = 38
    OpenInEditor = 39
    OpenInParaVis = 40
    BackUp = 41
    EditDescription = 42
    ReRun = 43
    DeleteResults = 44
    Find = 45
    SetupDirs = 46
    Remove = 47
    Browse = 48
    ImportTextStage = 49
    ExportCaseTest = 50
    ImportCaseTest = 51
    LinkToTranslator = 52
    ExportToOpenTurns = 53
    ValidityReport = 54
    ImportStageFromTemplate = 55
    ImportTextStageFromTemplate = 56
    OpenWith = 57
    ShowMeshView = 58
    ActivateCommand = 59
    DeactivateCommand = 60
    EditConcepts = 61
    InsertStage = 62
    ConnectServers = 63
    AddStageUsingAssistant = 64
    GroupsInvolved = 65
    AnalysisSummary = 66
    AddCaseFromDB = 67
    ConvertMesh = 68
    UnusedConcepts = 69
    RecoveryMode = 70
    RepairCase = 71
    CommandGroups = 72
    ShowResults = 73
    ShowExternalResults = 74
    # add new values BEFORE this line; don't forget to add docstring above

    # next commands are for debug mode only
    ShowConsole = 100
    ExecScript = 101


class MenuGroup:
    """
    Enumerator for menu group UID.

    Attributes:
        File: *File* menu.
        Edit: *Edit* menu.
        View: *View* menu.
        Operations: *Operations* menu.
        Commands: *Commands* menu.
        Test: *Test* menu (debug mode only).
        Help: *Help* menu.
    """

    File = 0
    Edit = 5
    View = 10
    Operations = 20
    Commands = 30
    Test = 99
    Help = 100
    # add new values before this line; don't forget to add docstring above


class ResourceDir:
    """
    Enumerator for resource directory.

    Attributes:
        Assistant: Calculation assistants directory.
        Templates: Templates directory.
    """
    Assistant = 0
    Templates = 1


class ResourceType:
    """
    Enumerator for resource type.

    Attributes:
        Appplication: Application resources.
        User: User resources.
    """
    Application = 0
    User = 1


class Entity:
    """
    Class that represents selection entity.

    Attributes:
        uid (int): Entity identifier.
        type (int): Entity type (*NodeType*).
        flags (int): Entity flags (*Qt.ItemFlags*).
        args (dict): Extra attributes.
    """

    def __init__(self, uid, typeid=NodeType.Unknown, flags=None, **kwargs):
        """
        Create selection entity.

        Arguments:
            uid (int): Identifier of the item.
            typeid (Optional[int]): Type of the item (*NodeType*).
                Defaults to *NodeType.Unknown*.
            flags (Optional[int]): Item flags. Defaults to *None*.
            **kwargs: Additional named attributes.
        """
        self.type = typeid
        self.uid = uid
        self.flags = flags
        self.args = {}
        self.args.update(kwargs)

    def arg(self, name, default=None):
        """
        Get named attribute.

        Arguments:
            name (str): Parameter's name.
            default (Optional[any]): Default value. Defaults to *None*.

        Returns:
            any: Attribute's value: *None* if no such attribute or
            *default* if it's specified.
        """
        values = {}
        values["type"] = self.type
        values["uid"] = self.uid
        values["flags"] = self.flags
        return values.get(name) or self.args.get(name, default)

    def __repr__(self):
        """
        Get string representation of the selection entity.
        """
        value = "uid={uid} type={type}".format(uid=self.uid, type=self.type)
        if self.flags is not None:
            value += " flags={flags}".format(flags=self.flags)
        for arg in sorted(self.args):
            value += " {name}={value}".format(name=arg, value=self.arg(arg))
        return "<" + value + ">"


class HistoryProxy:
    """
    Base class for referencing *History* instance inside category model.

    Successor classes should define the following properties:

    - *root*: To refer to the root node of data tree;
    - *case*: To refer to the case being managed.

    The *case* property depends on a type of *root*:

    - If *root* is a *Stage* or a *Command*, *case* property should be
      equal to *None*;
    - If *root* is a *Case*, *case* property should be equal to *root*;
    - If *root* is a *History*, *case* should be one of its child nodes,
      a valid *Case*.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
    def root(self):
        """
        Get root node of the data tree.

        Returns:
            Node: Root data tree node.
        """
        return None

    @abstractproperty
    def case(self):
        """
        Get case being managed.

        Returns:
            Case: *Case* object.
        """
        return None


def check_selection(selection, **kwargs):
    """
    Check that selection suits specified conditions.

    Conditions are specified as the keyword arguments; supported
    criteria are currently the following:

    - size (int): Number of selected entities.
    - typeid (int, list[int]): Type(s) of selected item(s).
    - flags (int): Item flags (*Qt.ItemFlags*).

    Arguments:
        selection (list[Entity]): Selected entities.
        **kwargs: Keyword arguments specifying selection criteria.

    Returns:
        bool: *True* if selection suits given criteria; *False*
        otherwise.
    """
    def _match(_types, _sel):
        _matched = False
        for _type in _types:
            if _type & _sel:
                _matched = True
                break
        return _matched
    result = True
    if "size" in kwargs:
        result = result and len(selection) == kwargs["size"]
    else:
        result = bool(selection)
    if result and "typeid" in kwargs:
        typeid = to_list(kwargs["typeid"])
        for item in selection:
            result = result and _match(typeid, item.type)
            if not result:
                break
    if result and "flags" in kwargs:
        for item in selection:
            result = result and (item.flags & kwargs["flags"])
            if not result:
                break
    return result


def translate_category(category):
    """
    Translate category.

    Arguments:
        category (str): Category title.

    Returns:
        str: Translated category title.
    """
    return translate("Categories", category)


def root_node_type():
    """
    Get root item's type.

    Returns:
        int: Root item's typeid.
    """
    return 0


def get_node_type(obj):
    """
    Get object's typeid.

    Arguments:
        obj (str, Node, Category): Object being checked or its typename.

    Returns:
        int: Object's typeid (*NodeType*); *NodeType.Unknown* for
        unknown entity.
    """
    if isinstance(obj, str):
        type_name = obj
    elif isinstance(obj, type):
        type_name = obj.__name__
    else:
        type_name = obj.__class__.__name__
    types = {
        "History" : NodeType.History,
        "Case" : NodeType.Case,
        "Stage" : NodeType.Stage,
        "Category" : NodeType.Category,
        "Command" : NodeType.Command,
        "Formula" : NodeType.Command,
        "Variable" : NodeType.Variable,
        "Comment" : NodeType.Comment,
        "Unit" : NodeType.Unit,
        "File" : NodeType.Unit,
        "Dir" : NodeType.Dir,
        "Directory" : NodeType.Dir,
        "Hidden" : NodeType.Macro,
        "Macro" : NodeType.Macro,
        # Postprocessing navigator tree
        "Concept": NodeType.Result,
        "Point Field": NodeType.Result,
        "Cell Field": NodeType.Result,
        "Group Visible": NodeType.Result,
        # ParaView Control (PVC) buttons
        "PVC Clear": NodeType.Result,
        "PVC Refresh": NodeType.Result,
        "PVC XProj": NodeType.Result,
        "PVC YProj": NodeType.Result,
        "PVC ZProj": NodeType.Result,
        "PVC TFirst": NodeType.Result,
        "PVC TPrev": NodeType.Result,
        "PVC Play": NodeType.Result,
        "PVC Pause": NodeType.Result,
        "PVC TNext": NodeType.Result,
        "PVC TLast": NodeType.Result,
        "PVC Outline": NodeType.Result,
        "PVC Reference": NodeType.Result,
        "PVC MinMax": NodeType.Result,
        "PVC Rescale": NodeType.Result,
        "PVC Probe": NodeType.Result,
        "PVC Plot": NodeType.Result,
        "PVC Screenshot": NodeType.Result,
        "PVC Movie": NodeType.Result,
        "CB Sep": NodeType.Result,
        "CB Insert": NodeType.Result,
        "CB Remove": NodeType.Result,
        }
    return types.get(type_name, NodeType.Unknown)


def get_icon(obj):
    """
    Get icon for the given object.

    Arguments:
        obj (Node, Category): Object.

    Returns:
        QIcon: Object's icon (*None* if icon is not specified).
    """

    if not hasattr(get_icon, "icons"):
        get_icon.icons = {}
        get_icon.icons["history"] = load_icon("as_ico_history.png")
        get_icon.icons["run_case"] = load_icon("as_ico_run_case.png")
        get_icon.icons["backup_case"] = load_icon("as_ico_backup_case.png")
        get_icon.icons["current_case"] = load_icon("as_ico_current_case.png")
        get_icon.icons["stage_graph"] = load_icon("as_ico_graphical_stage.png")
        get_icon.icons["stage_text"] = load_icon("as_ico_text_stage.png")
        get_icon.icons["category"] = load_icon("as_ico_category.png")
        get_icon.icons["command"] = load_icon("as_ico_command.png")
        get_icon.icons["variable"] = load_icon("as_ico_variable.png")
        get_icon.icons["comment"] = load_icon("as_ico_comment.png")
        get_icon.icons["macro"] = load_icon("as_ico_macro.png")
        get_icon.icons["unit"] = load_icon("as_ico_file.png")
        get_icon.icons["dir"] = load_icon("as_ico_dir.png")
        # Post-processing icons
        get_icon.icons["concept"] = load_icon("as_ico_concept.png")
        get_icon.icons["point_field"] = load_icon("as_ico_point_field.png")
        get_icon.icons["cell_field"] = load_icon("as_ico_cell_field.png")
        get_icon.icons["group_visible"] = load_icon("as_ico_eye_off.png")
        get_icon.icons["pvc_clear"] = load_icon("as_ico_pv_clear.png")
        get_icon.icons["pvc_refresh"] = load_icon("as_ico_refresh.png")
        get_icon.icons["pvc_xproj"] = load_icon("as_ico_xproj.png")
        get_icon.icons["pvc_yproj"] = load_icon("as_ico_yproj.png")
        get_icon.icons["pvc_zproj"] = load_icon("as_ico_zproj.png")
        get_icon.icons["pvc_tprev"] = load_icon("as_ico_tprev.png")
        get_icon.icons["pvc_tnext"] = load_icon("as_ico_tnext.png")
        get_icon.icons["pvc_outline"] = load_icon("as_ico_outline.png")
        get_icon.icons["pvc_minmax"] = load_icon("as_ico_minmax.png")
        get_icon.icons["pvc_screenshot"] = load_icon("as_ico_screenshot.png")
        get_icon.icons["pvc_movie"] = load_icon("as_ico_movie.png")
        get_icon.icons["pvc_reference"] = load_icon("as_ico_reference.png")
        get_icon.icons["pvc_play"] = load_icon("as_ico_play.png")
        get_icon.icons["pvc_pause"] = load_icon("as_ico_pause.png")
        get_icon.icons["pvc_tfirst"] = load_icon("as_ico_tfirst.png")
        get_icon.icons["pvc_tlast"] = load_icon("as_ico_tlast.png")
        get_icon.icons["pvc_probe"] = load_icon("as_ico_probe.png")
        get_icon.icons["pvc_plot"] = load_icon("as_ico_plot.png")
        get_icon.icons["pvc_rescale"] = load_icon("as_ico_rescale_bar.png")
        get_icon.icons["cb_sep"] = load_icon("as_ico_colorbar_sep.png")
        get_icon.icons["cb_insert"] = load_icon("as_ico_colorbar_insert.png")
        get_icon.icons["cb_remove"] = load_icon("as_ico_colorbar_remove.png")

    icon = None
    obj_type = get_node_type(obj)

    if obj_type == NodeType.History:
        icon = get_icon.icons["history"]
    elif obj_type == NodeType.Case:
        if obj.model:
            if obj is obj.model.current_case:
                icon = get_icon.icons["current_case"]
            elif obj in obj.model.backup_cases:
                icon = get_icon.icons["backup_case"]
            elif obj in obj.model.run_cases:
                icon = get_icon.icons["run_case"]
    elif obj_type == NodeType.Stage:
        is_graphical_stage = obj.is_graphical_mode()
        icon = get_icon.icons["stage_graph"] if is_graphical_stage \
            else get_icon.icons["stage_text"]
    elif obj_type == NodeType.Category:
        icon = get_icon.icons["category"]
    elif obj_type == NodeType.Command:
        command = obj.title.lower() + ".png"
        if command not in get_icon.icons:
            default = get_icon.icons["command"]
            get_icon.icons[command] = load_icon(command, default=default)
        icon = get_icon.icons[command]
    elif obj_type == NodeType.Variable:
        icon = get_icon.icons["variable"]
    elif obj_type == NodeType.Comment:
        icon = get_icon.icons["comment"]
    elif obj_type == NodeType.Macro:
        icon = get_icon.icons["macro"]
    elif obj_type == NodeType.Unit:
        icon = get_icon.icons["unit"]
    elif obj_type == NodeType.Dir:
        icon = get_icon.icons["dir"]
    elif obj_type == NodeType.Result:
        icon = get_icon.icons[obj.lower().replace(' ', '_')]

    return icon


def str2font(text):
    """
    Create font from text description.

    Arguments:
        text (str): Font string representation.

    Returns:
        QFont: Font.
    """
    font = Q.QFont()
    values = text.split(',')
    values = [i.strip() for i in values if i.strip()]
    if values:
        family = values[0]
        font = Q.QFont(family)
        for i in values[1:]:
            if i in ('bold',):
                font.setBold(True)
            elif i in ('italic',):
                font.setItalic(True)
            elif i in ('underline',):
                font.setUnderline(True)
            elif i in ('shadow', 'overline'):
                font.setOverline(True)
            else:
                size = to_type(i, int)
                if size is not None:
                    font.setPointSize(size)
    return font


class UrlHandler(Q.QObject):
    """
    Handler to open url in an external web browser or the default one.
    """

    @classmethod
    def open_url(cls, url):
        """Open an url in the external browser if it is configured or the
        native one otherwise.

        Arguments:
            url (QUrl): URL to open. Does nothing if it is null.
        """
        if not url:
            return
        browser = behavior().external_browser
        if browser:
            cmd = " ".join([browser, str(url), "&"])
            print("Executing: {}".format(cmd))
            call(cmd, shell=True)
        else:
            Q.QDesktopServices.openUrl(Q.QUrl(url))

Q.QDesktopServices.setUrlHandler("http", UrlHandler(), "open_url")

def clipboard_text():
    """
    Get text data from clipboard.

    Returns:
        str: Text data from clipboard.
    """
    text = ''
    clipboard = Q.QApplication.clipboard()
    if clipboard.mimeData(Q.QClipboard.Clipboard).hasText():
        text = clipboard.mimeData(Q.QClipboard.Clipboard).text()
    elif clipboard.mimeData(Q.QClipboard.Selection).hasText() \
            and behavior().treat_selection_buffer:
        text = clipboard.mimeData(Q.QClipboard.Selection).text()
    return text
