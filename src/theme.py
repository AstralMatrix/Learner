from enum import Enum
from settings import Settings
from typing import List


class Theme(object):


    def __init__(self):
        self.__colors: dict = None  # Store each color for the theme.
        self.update_colors()  # Set the colors upon loading.

        # Stores tkinter form items to their respective color grouping
        # so that they are colored properly.
        self.__item_groups: dict = {
            ThemeGroup.MAIN_GROUP: [],
            ThemeGroup.BUTTON_GROUP: [],
            ThemeGroup.LABEL_GROUP: [],
            ThemeGroup.TEXT_BOX_GROUP: []
        }


    def update_colors(self) -> None:
        '''Sets the current theme colors from the colors saved in the settings.'''
        theme_colors: List[str] = Settings.theme_colors
        self.__colors = {
            ThemeColor.MAIN_COLOR: theme_colors[0],
            ThemeColor.SECONDARY_COLOR: theme_colors[1],
            ThemeColor.BACK_COLOR: theme_colors[2],
            ThemeColor.TEXT_COLOR: theme_colors[3],
            ThemeColor.CORRECT_COLOR: theme_colors[4],
            ThemeColor.INCORRECT_COLOR: theme_colors[5]
        }


    def add_to_group(self, item, group: 'ThemeGroup') -> None:
        '''Adds a tkinter form element to a color grouping.

            Args:
                item: The tkinter element to be grouped.
                group (ThemeGroup): The group the object belongs to.
        '''
        self.__item_groups[group].append(item)


    def set_theme_color(self) -> None:
        '''Sets the normal theme coloring to all grouped elements.

            Each group is colored specially to fit the theme. This is also
            to reset the color after the color has been changed to a grading
            color.
        '''
        # Iterate through all the grouped elements, applying the specific
        # coloring required for each individual group.
        for key in self.__item_groups.keys():
            for elem in self.__item_groups[key]:
                if key is ThemeGroup.MAIN_GROUP:
                    elem.config(background=self.__colors[ThemeColor.MAIN_COLOR])
                elif key is ThemeGroup.BUTTON_GROUP:
                    elem.config(background=self.__colors[ThemeColor.SECONDARY_COLOR])
                    elem.config(foreground=self.__colors[ThemeColor.TEXT_COLOR])
                elif key is ThemeGroup.LABEL_GROUP:
                    elem.config(background=self.__colors[ThemeColor.MAIN_COLOR])
                    elem.config(foreground=self.__colors[ThemeColor.TEXT_COLOR])
                elif key is ThemeGroup.TEXT_BOX_GROUP:
                    elem.config(background=self.__colors[ThemeColor.BACK_COLOR])
                    elem.config(foreground=self.__colors[ThemeColor.TEXT_COLOR])                


    def set_correct_color(self) -> None:
        '''Sets the 'correct' grading color to the elements that display it.'''
        # Iterate through all the grouped elements, applying the specific
        # coloring required for each individual group.
        for key in self.__item_groups.keys():
            for elem in self.__item_groups[key]:
                if key is ThemeGroup.MAIN_GROUP:
                    elem.config(background=self.__colors[ThemeColor.CORRECT_COLOR])
                elif key is ThemeGroup.LABEL_GROUP:
                    elem.config(background=self.__colors[ThemeColor.CORRECT_COLOR])


    def set_incorrect_color(self) -> None:
        '''Sets the 'incorrect' grading color to the elements that display it.'''
        # Iterate through all the grouped elements, applying the specific
        # coloring required for each individual group.
        for key in self.__item_groups.keys():
            for elem in self.__item_groups[key]:
                if key is ThemeGroup.MAIN_GROUP:
                    elem.config(background=self.__colors[ThemeColor.INCORRECT_COLOR])
                elif key is ThemeGroup.LABEL_GROUP:
                    elem.config(background=self.__colors[ThemeColor.INCORRECT_COLOR])


class ThemeGroup(Enum):
    '''Enum for the different coloring groups that any given element can
        be colored as in the given theme.'''
    MAIN_GROUP: str = "main_group"
    BUTTON_GROUP: str = "button_group"
    LABEL_GROUP: str = "label_group"
    TEXT_BOX_GROUP: str = "text_box_group"


class ThemeColor(Enum):
    '''Enum for each of the different colors in the given theme.'''
    MAIN_COLOR: str = "main_color"
    SECONDARY_COLOR: str = "secondary_color"
    BACK_COLOR: str = "back_color"
    TEXT_COLOR: str = "text_color"
    CORRECT_COLOR: str = "correct_color"
    INCORRECT_COLOR: str = "incorrect_color"
