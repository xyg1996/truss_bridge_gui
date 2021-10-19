


#


"""
Preferences management
----------------------

Implementation of preferences manager for AsterStudy standalone GUI.

TODO:
    Manage *subst* parameter (see `PreferencesMgr.str_value()`).

"""


import os
from contextlib import contextmanager

from PyQt5 import Qt as Q

from ..common import CFG, to_type

# note: the following pragma is added to prevent pylint complaining
#       about functions that follow Qt naming conventions;
#       it should go after all global functions
# pragma pylint: disable=invalid-name


@contextmanager
def ignore_user_values(pref_mgr, ignore=True):
    """Context manager to ignore user's preferences."""
    old_value = pref_mgr.IGNORE_USER_VALUES
    pref_mgr.IGNORE_USER_VALUES = ignore
    yield pref_mgr
    pref_mgr.IGNORE_USER_VALUES = old_value


class PreferencesMgr(Q.QSettings):
    """Preferences manager for standalone GUI."""

    IGNORE_USER_VALUES = False

    def __init__(self):
        """
        Create preferences manager.
        """
        super().__init__()
        self._settings = [Q.QSettings(CFG.apprc, Q.QSettings.IniFormat)]
        if os.getenv("AsterStudyConfig"):
            config_dirs = os.getenv("AsterStudyConfig").split(os.pathsep)
            config_dirs.reverse()
            for path in [i for i in config_dirs if i]:
                config_file = os.path.join(path, "AsterStudy.conf")
                if os.path.exists(config_file):
                    extra_settings = Q.QSettings(config_file,
                                                 Q.QSettings.IniFormat)
                    self._settings[0:0] = [extra_settings]

    def contains(self, key):
        """
        Check preference option's existence.
        Re-implemented from *QSettings* class.

        Arguments:
            key (str): Option's name.

        Returns:
            bool: *True* if an option is "known" to preferences manager;
            *False* otherwise.
        """
        key = self._convertKey(key)
        if not self.IGNORE_USER_VALUES:
            if super().contains(key):
                return True
        for i in self._settings:
            if i.contains(key):
                return True
        return False

    def setValue(self, key, value):
        """
        Set preference option's value.
        Re-implemented from *QSettings* class.

        Arguments:
            key (str): Option's name.
            value (any). Option's value.
        """
        key = self._convertKey(key)
        super().setValue(key, value)

    def value(self, key, default=None, **kwargs):
        """
        Get preference option's value.
        Re-implemented from *QSettings* class.

        Arguments:
            key (str): Option's name.
            default (Optional[any]). Default value for the option.
                Defaults to None.
            **kwargs: Keywords arguments.

        Returns:
            any: Option's value (string value by default; the result
            type can be requested via the `type` parameter).
        """
        key = self._convertKey(key)
        if not self.IGNORE_USER_VALUES:
            if super().contains(key):
                return super().value(key, default, **kwargs)
        for i in self._settings:
            if i.contains(key):
                return i.value(key, default, **kwargs)
        return default

    def int_value(self, key, default=0):
        """
        Get preference option's value as an integer.

        Arguments:
            key (str): Option's name.
            default (Optional[int]). Default value for the option.
                Defaults to 0.

        Returns:
            int: Option's value.
        """
        return self.value(key, default, type=int)

    def float_value(self, key, default=.0):
        """
        Get preference option's value as a float.

        Arguments:
            key (str): Option's name.
            default (Optional[float]). Default value for the option.
                Defaults to 0.0.

        Returns:
            float: Option's value.
        """
        return self.value(key, default, type=float)

    def bool_value(self, key, default=False):
        """
        Get preference option's value as a boolean.

        Arguments:
            key (str): Option's name.
            default (Optional[bool]). Default value for the option.
                Defaults to *False*.

        Returns:
            bool: Option's value.
        """
        return self.value(key, default, type=bool)

    # pragma pylint: disable=unused-argument
    def str_value(self, key, default="", subst=True):
        """
        Get preference option's value as a string.

        Arguments:
            key (str): Option's name.
            default (Optional[str]). Default value for the option.
                Defaults to empty string.
            subst (Optional[bool]). Flag specifying if it's necessary to
                perform auto-substitution of variables. Defaults to
                *True*.

        Returns:
            str: Option's value.

        TODO:
            Manage *subst* parameter.
        """
        return self.value(key, default, type=str)

    def font_value(self, key, default=Q.QFont()):
        """
        Get preference option's value as *QFont*.

        Arguments:
            key (str): Option's name.
            default (Optional[QFont]). Default value for the option.
                Defaults to null font.

        Returns:
            QFont: Option's value.
        """
        return self.value(key, default, type=Q.QFont)

    def color_value(self, key, default=Q.QColor()):
        """
        Get preference option's value as *QColor*.

        Arguments:
            key (str): Option's name.
            default (Optional[QColor]). Default value for the option.
                Defaults to null color.

        Returns:
            QColor: Option's value.
        """
        return self.value(key, default, type=Q.QColor)

    @staticmethod
    def _convertKey(key):
        """Convert option to lowercase."""
        separator = '/'
        values = key.split(separator)
        values[-1] = values[-1].lower()
        return separator.join(values)


def toolbar_style(label):
    """
    Get type of the toolbar buttons style by label.

    Arguments:
        label (str): Toolbar style's label (preference identifier).

    Returns:
        Qt.ToolButtonStyle: Toolbar style enumerator.
    """
    styles = {"icon_only" : Q.Qt.ToolButtonIconOnly,
              "text_only" : Q.Qt.ToolButtonTextOnly,
              "text_beside_icon": Q.Qt.ToolButtonTextBesideIcon,
              "text_under_icon": Q.Qt.ToolButtonTextUnderIcon,
              "follow_style" : Q.Qt.ToolButtonFollowStyle}
    return styles.get(label, Q.Qt.ToolButtonFollowStyle)


def tab_position(label):
    """
    Get type of the tab pages position by label.

    Arguments:
        label (str): Tab pages position's label (preference identifier).

    Returns:
        QTabWidget.TabPosition: Tab pages position enumerator.
    """
    positions = {"north" : Q.QTabWidget.North,
                 "south" : Q.QTabWidget.South,
                 "west" : Q.QTabWidget.West,
                 "east" : Q.QTabWidget.East}
    return positions.get(label, Q.QTabWidget.West)


def completion_mode(label):
    """
    Get type of the completion mode by label.

    Arguments:
        label (str): Completion mode label (preference identifier).

    Returns:
        int: Completion mode enumerator.
    """
    modes = {"none" : 0, "auto" : 1, "manual" : 2, "always" : 3}
    default = to_type(label, int)
    default = default if default in modes.values() else 3
    return modes.get(label, default)
