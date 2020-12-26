"""TODO: INSERT DOCSTRING."""
import tkinter as tk
from tkinter import Frame, Button, Label, TOP, BOTTOM, BOTH, TclError, CENTER
from typing import Tuple
from time import sleep


INIT_SCREEN_SIZE: str = '700x300'  # Starting screen size.
MIN_SCREEN_SIZE: Tuple[int, int] = (700, 300)  # Minimum screen size.

WHITE: str = '#FFFFFF'
BLACK: str = '#000000'
LIGHT_GRAY: str = '#F0F0F0'
MEDIUM_GRAY: str = '#D0D0D0'

DEFAULT_FONT: Tuple[str, int] = ('', 14)
DEFAULT_FONT_SMALL: Tuple[str, int] = (DEFAULT_FONT[0], DEFAULT_FONT[1] - 4)
DEFAULT_WIDTH: int = 21
CURRENT_THEME_STR: str = 'current: {}'


class PopupForm:
    """TODO: INSERT DOCSTRING."""

    def __init__(self, title: str, msg_type: str, msg: str):
        """TODO: INSERT DOCSTRING."""
        self.form = tk.Tk()
        self.form.geometry(INIT_SCREEN_SIZE)
        self.form.minsize(MIN_SCREEN_SIZE[0], MIN_SCREEN_SIZE[1])
        self.form.title(title)

        # Create the main frame to hold all the elements.
        self.frame: Frame = Frame(self.form, background=WHITE)
        # Make the main frame fit the size of the window.
        self.frame.pack(fill=BOTH, expand=True)

        self.close_button = Button(
            self.frame, text='Close', font=DEFAULT_FONT_SMALL,
            command=self.close_callback, background=MEDIUM_GRAY,
            foreground=BLACK)
        self.close_button.pack(side=BOTTOM, padx=10, pady=10)

        self.msg_type_label = Label(
            self.frame, text=msg_type, font=DEFAULT_FONT, background=WHITE,
            foreground=BLACK)
        self.msg_type_label.pack(side=TOP, padx=20, pady=20)

        self.msg_label = Label(
            self.frame, text=msg, font=DEFAULT_FONT, background=WHITE,
            foreground=BLACK, justify=CENTER, wraplength=MIN_SCREEN_SIZE[0])
        self.msg_label.pack(side=TOP)

    def close_callback(self):
        """TODO: INSERT DOCSTRING."""
        self.form.destroy()

    def update(self):
        """TODO: INSERT DOCSTRING."""
        try:
            self.form.update_idletasks()
            self.form.update()
            self.form.lift()
        except TclError:  # The form has been destroyed (i.e. on exit)
            # Return None so the updater knows this form is no longer active.
            return None
        # Return itself so the updater knows this form is still active.
        return self

    @staticmethod
    def create_popup(title: str, msg_type: str, msg: str):
        """TODO: INSERT DOCSTRING."""
        popup: PopupForm = PopupForm(title, msg_type, msg)
        while popup is not None:
            popup = popup.update()
            sleep(0.1)  # Prevent excessive CPU usage.
