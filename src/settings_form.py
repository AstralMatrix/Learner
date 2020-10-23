import tkinter as tk
from tkinter import ttk
from tkinter import *
from settings import Settings
from file_reader import FileReader


INIT_SCREEN_SIZE: str = '500x500'  # Starting screen size.
MIN_SCREEN_SIZE: (int, int) = (500, 500)  # Minimum screen size.
SCREEN_TITLE: str = "Settings   "  # Window / Form title.

WHITE: str = '#FFFFFF'
LIGHT_GRAY: str = '#F0F0F0'
MEDIUM_GRAY: str = '#D0D0D0'

class SettingsForm(object):

    
    def __init__(self):
        self.form = tk.Tk()
        self.form.geometry(INIT_SCREEN_SIZE)
        self.form.minsize(MIN_SCREEN_SIZE[0], MIN_SCREEN_SIZE[1])
        self.form.title(SCREEN_TITLE)

        self.frame: Frame = Frame(self.form, background=LIGHT_GRAY)  # Create the main frame to hold all the elements.
        self.frame.pack(fill=BOTH, expand=1)  # Make the main frame fit the size of the window.

        self.create_widgets()


    def create_widgets(self):

        self.file_frame = Frame(self.frame, background=LIGHT_GRAY)
        self.file_frame.pack(fill=BOTH, expand=1, side=LEFT, padx=5, pady=5)

        self.active_files = Listbox(self.file_frame, relief=FLAT)
        self.active_files.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.active_files.insert(END, '       active       ')
        self.active_files.insert(END, '--------------------')

        self.file_button_frame = Frame(self.file_frame, background=LIGHT_GRAY)
        self.file_button_frame.pack(fill=BOTH, expand=0, padx=5, pady=5)

        self.activate_button = Button(self.file_button_frame, text='▲', relief=FLAT, background=MEDIUM_GRAY, command=self.activate_callback)
        self.activate_button.pack(fill=BOTH, expand=1, side=LEFT, padx=5, pady=5)

        self.disable_button = Button(self.file_button_frame, text='▼', relief=FLAT, background=MEDIUM_GRAY, command=self.disable_callback)
        self.disable_button.pack(fill=BOTH, expand=1, side=RIGHT, padx=5, pady=5)

        self.disabled_files = Listbox(self.file_frame, relief=FLAT)
        self.disabled_files.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.disabled_files.insert(END, '      disabled      ')
        self.disabled_files.insert(END, '--------------------')


        self.content_frame = Frame(self.frame, background=LIGHT_GRAY)
        self.content_frame.pack(fill=Y, expand=0, side=RIGHT, padx=5, pady=10)

        # ----- DIRECTORY SETTING -----
        self.directory_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.directory_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.directory_label = Label(self.directory_frame, text='Directory: ', font=('Verdana', 9), background=LIGHT_GRAY)
        self.directory_label.pack(side=LEFT)

        self.directory_input = Entry(self.directory_frame, text='null', font=('Verdana', 9), background=WHITE, relief=FLAT, width=21)
        self.directory_input.pack(side=LEFT)
        self.directory_input.insert(0, Settings.directory_path)
        self.directory_input.config(state=DISABLED)
        # ------------------------------

        # ----- FONT SIZE SETTING -----
        self.font_size_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.font_size_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.font_size_label = Label(self.font_size_frame, text='Font Size:', font=('Verdana', 9), background=LIGHT_GRAY)
        self.font_size_label.pack(side=LEFT, anchor=SW)

        self.font_size_input = Scale(self.font_size_frame, orient=HORIZONTAL, font=('Verdana', 9), background=WHITE, relief=FLAT, from_=4, to=140, sliderlength=20, resolution=4, length=175)
        self.font_size_input.pack(side=LEFT)
        self.font_size_input.set(Settings.font_size)
        # ------------------------------

        # ----- TYPEFACE SETTING -----
        self.typeface_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.typeface_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.typeface_label = Label(self.typeface_frame, text='Typeface: ', font=('Verdana', 9), background=LIGHT_GRAY)
        self.typeface_label.pack(side=LEFT)

        self.typeface_input = Entry(self.typeface_frame, text='Verdana', font=('Verdana', 9), width=17, background=WHITE, relief=FLAT)
        self.typeface_input.pack(side=LEFT)
        self.typeface_input.insert(0, Settings.typeface)
        # ------------------------------

        # ----- THEME SETTING -----
        self.theme_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.theme_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.theme_label = Label(self.theme_frame, text='Theme: ', font=('Verdana', 9), background=LIGHT_GRAY)
        self.theme_label.pack(side=LEFT)

        self.theme_input = Listbox(self.theme_frame, font=('Verdana', 9), background=WHITE, relief=FLAT, height=len(Settings.theme_names)+3)
        self.theme_input.pack(side=LEFT)
        self.theme_input.insert(END, 'current: ' + Settings.current_theme)
        self.theme_input.insert(END, '--------------------')
        for theme_name in Settings.theme_names:
            self.theme_input.insert(END, theme_name)
        self.theme_input.select_set(0)
        # ------------------------------

        # ----- ITEM RANGE -----
        self.display_item_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.display_item_frame.pack(fill=X, expand=0, side=TOP, padx=5, pady=10)

        self.display_item_label = Label(self.display_item_frame, text='Display Item: ', font=('Verdana', 9), background=LIGHT_GRAY)
        self.display_item_label.pack(side=LEFT)

        self.display_item_input = Entry(self.display_item_frame, text='idx', font=('Verdana', 9), width=6, background=WHITE, relief=FLAT)
        self.display_item_input.pack(side=LEFT)
        self.display_item_input.insert(0, Settings.display_item)
        # ------------------------------

        # ----- BUTTON FRAME -----
        self.button_frame = Frame(self.content_frame, background=LIGHT_GRAY)
        self.button_frame.pack(fill=X, expand=0, side=BOTTOM, padx=10, pady=10)
        # ------------------------------

        # ----- SAVE BUTTON -----
        self.save_button = Button(self.button_frame, text='Save & Quit', background=MEDIUM_GRAY, relief=FLAT, command=self.save_callback)
        self.save_button.pack(side=RIGHT, padx=3, pady=3)
        # ------------------------------

        # ----- CANCEL BUTTON -----
        self.cancel_button = Button(self.button_frame, text='Cancel', background=MEDIUM_GRAY, relief=FLAT, command=self.cancel_callback)
        self.cancel_button.pack(side=LEFT, padx=3, pady=3)
        # ------------------------------


    def cancel_callback(self) -> None:
        FileReader.load_settings()
        self.form.destroy()


    def save_callback(self) -> None:
        FileReader.save_settings()
        self.form.destroy()


    def activate_callback(self) -> None:
        print("activate")
        pass


    def disable_callback(self) -> None:
        print("disable")
        pass


    def update_settings(self) -> None:
        theme_name: str = str(self.theme_input.get(ACTIVE))
        if not theme_name in Settings.theme_names:
            theme_name = Settings.current_theme
        self.theme_input.delete(0)
        self.theme_input.insert(0, 'current: ' + Settings.current_theme)

        Settings.set_value({
            "font_size": self.font_size_input.get(),
            "typeface": self.typeface_input.get(),
            "current_theme": theme_name
            })


    def update(self):
        try:
            self.update_settings()
            self.form.update_idletasks()
            self.form.update()
        except TclError:  # The form has been destroyed (i.e. on exit)
            return None
        return self