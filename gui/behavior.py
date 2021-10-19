


#


"""
Behavior controller
-------------------

This module implements *Behavior* class that allows controlling behavior
of the *AsterStudy* application.

"""


import os

from ..common import to_type

__all__ = ["Behavior", "behavior"]

# pragma pylint: disable=attribute-defined-outside-init
# pragma pylint: disable=invalid-name
# pragma pylint: disable=too-many-instance-attributes


class Props(dict):
    """Custom properties storage."""

    def __getattr__(self, name):
        """Wrapper for `getattr()` function."""
        return self.get(name)

    def __setattr__(self, name, value):
        """Wrapper for `setattr()` function."""
        self[name] = value

    @property
    def forced_native_names(self):
        """
        bool: Attribute that is set to *True* when native *code_aster*
        catalogue's names are forced from either command line or
        environment variable *ASTERSTUDY_NATIVE_NAMES*.
        If it is *True*, actual value of corresponding option can be
        get via *force_native_names* attribute.
        """
        return self.force_native_names is not None

    @property
    def use_native_names(self):
        """
        bool: Attribute that holds value opposing to
        'use_business_translations' attribute, i.e
        *use_native_names* = not *use_business_translations*.
        """
        return not self.use_business_translations

    @property
    def used_lang(self):
        """
        bool: Attribute that holds the currently used language for
        documentation which is the application language or that choosen by
        the user.
        """
        language = self.doc_language
        if language == 'application':
            language = 'fr' if self.language == 'fr' else 'en'
        return language


