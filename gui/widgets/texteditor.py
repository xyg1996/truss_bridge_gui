

"""
Text editor
-----------

The module implements text editor that is used to edit Python code,
for example in Stage editor.

For more details refer to *TextEditor* class.

"""


from PyQt5 import Qt as Q

from ..prefmanager import completion_mode

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name



class BaseTextEditor:
    """Base object for different kinds of text editors."""

    def setCurrentLine(self, line):
        """
        Change current line number to the given one.

        Arguments:
            line (int): New current line number to be set.
        """
        # pylint: disable=no-member
        if hasattr(self.editor, "setCurrentLine"):
            self.editor.setCurrentLine(line)
        elif hasattr(self.editor, "document"):
            # set cursor to the given line in default editor
            cursor = Q.QTextCursor(
                self.editor.document().findBlockByLineNumber(line-1))
            self.editor.setTextCursor(cursor)


class TextEditor(Q.QWidget, BaseTextEditor):
    """
    Helper class implementing an editor of Stage in text mode.

    This class uses SALOME Python editor class for editing purpose if
    it is available; otherwise editor is represented by simple plain
    text editor.

    """

    textChanged = Q.pyqtSignal()
    """
    Signal: emitted when text is changed.
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        try:
            import PyEditorPy
            if hasattr(PyEditorPy, "PyEditor_Widget"):
                self.editor = PyEditorPy.PyEditor_Widget(self)
                self.editor.editor().setObjectName("text_editor")
            else:
                self.editor = PyEditorPy.PyEditor_Editor(self)
        except ImportError:
            self.editor = Q.QPlainTextEdit(self)
        self.editor.setObjectName("text_editor")
        v_layout = Q.QVBoxLayout(self)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(5)
        v_layout.addWidget(self.editor)
        self.editor.textChanged.connect(self.textChanged)
        self.setFocusProxy(self.editor)

    def text(self):
        """
        Get the edited text.

        Returns:
            str: Text from editor
        """
        return self.editor.text() if hasattr(self.editor, "text") \
            else self.editor.toPlainText()

    def setText(self, txt):
        """
        Sets the specified text into editor.

        Arguments:
            txt (str): Text for editor
        """
        if hasattr(self.editor, "setText"):
            self.editor.setText(txt)
        else:
            self.editor.setPlainText(txt)

    def setReadOnly(self, on):
        """
        Enable/disable read-only mode for the editor.

        Arguments:
            on (bool): Mode to be set.
        """
        self.editor.editor().setReadOnly(on)

    def setKeywords(self, keywords, group, color):
        """
        Set custom keywords for auto-completion feature.

        Arguments:
            keywords (list[str]): List of custom keywords.
            group (int): Group of keywords.
            color (QColor): Color of the keyword group.
        """
        if hasattr(self.editor, "appendKeywords"):
            self.editor.appendKeywords(keywords, group, color)

    @Q.pyqtSlot(object)
    def updateSettings(self, pref_mgr):
        """
        Called when preferences are changed.

        Arguments:
            pref_mgr (object): Application's preferences manager.
        """
        settings = self._settings()

        if settings is None or pref_mgr is None:
            return

        section = 'PyEditor/HighlightCurrentLine'
        default = settings.highlightCurrentLine()
        val = pref_mgr.bool_value(section, default)
        settings.setHighlightCurrentLine(val)

        section = 'PyEditor/TextWrapping'
        default = settings.textWrapping()
        val = pref_mgr.bool_value(section, default)
        settings.setTextWrapping(val)

        section = 'PyEditor/CenterCursorOnScroll'
        default = settings.centerCursorOnScroll()
        val = pref_mgr.bool_value(section, default)
        settings.setCenterCursorOnScroll(val)

        section = 'PyEditor/LineNumberArea'
        default = settings.lineNumberArea()
        val = pref_mgr.bool_value(section, default)
        settings.setLineNumberArea(val)

        section = 'PyEditor/VerticalEdge'
        default = settings.verticalEdge()
        val = pref_mgr.bool_value(section, default)
        settings.setVerticalEdge(val)

        section = 'PyEditor/NumberColumns'
        default = settings.numberColumns()
        val = pref_mgr.int_value(section, default)
        settings.setNumberColumns(val)

        section = 'PyEditor/TabSpaceVisible'
        default = settings.tabSpaceVisible()
        val = pref_mgr.bool_value(section, default)
        settings.setTabSpaceVisible(val)

        section = 'PyEditor/TabSize'
        default = settings.tabSize()
        val = pref_mgr.int_value(section, default)
        settings.setTabSize(val)

        section = 'PyEditor/Font'
        default = settings.font()
        val = pref_mgr.font_value(section, default)
        settings.setFont(val)

        if hasattr(settings, "completionPolicy"):
            section = 'PyEditor/CompletionPolicy'
            default = settings.completionPolicy()
            val = completion_mode(pref_mgr.str_value(section, str(default)))
            settings.setCompletionPolicy(val)

        self._setSettings(settings)

    def _settings(self):
        """
        Get editor's settings.

        Returns:
            PyEditor_Settings: Settings object.
        """
        if hasattr(self.editor, "settings"):
            return self.editor.settings()
        if hasattr(self.editor, "editor"):
            editor = self.editor.editor()
            if hasattr(self.editor, "settings"):
                return editor.settings()
        return None

    def _setSettings(self, settings):
        """
        Set editor's settings.

        Arguments:
            settings (PyEditor_Settings): Settings object.
        """
        if hasattr(self.editor, "setSettings"):
            self.editor.setSettings(settings)
        elif hasattr(self.editor, "editor"):
            editor = self.editor.editor()
            if hasattr(self.editor, "setSettings"):
                editor.setSettings(settings)
