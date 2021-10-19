

"""
Dialog
------

The module implements general purpose dialog box with set of buttons.

For more details refer to *Dialog* class.

"""


import os
import os.path as osp

from PyQt5 import Qt as Q

from .. import behavior

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class Dialog(Q.QDialog):
    """
    Generic dialog box with set of buttons.

    By default, only *OK* and *Cancel* buttons are shown. Additional
    buttons can be inserted with *addStandardButton()* or *addButton()*
    methods.

    Child widgets can be put into either of the following parts:

    - Top-level *frame* widget which has vertical layout;
    - Tab widget (shown in the upper part of *frame*); by default tab
      widget is hidden. New tabs can be added by `addTab()` method.
    - *Main* widet (shown under the tab widget); does not have any
      layout.
    """

    def __init__(self, parent=None, modal=True):
        """
        Create dialog.

        Arguments:
            parent (Optional[QWidget]): Parent widget. Defaults to
                *None*.
            modal (Optional[bool]): Dialog's modality: *True* for modal
                dialog; *False* for modeless one. Defaults to *True*.
        """
        super().__init__(parent)
        self.setModal(modal)

        self._buttons = {}

        self._frame = Q.QWidget(self)
        self._frame.setObjectName("Dialog_frame")
        self._tab = Q.QTabWidget(self._frame)
        self._tab.setObjectName("Dialog_tab")
        self._main = Q.QWidget(self)
        self._main.setObjectName("Dialog_main")

        self._buttonbox = Q.QDialogButtonBox(Q.Qt.Horizontal, self)
        buttons = Q.QDialogButtonBox.Ok | Q.QDialogButtonBox.Cancel
        self.setStandardButtons(buttons)

        v_layout = Q.QVBoxLayout(self._frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.addWidget(self._tab)
        v_layout.addWidget(self._main)

        v_layout = Q.QVBoxLayout(self)
        v_layout.addWidget(self._frame)
        v_layout.addWidget(self._buttonbox)

        self._tab.hide()

        self.okButton().clicked.connect(self.accept)
        self.cancelButton().clicked.connect(self.reject)

    def frame(self):
        """
        Get central frame widget.

        Central widget is a top-level that contains all other child
        widgets including tab page widget (hidden by default) and
        *main* widget.

        Returns:
            QWidget: Top-level central widget of the dialog.
        """
        return self._frame

    def tabWidget(self):
        """
        Get tab widget.

        Returns:
            QTabWidget: Tab widget which is the part of central area.
        """
        return self._tab

    def main(self):
        """
        Get main widget.

        Returns:
            QWidget: Main widget which is the part of central area.
        """
        return self._main

    def addTab(self, title):
        """
        Add tab page with given *title* to the central area.

        Arguments:
            title (str): Tab's title.

        Returns:
            QWidget: Tab page widget.
        """
        tab = Q.QWidget()
        tab.setContentsMargins(9, 9, 9, 9)
        self._tab.addTab(tab, title)
        self._tab.show()
        return tab

    def tab(self, tab):
        """
        Get tab page.

        Arguments:
            tab (int, str): Page's index or title.

        Returns:
            QWidget: Tab page widget; *None* if page is not found.
        """
        if isinstance(tab, int):
            return self._tab.widget(tab)

        page = [self.tab(i) for i in range(self._tab.count()) \
                     if self._tab.tabText(i) == tab]
        return page[0] if page else None

    def setStandardButtons(self, buttons):
        """
        Set standard buttons to dialog.

        Arguments:
            buttons (QDialogButtonBox.StandardButtons): Buttons.
        """
        self._buttonbox.setStandardButtons(buttons)

    def addStandardButton(self, button):
        """
        Add standard button.

        Arguments:
            button (QDialogButtonBox.StandardButton): Button UID.

        Returns:
            QPushButton: Button (*None* if UID is invalid).
        """
        return self._buttonbox.addButton(button)

    def addButton(self, title, role=Q.QDialogButtonBox.ActionRole):
        """
        Add custom button.

        Arguments:
            title (str): Button's title.
            role (Optional[QDialogButtonBox.ButtonRole]): Button's role.
                Defaults to *QDialogButtonBox.ActionRole*.

        Returns:
            QPushButton: Button.
        """
        button = self._buttonbox.addButton(title, role)
        idx = -(len(self._buttons) + 1)
        self._buttons[idx] = button
        return button

    def buttonId(self, button):
        """
        Get custom button's UID.

        Arguments:
            button (QPushButton): Button.

        Returns:
            int: Button UID (*None* if button is not found).
        """
        buttons = [i for i in self._buttons if self._buttons[i] == button]
        custom_button = buttons[0] if buttons else None
        std_button = self._buttonbox.standardButton(button)
        if std_button == Q.QDialogButtonBox.NoButton:
            std_button = None
        return custom_button or std_button

    def button(self, button):
        """
        Get button by its UID.

        Arguments:
            button (int): Button UID (it may be
                QDialogButtonBox.StandardButton or negative integer for
                custom button).

        Returns:
            button (QPushButton): Button (*None* if button is not found).
        """
        return self._buttons.get(button) or self._buttonbox.button(button)

    def okButton(self):
        """
        Get *OK* button.

        Returns:
            QPushButton: *OK* button.
        """
        return self.button(Q.QDialogButtonBox.Ok)

    def cancelButton(self):
        """
        Get *Cancel* button.

        Returns:
            QPushButton: *Cancel* button.
        """
        return self.button(Q.QDialogButtonBox.Cancel)

    @Q.pyqtSlot()
    def accept(self):
        """Close dialog box with *Accepted* status."""
        super().accept()
        self.close()

    @Q.pyqtSlot()
    def reject(self):
        """Close dialog box with *Rejected* status."""
        super().reject()
        self.close()


class TestnameDialog(Dialog):
    """Simple dialog to enter a testcase name.
    """

    def __init__(self, astergui, title, label):
        """
        Create dialog.

        Arguments:
            astergui (AsterGui): Parent AsterGui instance.
        """
        parent = astergui.mainWindow()
        Dialog.__init__(self, parent)
        self.setWindowTitle(title)

        label = Q.QLabel(label, parent)
        label.setObjectName("TestnameDlg_label")
        self.editor = Q.QLineEdit(parent)
        self.editor.setObjectName("TestnameDlg_edit")
        layout = Q.QGridLayout(self.main())
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.editor, 0, 1)
        self.editor.setFocus()

        study = astergui.study()
        if study is not None:
            tests_path = study.history.tests_path
            if osp.isdir(tests_path):
                ext = '.{}'.format(behavior().export_extension)
                files = [i for i in os.listdir(tests_path) if osp.splitext(i)[-1] in (ext,)]
                files = [osp.splitext(i)[0] for i in files]
                self.editor.setCompleter(Q.QCompleter(sorted(files)))


    @staticmethod
    def execute(astergui, title, label):
        """
        Show *Testname* dialog.

        Arguments:
            astergui (AsterGui): Parent AsterGui instance.

        Returns:
            str: Testcase name enter by the user.
        """
        testname = ""
        dlg = TestnameDialog(astergui, title, label)
        if dlg.exec_():
            testname = dlg.editor.text()
        return testname
