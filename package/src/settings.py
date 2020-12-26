"""TODO: INSERT DOCSTRING."""
from typing import List
import os.path
import json

from package.src.exception import error


# The relative path to the settings json file.
SETTINGS_PATH: str = "package/src/settings.json"


class Settings:
    """TODO: INSERT DOCSTRING."""

    # The raw data from when the settings are loaded. This is kept, so
    # that the settings can be easily exported to json by just updating
    # the dict to the new values before exporting. This also allows data
    # checks to be skipped for items in the settings file that aren't
    # fully loaded in (i.e. the list of themes) while keeping them present
    # after the settings are exported and saved.
    __raw_data: dict = {}
    directory_path: str = 'data/'  # Path to the data files.
    active_files: List[str] = []  # All data files that are active.
    # Segment of the DataObject to display as the question
    display_item: int = 0
    font_size: int = 44  # Current font size.
    typeface: str = 'Verdana'  # Current font.
    # Current theme key for the themes in the settings file.
    current_theme: str = "Default"
    theme_names: List[str] = []
    # The current theme colors.
    theme_colors: List[str] = ['#F0F0F0', '#D0D0D0', '#FFFFFF', '#000000',
                               '#008000', '#B22222']

    @staticmethod
    def load_from(data: dict) -> None:
        """Set all of the settings values from the provided data.

        This should be used when loading settings from a file.

        Data verification checks are preformed on every item before
        setting their values. These ensure the data is in the correct
        format and won't throw exceptions later when the values are
        used. This is used to combat invalid changes to the settings.json
        file. An error message is logged and displayed any time a
        verification check fails, and the default value is used.

        Args:
            data (dict): The data that contains each of the different
                settings values.

        Returns:
            None
        """
        if not isinstance(data, dict):
            error("settings can not load from type {}, must be type 'dict'"
                  .format(type(data)))
            return
        Settings.__raw_data = data

        # Verify and set the new directory path. Ensure the new directory
        # path is a string and that the file path exists.
        new_directory_path: str = data.get("directory_path", None)
        if new_directory_path is not None and \
           isinstance(new_directory_path, str) and \
           os.path.exists(new_directory_path):
            Settings.directory_path = new_directory_path
        else:
            error(("settings unable to load directory path, ensure the path "
                   "exists. expected type 'str', got {}")
                  .format(type(new_directory_path)))

        # Verify and set the new active files list. Ensure the data is
        # a list, and that every item in it is a string.
        new_active_files: List[str] = data.get("active_files", None)
        if new_active_files is not None and \
           isinstance(new_active_files, list):
            is_valid: bool = True
            for item in new_active_files:
                if not isinstance(item, str):
                    is_valid = False
            if is_valid:
                Settings.active_files = new_active_files
            else:
                error("settings unable to load active files, list contents "
                      "contained a type that was not a 'str'")
        else:
            error(("settings unable to load active files, expected type "
                   "'list', got {}").format(type(new_active_files)))

        # Verify and set the new display item. Ensure the display item is an
        # integer.
        new_display_item: int = data.get("display_item", None)
        if new_display_item is not None and \
           isinstance(new_display_item, int):
            Settings.display_item = new_display_item
        else:
            error(("settings unable to load display item, expected type "
                   "'int', got {}").format(type(new_display_item)))

        # Verify and set the new font size. Ensure the font size is an integer.
        new_font_size: int = data.get("font_size", None)
        if new_font_size is not None and \
           isinstance(new_font_size, int):
            Settings.font_size = new_font_size
        else:
            error(("settings unable to load font size, expected type 'int', "
                   "got {}").format(type(new_font_size)))

        # Verify and set the new typeface. Ensure the typeface is an integer.
        new_typeface: str = data.get("typeface", None)
        if new_typeface is not None and \
           isinstance(new_typeface, str):
            Settings.typeface = new_typeface
        else:
            error(("settings unable to load typeface, expected type 'str', "
                   "got {}").format(type(new_typeface)))

        # Retrieve the key for the current theme to be loaded.
        theme_colors_key: str = data.get("current_theme", "")
        Settings.current_theme = theme_colors_key
        # Verify and set the new theme colors. Ensure the theme colors
        # is a list of exactly 6 elements (one for each color), and that
        # every element of the list is a valid hex color starting with
        # a '#'. The colors are formatted like so: '#xxxxxx' where each
        # 'x' is a hex value.
        new_theme_colors: List[str] = \
            data.get("all_themes", None).get(theme_colors_key, None)
        if new_theme_colors is not None and \
           isinstance(new_theme_colors, list) and \
           len(new_theme_colors) == 6:
            is_valid = True
            for item in new_theme_colors:
                if isinstance(item, str):
                    if len(item) != 7 or \
                       item[0] != '#':
                        is_valid = False
                    valid_chars: List[str] = [
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                        'B', 'C', 'D', 'E', 'F']
                    for char in item[1:]:
                        if not char.upper() in valid_chars:
                            is_valid = False
                else:
                    is_valid = False
            if is_valid:
                Settings.theme_colors = new_theme_colors
            else:
                error("settings unable to load theme colors, list contents "
                      "contained value that is not a valid color")
        else:
            error(("settings unable to load theme colors, expected type "
                   "'list' with len(6), got {}")
                  .format(type(new_theme_colors)))

        theme_dict: dict = data.get("all_themes", None)
        Settings.theme_names = []  # Prevent duplicate names from being created
        if theme_dict is not None and \
           isinstance(theme_dict, dict):
            for key in theme_dict.keys():
                if key is not None and \
                   isinstance(key, str):
                    Settings.theme_names.append(key)
                else:
                    error(("settings unable to theme name, expected type "
                           "'str', got {}").format(type(key)))
        else:
            error(("settings unable to load theme names, expected type "
                   "'dict', got {}").format(type(theme_dict)))

    @staticmethod
    def set_value(update_data: dict):
        """TODO: INSERT DOCSTRING."""
        for key in update_data.keys():
            if key == "directory_path":
                Settings.directory_path = update_data.get(key, None)
            elif key == "active_files":
                Settings.active_files = update_data.get(key, None)
            elif key == "display_item":
                Settings.display_item = update_data.get(key, None)
            elif key == "font_size":
                Settings.font_size = update_data.get(key, None)
            elif key == "typeface":
                Settings.typeface = update_data.get(key, None)
            elif key == "current_theme":
                Settings.current_theme = update_data.get(key, None)
                Settings.theme_colors = (
                    Settings.__raw_data.get("all_themes", None)
                    .get(Settings.current_theme))

    @staticmethod
    def as_json() -> str:
        """Convert the settings into a json string that can be saved to a file.

        Returns:
            str: The json string.
        """
        # Update the values in __raw_data to their current value. This
        # updates them if they have been changed, then convert the data
        # to a json string.
        ret_data: dict = Settings.__raw_data
        ret_data["directory_path"] = Settings.directory_path
        ret_data["active_files"] = Settings.active_files
        ret_data["display_item"] = Settings.display_item
        ret_data["font_size"] = Settings.font_size
        ret_data["typeface"] = Settings.typeface
        ret_data["current_theme"] = Settings.current_theme
        return json.dumps(ret_data, indent=4)