class Behavior:
    """Class that controls behavior of *AsterStudy* application."""

    singleton = None

    def __init__(self):
        """
        Create and initialize behavior.

        `Behavior` instance is initialized by `AsterGui`.
        """
        if Behavior.singleton is not None:
            raise RuntimeError("Behavior has been already initialized")
        Behavior.singleton = self

        self.props = Props()

        self.props.no_mesh_view = \
            to_type(os.getenv("ASTERSTUDY_NO_MESH_VIEW"), int)
        self.props.force_native_names = \
            to_type(os.getenv("ASTERSTUDY_NATIVE_NAMES"), int)
        self.props.editor_use_unicode = True

        self.props.study_extension = 'ajs'
        self.props.comm_extension = 'comm'
        self.props.comm_file_mask = 'com?*'
        self.props.export_extension = 'export'

        self.props.embedded_message_link = False
        self.props.process_message_dblclick = True
        self.props.show_separators_in_combobox = False

        self.props.show_mesh_view = True
        self.props.mesh_view_handle_selection = True

        self.props.treat_selection_buffer = False

        self.props.preferences_colors = False

        self.props.summary_use_resizable_list = True
        self.props.summary_elide_category = True
        self.props.recalculate_usages_visibility = True

        self.props.title_button_size = 16

        self.from_preferences()

    def from_preferences(self):
        """Initialize behavior from user's Preferences."""

        pref_mgr = self.preferencesMgr() # pragma pylint: disable=no-member

        self.props.code_aster_version = \
            pref_mgr.value("code_aster_version")
        self.props.use_external_editor_stage = \
            pref_mgr.bool_value("use_external_editor_stage")
        self.props.use_external_editor_data_file = \
            pref_mgr.bool_value("use_external_editor_data_file")
        self.props.use_external_editor_msg_file = \
            pref_mgr.bool_value("use_external_editor_msg_file")
        self.props.external_editor = \
            pref_mgr.value("external_editor")
        self.props.external_browser = \
            pref_mgr.value("ExternalBrowser/application")
        self.props.language = pref_mgr.value("language/language") or \
            pref_mgr.value("language")
        self.props.doc_language = \
            pref_mgr.value("doc_language")
        self.props.toolbar_button_style = \
            pref_mgr.value("toolbar_button_style")
        self.props.workspace_tab_position = \
            pref_mgr.value("workspace_tab_position")
        self.props.strict_import_mode = \
            pref_mgr.bool_value("strict_import_mode")
        self.props.nblines_limit = \
            pref_mgr.int_value("nblines_limit")
        self.props.msgbox_convert_invalid_graphic_stage = \
            pref_mgr.bool_value("msgbox_convert_invalid_graphic_stage")
        self.props.msgbox_delete = \
            pref_mgr.bool_value("msgbox_delete")
        self.props.msgbox_delete_case = \
            pref_mgr.bool_value("msgbox_delete_case")
        self.props.msgbox_delete_stages = \
            pref_mgr.bool_value("msgbox_delete_stages")
        self.props.msgbox_parampanel_abort = \
            pref_mgr.bool_value("msgbox_parampanel_abort")
        self.props.msgbox_parampanel_close = \
            pref_mgr.bool_value("msgbox_parampanel_close")
        self.props.msgbox_undefined_files = \
            pref_mgr.bool_value("msgbox_undefined_files")
        self.props.show_selector_value = \
            pref_mgr.bool_value("show_selector_value")
        self.props.sort_selector_values = \
            pref_mgr.bool_value("sort_selector_values")
        self.props.allow_delete_cases = \
            pref_mgr.bool_value("allow_delete_cases")
        self.props.use_business_translations = \
            pref_mgr.bool_value("use_business_translations")
        self.props.disable_undo_redo = \
            pref_mgr.bool_value("disable_undo_redo")
        self.props.connect_servers_init = \
            pref_mgr.bool_value("connect_servers_init")
        self.props.sort_stages = \
            pref_mgr.bool_value("sort_stages")
        self.props.show_related_concepts = \
            pref_mgr.bool_value("show_related_concepts")
        self.props.show_catalogue_name = \
            pref_mgr.bool_value("show_catalogue_name")
        self.props.show_comments = \
            pref_mgr.bool_value("show_comments")
        self.props.auto_edit = \
            pref_mgr.bool_value("auto_edit")
        self.props.show_readonly_banner = \
            pref_mgr.bool_value("show_readonly_banner")
        self.props.content_mode = \
            pref_mgr.value("content_mode")
        self.props.external_list = \
            pref_mgr.bool_value("external_list")
        self.props.show_catalogue_name_in_selectors = \
            pref_mgr.bool_value("show_catalogue_name_in_selectors")
        self.props.auto_hide_search = \
            pref_mgr.bool_value("auto_hide_search")
        self.props.file_size_limit = \
            pref_mgr.int_value("file_size_limit")
        self.props.join_similar_files = \
            pref_mgr.bool_value("join_similar_files")
        self.props.grp_global_cmd = \
            pref_mgr.bool_value("grp_global_cmd")
        self.props.show_catalogue_name_data_files = \
            pref_mgr.bool_value("show_catalogue_name_data_files")
        self.props.no_type_in_selectors = \
            pref_mgr.bool_value("no_type_in_selectors")
        self.props.favorites_first = \
            pref_mgr.bool_value("favorites_first")
        self.props.workspace_initial_view = \
            pref_mgr.value("workspace_initial_view")
        self.props.rename_on_copy = \
            pref_mgr.bool_value("rename_on_copy")
        self.props.dashboard_use_logger = \
            pref_mgr.bool_value("dashboard_use_logger")
        self.props.show_categories = \
            pref_mgr.bool_value("show_categories")
        self.props.auto_expand = \
            pref_mgr.bool_value("auto_expand")
        self.props.reuse_buttons = \
            pref_mgr.bool_value("reuse_buttons")
        self.props.summary_chunk = \
            pref_mgr.int_value("summary_chunk")


def behavior():
    """
    Get access to Behavior's singleton instance.

    Returns:
        Behavior: Single instance of behavior.
    """
    if Behavior.singleton is None:
        raise RuntimeError("Behavior is not initialized")
    return Behavior.singleton.props
