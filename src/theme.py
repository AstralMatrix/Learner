from enum import Enum


DEFAULT_THEME_COLOR = ('#F0F0F0', '#D0D0D0', '#FFFFFF', '#000000', '#008000', '#B22222')

class Theme(object):

    def __init__(self, theme_colors: tuple):
        theme_colors = DEFAULT_THEME_COLOR
        self.__colors: dict = {
            ThemeColor.MAIN_COLOR: theme_colors[0],
            ThemeColor.SECONDARY_COLOR: theme_colors[1],
            ThemeColor.BACK_COLOR: theme_colors[2],
            ThemeColor.TEXT_COLOR: theme_colors[3],
            ThemeColor.CORRECT_COLOR: theme_colors[4],
            ThemeColor.INCORRECT_COLOR: theme_colors[5]
        }
        self.__item_groups: dict = {
            ThemeGroup.MAIN_GROUP: [],
            ThemeGroup.BUTTON_GROUP: [],
            ThemeGroup.LABEL_GROUP: [],
            ThemeGroup.TEXT_BOX_GROUP: []
        }


    def add_to_group(self, item, group: 'ThemeGroup') -> None:
        self.__item_groups[group].append(item)


    def set_theme_color(self) -> None:
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
        for key in self.__item_groups.keys():
            for elem in self.__item_groups[key]:

                if key is ThemeGroup.MAIN_GROUP:
                    elem.config(background=self.__colors[ThemeColor.CORRECT_COLOR])

                elif key is ThemeGroup.LABEL_GROUP:
                    elem.config(background=self.__colors[ThemeColor.CORRECT_COLOR])


    def set_incorrect_color(self) -> None:
        for key in self.__item_groups.keys():
            for elem in self.__item_groups[key]:

                if key is ThemeGroup.MAIN_GROUP:
                    elem.config(background=self.__colors[ThemeColor.INCORRECT_COLOR])

                elif key is ThemeGroup.LABEL_GROUP:
                    elem.config(background=self.__colors[ThemeColor.INCORRECT_COLOR])


class ThemeGroup(Enum):
    MAIN_GROUP: str = "main_group"
    BUTTON_GROUP: str = "button_group"
    LABEL_GROUP: str = "label_group"
    TEXT_BOX_GROUP: str = "text_box_group"


class ThemeColor(Enum):
    MAIN_COLOR: str = "main_color"
    SECONDARY_COLOR: str = "secondary_color"
    BACK_COLOR: str = "back_color"
    TEXT_COLOR: str = "text_color"
    CORRECT_COLOR: str = "correct_color"
    INCORRECT_COLOR: str = "incorrect_color"