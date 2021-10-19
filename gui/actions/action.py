


#


"""
Generic action
--------------

The module implements generic action class for AsterStudy application.

For more details, see *Action* class.

"""


from PyQt5 import Qt as Q

from ...common import update_visibility

__all__ = ["Action"]

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


class Action(Q.QAction):
    """
    Generic action class that automatically updates visibility of
    toolbars and menus where it is inserted.
    """

    def __init__(self, text, parent):
        """
        Create action.

        Arguments:
            text (str): Action's text.
            parent (QObject): Parent object.
        """
        super().__init__(text, parent)
        self.changed.connect(self._changed)

    @Q.pyqtSlot()
    def _changed(self):
        """
        Called when action is changed.

        Updates related widgets.
        """
        for widget in self.associatedWidgets():
            update_visibility(widget)
