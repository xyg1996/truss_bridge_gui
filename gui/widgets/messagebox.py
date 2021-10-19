

"""
Message Box
-----------

The module implements improved version of message box.

For more details refer to *MessageBox* class.

"""


from PyQt5 import Qt as Q

from ...common import translate

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class MessageBox(Q.QMessageBox):
    """
    Message box with extended static methods and 'Don't show' check box.

    Provides static methods for showing message boxex of standard types.
    Each method can get additional keyword arguments for message box
    properties: *detailedText*, *iconPixmap*, *informativeText*,
    *textFormat*, *textInteractionFlags*, etc.

    Additional keyword argument *noshow* is supported. This argument is
    used to specify name of the preference option that stores 'don't
    show' message box flag. It allows the user disabling message box
    displaying next time when it is supposed to be shown by checking a
    dedicated check box.
    """

    Ok = Q.QMessageBox.Ok
    Open = Q.QMessageBox.Open
    Save = Q.QMessageBox.Save
    Cancel = Q.QMessageBox.Cancel
    Close = Q.QMessageBox.Close
    Discard = Q.QMessageBox.Discard
    Apply = Q.QMessageBox.Apply
    Reset = Q.QMessageBox.Reset
    RestoreDefaults = Q.QMessageBox.RestoreDefaults
    Help = Q.QMessageBox.Help
    SaveAll = Q.QMessageBox.SaveAll
    Yes = Q.QMessageBox.Yes
    YesToAll = Q.QMessageBox.YesToAll
    No = Q.QMessageBox.No
    NoToAll = Q.QMessageBox.NoToAll
    Abort = Q.QMessageBox.Abort
    Retry = Q.QMessageBox.Retry
    Ignore = Q.QMessageBox.Ignore
    NoButton = Q.QMessageBox.NoButton

    InvalidRole = Q.QMessageBox.InvalidRole
    AcceptRole = Q.QMessageBox.AcceptRole
    RejectRole = Q.QMessageBox.RejectRole
    DestructiveRole = Q.QMessageBox.DestructiveRole
    ActionRole = Q.QMessageBox.ActionRole
    HelpRole = Q.QMessageBox.HelpRole
    YesRole = Q.QMessageBox.YesRole
    NoRole = Q.QMessageBox.NoRole
    ApplyRole = Q.QMessageBox.ApplyRole
    ResetRole = Q.QMessageBox.ResetRole

    NoIcon = Q.QMessageBox.NoIcon
    Question = Q.QMessageBox.Question
    Information = Q.QMessageBox.Information
    Warning = Q.QMessageBox.Warning
    Critical = Q.QMessageBox.Critical

    @classmethod
    def critical(cls, parent, title, text, buttons=Q.QMessageBox.Ok,
                 defaultButton=Q.QMessageBox.NoButton, **kwargs):
        """ Show critical message box. """
        return MessageBox._display(Q.QMessageBox.Critical, parent, title, text,
                                   buttons, defaultButton, **kwargs)

    @classmethod
    def information(cls, parent, title, text, buttons=Q.QMessageBox.Ok,
                    defaultButton=Q.QMessageBox.NoButton, **kwargs):
        """ Show information message box. """
        return MessageBox._display(Q.QMessageBox.Information, parent, title,
                                   text, buttons, defaultButton, **kwargs)

    @classmethod
    def question(cls, parent, title, text,
                 buttons=Q.QMessageBox.Yes|Q.QMessageBox.No,
                 defaultButton=Q.QMessageBox.NoButton, **kwargs):
        """ Show confirmation (question) message box. """
        return MessageBox._display(Q.QMessageBox.Question, parent, title, text,
                                   buttons, defaultButton, **kwargs)

    @classmethod
    def warning(cls, parent, title, text, buttons=Q.QMessageBox.Ok,
                defaultButton=Q.QMessageBox.NoButton, **kwargs):
        """ Show warning message box. """
        return MessageBox._display(Q.QMessageBox.Warning, parent, title, text,
                                   buttons, defaultButton, **kwargs)

    # pragma pylint: disable=too-many-branches,too-many-locals
    @classmethod
    def _display(cls, icon, parent, title, text,
                 buttons, defaultButton, **kwargs):
        """ Show message with specified icon box. """
        mbdisabled = False
        resbtn = Q.QMessageBox.NoButton
        notshow = kwargs['noshow'] if 'noshow' in kwargs else None
        prefmgr = kwargs['prefmgr'] if 'noshow' in kwargs else None
        if notshow is not None and prefmgr is not None:
            value = prefmgr.bool_value("msgbox_" + notshow, True)
            if not value:
                mbdisabled = True

        if mbdisabled:
            resbtn = defaultButton
            btntry = 1
            while (resbtn == Q.QMessageBox.NoButton and
                   btntry <= Q.QMessageBox.RestoreDefaults):
                if buttons & btntry == btntry:
                    resbtn = btntry
                btntry = btntry << 1
        else:
            msgbox = MessageBox(icon, title, text, buttons, parent)
            msgbox.setDefaultButton(defaultButton)

            if notshow is not None and prefmgr is not None:
                msg = translate("MessageBox",
                                "Don't show this message anymore.")
                msgbox.setCheckBox(Q.QCheckBox(msg, msgbox))

            propMap = {}
            for p in range(msgbox.metaObject().propertyCount()):
                propMap[msgbox.metaObject().property(p).name()] = 0

            for prop in kwargs:
                if prop in propMap:
                    msgbox.setProperty(prop, kwargs[prop])

            ovrcursor = Q.QApplication.overrideCursor() is not None
            if ovrcursor:
                Q.QApplication.setOverrideCursor(Q.Qt.ArrowCursor)
            resbtn = msgbox.exec_()
            if ovrcursor:
                Q.QApplication.restoreOverrideCursor()

            if prefmgr is not None and msgbox.checkBox() is not None and \
                    msgbox.checkBox().isChecked():
                prefmgr.setValue("msgbox_" + notshow, False)

        return resbtn
