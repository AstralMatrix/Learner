import tkinter as tk
from tkinter import *
from tkinter import messagebox
#from tkinter import BOTH, X, Y, N, S, E, W, FLAT, CENTER, WORD, DISABLED, LEFT, RIGHT, TOP, BOTTOM, NORMAL, END
from form_status import FormReturnStatus
from time import sleep
from grader import Grader
from theme import Theme, ThemeGroup
from queue import Queue
from threading import Timer
import exception


INIT_SCREEN_SIZE: str = '854x405'
MIN_SCREEN_SIZE: (int, int) = (400, 300)
SCREEN_TITLE: str = "Learner"
INITAL_MESSAGE: str = "Welcome!\nPress \"Begin\" to start"
PROGRESS_UNBLOCK_DURATION: int = 3000
RETURN_KEY: str = '<Return>'


class MainForm(object):

    def __init__(self):
        tk.Tk.report_callback_exception = exception.unhandled_error
        self.return_status: FormReturnStatus = FormReturnStatus.STOP

        self.grader: Grader = Grader(["../data/example.json"])

        self.form = tk.Tk()
        self.form.geometry(INIT_SCREEN_SIZE)
        self.form.minsize(MIN_SCREEN_SIZE[0], MIN_SCREEN_SIZE[1])
        self.form.title(SCREEN_TITLE)

        self.all_elements = []
        self.grading_color_elements = []

        self.theme: Theme = Theme((None,))

        self.frame = tk.Frame(self.form)  # Create a (main) frame on the screen to hold all the elements.
        self.frame.pack(fill=tk.BOTH, expand=1)  # Make the main frame fit the size of the window.
        self.all_elements.append(self.frame)  # Add the frame to all elements, since it is an element.
        self.theme.add_to_group(self.frame, ThemeGroup.MAIN_GROUP)

        self.is_reviewing = True
        self.progress_blocked = False
        self.display_item = 0

        self.scheduled_actions: Queue = Queue()

        self.font_style = "verdana"
        self.font_size = 44

        self.create_widgets()
        self.form.bind(RETURN_KEY, self.submit_callback)
        self.theme.set_theme_color()
        self.display(INITAL_MESSAGE)


    def create_widgets(self):
        '''Form Layout Hierarchy:

            Main Frame
            |
            |---Display Frame
            |   |---Display Box
            |   |
            |---Content Frame
            |   |
            |   |---Guess Frame
            |   |   |---Guess Label
            |   |   |---Guess Input
            |   |
            |   |---Button Frame
            |   |   |---Submit Button
            |   |   |---Settings Button
        '''

        self.display_frame = tk.Frame(self.frame)  # Create a frame to put the text display in.
        self.display_frame.pack(fill=BOTH, expand=1)  # Place the frame in the window.
        self.all_elements.append(self.display_frame)
        self.theme.add_to_group(self.display_frame, ThemeGroup.MAIN_GROUP)

        self.content_frame = tk.Frame(self.frame)  # Create a frame to put all the elements that are not the display.
        self.content_frame.pack(anchor=S, fill=X, expand=0)  # Make this frame fill just the bottom part of the screen it needs.
        self.all_elements.append(self.content_frame)
        self.theme.add_to_group(self.content_frame, ThemeGroup.MAIN_GROUP)

        self.guess_frame = tk.Frame(self.content_frame)  # Create a frame to hold the guess input line
        self.guess_frame.pack(fill=X, expand=1, padx=10, pady=10)  # Format the frame so it expands and had ample room.
        self.all_elements.append(self.guess_frame)
        self.theme.add_to_group(self.guess_frame, ThemeGroup.MAIN_GROUP)

        self.button_frame = tk.Frame(self.content_frame)  # Create a frame to hold the control buttons.
        self.button_frame.pack(fill=X, expand=1, padx=10, pady=10)  # Format the frame so it expands and had ample room.
        self.all_elements.append(self.button_frame)
        self.theme.add_to_group(self.button_frame, ThemeGroup.MAIN_GROUP)

        self.display_box = tk.Text(self.display_frame, font=(self.font_style, self.font_size), relief=FLAT, height=2)
        self.display_box.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.display_box.tag_config('f', justify=CENTER, wrap=WORD)
        self.display_box.config(state=DISABLED)
        self.all_elements.append(self.display_box)
        self.theme.add_to_group(self.display_box, ThemeGroup.TEXT_BOX_GROUP)

        self.guess_label = tk.Label(self.guess_frame, text='Answer:', font=(self.font_style, 12))
        self.guess_label.pack(side=LEFT)
        self.all_elements.append(self.guess_label)
        self.theme.add_to_group(self.guess_label, ThemeGroup.LABEL_GROUP)

        self.guess_input = tk.Entry(self.guess_frame, font=(self.font_style, 12), relief=FLAT)
        self.guess_input.pack(side=RIGHT, fill=X, expand=1, padx=5, pady=5)
        self.all_elements.append(self.guess_input)
        self.theme.add_to_group(self.guess_input, ThemeGroup.TEXT_BOX_GROUP)

        self.submit_button = tk.Button(self.button_frame, text='Begin', font=(self.font_style, 12), relief=FLAT, command=self.submit_callback)
        self.submit_button.pack(side=RIGHT, padx=3, pady=3)
        self.all_elements.append(self.submit_button)
        self.theme.add_to_group(self.submit_button, ThemeGroup.BUTTON_GROUP)

        self.settings_button = tk.Button(self.button_frame, text='Settings', font=(self.font_style, 12), relief=FLAT, command=self.settings_callback)
        self.settings_button.pack(side=LEFT, padx=3, pady=3)
        self.all_elements.append(self.settings_button)
        self.theme.add_to_group(self.settings_button, ThemeGroup.BUTTON_GROUP)


    def submit_callback(self, event=None):
        if self.is_reviewing:
            if not self.progress_blocked:
                self.next_question()
                self.is_reviewing = False
                self.theme.set_theme_color()
                self.guess_input.delete(0, END)      
                self.submit_button.config(text="Submit")
        else:
            response: str = self.guess_input.get()
            correct: bool = self.grader.check(response)
            if correct:
                self.answer_correct()
            else:
                self.answer_wrong()
                
            self.is_reviewing = True
            self.submit_button.config(text="Next")
            

    def settings_callback(self):
        messagebox.showwarning("not implemented", "not implemented: settings functionality has not yet been implemented")


    def next_question(self) -> None:
        self.grader.next()
        self.display(self.grader.get_display_question(self.display_item))

    
    def answer_correct(self) -> None:
        self.display(self.grader.get_display_answer())
        self.theme.set_correct_color()


    def answer_wrong(self) -> None:
        self.display(self.grader.get_display_answer())
        # Breifly flash the color of the screen.
        self.theme.set_incorrect_color()
        self.form.after(200, self.theme.set_theme_color)
        self.form.after(400, self.theme.set_incorrect_color)
        self.form.after(600, self.theme.set_theme_color)
        self.form.after(800, self.theme.set_incorrect_color)
        self.progress_blocked = True
        self.form.after(PROGRESS_UNBLOCK_DURATION, self.unblock_progress)
        # Unblock the progress after the unblock duration. This is done
        # by creating a thread that waits for the given duration, then
        # enqueues a call to the unblock method. That call will then
        # be dequeued and called by the main thread on the next update.
        '''Timer(PROGRESS_UNBLOCK_DURATION,
            lambda: self.scheduled_actions.put(
                lambda: self.unblock_progress()
            )
        ).start()'''


    def unblock_progress(self):
        self.progress_blocked = False


    def display(self, msg: str) -> None:
        self.display_box.config(state=NORMAL)  # Allow the display text box to be edited.
        self.display_box.delete(0.0, END)  # Remove all text from the beginning to the end of the lines in the text box.
        self.display_box.insert(END, msg, 'f')  # Add the text that the user wants to display to the text box.
        self.display_box.config(state=DISABLED)  # Lock the display text box so that it can't be edited.


    def restart(self) -> None:
        self.form.destroy()
        self.return_status = FormReturnStatus.RESTART


    def update(self) -> FormReturnStatus:
        ''' Update the form screen.

            This is used to update the screen every 'tick' when this
            function is called.
        '''
        try:
            if not self.scheduled_actions.empty():
                self.scheduled_actions.get()()  # Execute the scheduled function.
            self.form.update_idletasks()
            self.form.update()
        except tk.TclError:
            return self.return_status
        return FormReturnStatus.RUNNING