import tkinter as tk
from tkinter import ttk
from tkinter import *
from settings import Settings
from file_reader import FileReader
import os
import os.path
from typing import List, Dict, Tuple

INIT_SCREEN_SIZE: str = '500x500'  # Starting screen size.
MIN_SCREEN_SIZE: (int, int) = (500, 500)  # Minimum screen size.
SCREEN_TITLE: str = "Settings"  # Window / Form title.

WHITE: str = '#FFFFFF'
LIGHT_GRAY: str = '#F0F0F0'
MEDIUM_GRAY: str = '#D0D0D0'

DEFAULT_FONT: Tuple[str, int] = ('Verdana', 9)
DEFAULT_WIDTH: int = 21
CURRENT_THEME_STR: str = 'current: {}'

class SettingsForm(object):

    
    def __init__(self):
        self.form = tk.Tk()
        self.form.geometry(INIT_SCREEN_SIZE)
        self.form.minsize(MIN_SCREEN_SIZE[0], MIN_SCREEN_SIZE[1])
        self.form.title(SCREEN_TITLE)

        # Store the last status of the directory path to determine if the
        # directory changed in order to update the file display boxes.
        self.last_dir_path: str = Settings.directory_path

        # Each file in the current directory is stored as the key of a
        # dictionary, with each key mapping to a bool of if that file
        # is enabled or not.
        self.all_files: Dict[str, bool] = {}
        self.load_all_files()

        self.frame: Frame = Frame(self.form, background=LIGHT_GRAY)  # Create the main frame to hold all the elements.
        self.frame.pack(fill=BOTH, expand=1)  # Make the main frame fit the size of the window.

        self.create_widgets()


    def create_widgets(self):
        '''Create all form elements, and populate the form. This should
            only be called once when the form is being created.'''

        '''Form Layout Hierarchy:

            Main Frame
            |---File Frame
            |   |---Active Files
            |   |---File Button Frame
            |   |   |---Activate Button
            |   |   |---Disable Button
            |   |---Disable Files
            |---Content Frame
            |   |---Directory Frame
            |   |   |---Directory Label
            |   |   |---Directory Input
            |   |---Font Size Frame
            |   |   |---Font Size Label
            |   |   |---Font Size Input
            |   |---Typeface Frame
            |   |   |---Typeface Label
            |   |   |---Typeface Input
            |   |---Theme Frame
            |   |   |---Theme Label
            |   |   |---Theme Input
            |   |---Display Item Frame
            |   |   |---Display Item Label
            |   |   |---Display Item Input
            |   |---Button Frame
            |   |   |---Save Button
            |   |   |---Cancel Button
        '''

        # ----- FILE SELECTOR -----
        self.file_frame = Frame(self.frame, background=LIGHT_GRAY)
        self.file_frame.pack(fill=BOTH, expand=1, side=LEFT, padx=5, pady=5)

        self.active_files = Listbox(self.file_frame, relief=FLAT)
        self.active_files.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.refresh_active_files()

        self.file_button_frame = Frame(self.file_frame, background=LIGHT_GRAY)
        self.file_button_frame.pack(fill=BOTH, expand=0, padx=5, pady=5)

        self.activate_button = Button(self.file_button_frame, text='▲', relief=FLAT, background=MEDIUM_GRAY, command=self.activate_callback)
        self.activate_button.pack(fill=BOTH, expand=1, side=LEFT, padx=5, pady=5)

        self.disable_button = Button(self.file_button_frame, text='▼', relief=FLAT, background=MEDIUM_GRAY, command=self.disable_callback)
        self.disable_button.pack(fill=BOTH, expand=1, side=RIGHT, padx=5, pady=5)

        self.disabled_files = Listbox(self.file_frame, relief=FLAT)
        self.disabled_files.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.refresh_disabled_files()
        #------------------------------

        self.content_frame = Frame(self.frame, background=LIGHT_GRAY)
        self.content_frame.pack(fill=Y, expand=0, side=RIGHT, padx=5, pady=10)

        # ----- DIRECTORY SETTING -----
        self.directory_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.directory_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.directory_label = Label(self.directory_frame, text='Directory: ', font=DEFAULT_FONT, background=LIGHT_GRAY)
        self.directory_label.pack(side=LEFT)

        self.directory_input = Entry(self.directory_frame, text='null', font=DEFAULT_FONT, background=WHITE, relief=FLAT, width=DEFAULT_WIDTH)
        self.directory_input.pack(side=LEFT)
        self.directory_input.insert(0, Settings.directory_path)
        # ------------------------------

        # ----- FONT SIZE SETTING -----
        self.font_size_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.font_size_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.font_size_label = Label(self.font_size_frame, text='Font Size:', font=DEFAULT_FONT, background=LIGHT_GRAY)
        self.font_size_label.pack(side=LEFT, anchor=SW)

        self.font_size_input = Scale(self.font_size_frame, orient=HORIZONTAL, font=DEFAULT_FONT, background=WHITE, relief=FLAT, from_=4, to=140, sliderlength=20, resolution=4, length=175)
        self.font_size_input.pack(side=LEFT)
        self.font_size_input.set(Settings.font_size)
        # ------------------------------

        # ----- TYPEFACE SETTING -----
        self.typeface_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.typeface_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.typeface_label = Label(self.typeface_frame, text='Typeface: ', font=DEFAULT_FONT, background=LIGHT_GRAY)
        self.typeface_label.pack(side=LEFT)

        self.typeface_input = Entry(self.typeface_frame, text='Verdana', font=DEFAULT_FONT, width=DEFAULT_WIDTH, background=WHITE, relief=FLAT)
        self.typeface_input.pack(side=LEFT)
        self.typeface_input.insert(0, Settings.typeface)
        # ------------------------------

        # ----- THEME SETTING -----
        self.theme_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.theme_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.theme_label = Label(self.theme_frame, text='Theme: ', font=DEFAULT_FONT, background=LIGHT_GRAY)
        self.theme_label.pack(side=LEFT)

        self.theme_input = Listbox(self.theme_frame, font=DEFAULT_FONT, background=WHITE, relief=FLAT, height=len(Settings.theme_names)+3, width=DEFAULT_WIDTH+2)
        self.theme_input.pack(side=LEFT)
        self.theme_input.insert(END, CURRENT_THEME_STR.format(Settings.current_theme))
        self.theme_input.insert(END, '')
        for theme_name in Settings.theme_names:
            self.theme_input.insert(END, theme_name)
        self.theme_input.select_set(0)
        # ------------------------------

        # ----- ITEM RANGE -----
        self.display_item_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.display_item_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.display_item_label = Label(self.display_item_frame, text='Display Item: ', font=DEFAULT_FONT, background=LIGHT_GRAY)
        self.display_item_label.pack(side=LEFT)

        self.display_item_input = Spinbox(self.display_item_frame, from_=-1, to=100, font=DEFAULT_FONT, width=DEFAULT_WIDTH-4, background=WHITE, relief=FLAT)
        self.display_item_input.pack(side=LEFT)
        self.display_item_input.delete(0, END)
        self.display_item_input.insert(0, Settings.display_item)
        # ------------------------------

        # ----- SAVE AND CANCEL BUTTONS -----
        self.button_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.button_frame.pack(fill=X, expand=0, side=BOTTOM, padx=10, pady=10)

        self.save_button = Button(self.button_frame, text='Save & Quit', background=MEDIUM_GRAY, relief=FLAT, command=self.save_callback)
        self.save_button.pack(side=RIGHT, padx=3, pady=3)

        self.cancel_button = Button(self.button_frame, text='Cancel', background=MEDIUM_GRAY, relief=FLAT, command=self.cancel_callback)
        self.cancel_button.pack(side=LEFT, padx=3, pady=3)
        # ------------------------------


    def cancel_callback(self) -> None:
        '''Restore the previous saved settings and close the form.'''
        FileReader.load_settings()
        self.form.destroy()


    def save_callback(self) -> None:
        '''Save the newly updated settings and close the form.'''
        FileReader.save_settings()
        self.form.destroy()
        

    def activate_callback(self) -> None:
        '''Takes the currently selected 'disabled' file and sets it to 'enabled'.'''
        file: str = str(self.disabled_files.get(ACTIVE))
        if file in self.all_files.keys():
            self.all_files[file] = True
        # Update the file display text boxes.
        self.refresh_active_files()
        self.refresh_disabled_files()


    def disable_callback(self) -> None:
        '''Takes the currently selected 'enabled' file and sets it to 'disabled'.'''
        file: str = str(self.active_files.get(ACTIVE))
        if file in self.all_files.keys():
            self.all_files[file] = False
        # Update the file display text boxes.
        self.refresh_active_files()
        self.refresh_disabled_files()

    
    def refresh_active_files(self) -> None:
        '''Clear and populate the active files text box with the currently active files.'''
        self.active_files.delete(0, END)
        self.active_files.insert(END, '       active       ')
        self.active_files.insert(END, '--------------------')
        for file in self.all_files.keys():
            if self.all_files[file]:  # File is active.
                self.active_files.insert(END, file)


    def refresh_disabled_files(self) -> None:
        '''Clear and populate the disabled files text box with the currently disabled files.'''
        self.disabled_files.delete(0, END)
        self.disabled_files.insert(END, '      disabled      ')
        self.disabled_files.insert(END, '--------------------')
        for file in self.all_files.keys():
            if not self.all_files[file]:  # File is disabled.
                self.disabled_files.insert(END, file)
        

    def load_all_files(self) -> None:
        '''Load all of the files from the current directory into self.all_files.
            This also sets the state if the files are active or disabled.'''
        dir_path: str = Settings.directory_path
        all_files: Dict[str, bool] = {}
        if os.path.exists(dir_path):
            # Loops through all files in the current directory.
            for file in [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]:
                is_active: bool = file in Settings.active_files
                all_files[file] = is_active  # Add new file (key) and activity status (value) to all_files dict.
        self.all_files = all_files


    def update_directory_path(self) -> str:
        '''Return the current directory in the directory input box.
            Update the current working files and file display boxes if
            a new directory was set.

            Returns:
                str: The directory path to be saved to the settings.
        '''
        new_dir_path: str = self.directory_input.get()
        # Update the current working files and file display boxes if the
        # directory changed. This is done to always display the files that
        # are in the current directory.
        if self.last_dir_path != Settings.directory_path:
            self.load_all_files()
            self.refresh_active_files()
            self.refresh_disabled_files()
            self.last_dir_path = Settings.directory_path
        # Set the last directory, then return the new directory to be
        # set the the settings. This makes it so that the elements update
        # from the conditional above. This is because the Settings will be
        # updated after this function returns.
        elif new_dir_path != Settings.directory_path:
            self.last_dir_path = Settings.directory_path
            return new_dir_path
        return Settings.directory_path


    def update_theme(self) -> str:
        '''Return the current theme in the theme input box. Use current
            theme if new theme isn't valid (i.e. title portion), and update
            the currenly selected theme in the input box.

            Returns:
                str: The name of the new theme to be saved to the settings.
        '''
        # Get the current selected theme from the Listbox. If the theme
        # is not valid, set it to the current theme so that a valid theme
        # is always used.
        theme_name: str = str(self.theme_input.get(ACTIVE))
        if not theme_name in Settings.theme_names: 
            theme_name = Settings.current_theme
        # Reset the first element of the Listbox which displays the current
        # theme, this shows the user the name of the theme that is currently
        # enabled. This also has the side effect of that element not being
        # able to be selected (which doesn't change anything).
        self.theme_input.delete(0)
        self.theme_input.insert(0, CURRENT_THEME_STR.format(Settings.current_theme))
                                   
        return theme_name


    def update_settings(self) -> None:
        '''Sets all of the current form values to the settings.'''
        dir_path: str = self.update_directory_path() # Get the current directory path.
        theme_name: str = self.update_theme() # Get the current theme name.
        active_files: List[str] = [f for f in self.all_files.keys() if self.all_files[f]] # Get all active files.

        # Update the setings to the new values.
        Settings.set_value({
            "directory_path": dir_path,
            "active_files": active_files,
            "display_item": 0,
            "font_size": self.font_size_input.get(),
            "typeface": self.typeface_input.get(),
            "current_theme": theme_name,
            })


    def update(self):
        ''' Update the form screen.

            This is used to update the screen and settings every 'tick'
            when this function is called.
        '''
        try:
            self.update_settings()
            self.form.update_idletasks()
            self.form.update()
        except TclError:  # The form has been destroyed (i.e. on exit)
            return None  # Return None so the main form knows this form is no longer active.
        return self  # Return itself so the main form knows this form is still active.
