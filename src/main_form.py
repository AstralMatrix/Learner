import tkinter as tk
from tkinter import *
from tkinter import messagebox
from form_status import FormReturnStatus
from time import sleep
from grader import Grader
from theme import Theme, ThemeGroup
from queue import Queue
from threading import Timer
import exception
from settings import Settings
from settings_form import SettingsForm


INIT_SCREEN_SIZE: str = '854x405'  # Starting screen size.
MIN_SCREEN_SIZE: (int, int) = (400, 300)  # Minimum screen size.
SCREEN_TITLE: str = "Learner"  # Window / Form title.
INITAL_MESSAGE: str = "Welcome!\nPress \"Begin\" to start"  # Message when user starts program.
PROGRESS_UNBLOCK_DURATION: int = 3000  # Wait time in ms before progress unlocks upon a wrong answer.
RETURN_KEY: str = '<Return>'  # Return key. Key bound to submit button.
FIXED_ELEMENT_FONT_SIZE = 12  # Font size of all fixed font size ui elements.


class MainForm(object):


    def __init__(self):
        # Set the exception callback to handle any of the exceptions
        # that are raised.
        tk.Tk.report_callback_exception = exception.unhandled_error
        # Set what the program will do when closed (stop / restart).
        self.return_status: FormReturnStatus = FormReturnStatus.STOP

        # Load all of the 'quiz' elements.
        self.grader: Grader = Grader(Settings.active_files)

        # Set form values from the settings.
        self.font_style: str = Settings.typeface
        self.font_size: int = Settings.font_size
        self.display_item: int = Settings.display_item  # The segment of the data objects to display.
        self.theme: Theme = Theme()

        self.settings_form: SettingsForm = None
        # Tracks if the settings form has closed. If so preform singe action
        # updates, such as updating the Grader, this is to limit number
        # of unnessicary file reads.
        self.update_after_settings_finish: bool = False
                
        # Create the main form and configure it.
        self.form = tk.Tk()
        self.form.geometry(INIT_SCREEN_SIZE)
        self.form.minsize(MIN_SCREEN_SIZE[0], MIN_SCREEN_SIZE[1])
        self.form.title(SCREEN_TITLE)

        self.frame: Frame = Frame(self.form)  # Create the main frame to hold all the elements.
        self.frame.pack(fill=BOTH, expand=1)  # Make the main frame fit the size of the window.
        self.theme.add_to_group(self.frame, ThemeGroup.MAIN_GROUP)

        # Tracks if the user is in the review state (i.e. looking at the anwser)
        self.is_reviewing: bool = True
        # Tracks if the user is allowed to move on. This is activated
        # for a short time when the user gets a question wrong. This
        # allows them time to review the correct answer, and prevents
        # them from accidentaly skipping it.
        self.progress_blocked: bool = False

        # A queue that other threads can store function calls to be
        # executed by the main thread on a form update.
        self.scheduled_actions: Queue = Queue()

        self.create_widgets()  # Populate the form.
        # Set the 'Enter' key to activate the submit button so the user
        # can submit using the keyboard.
        self.form.bind(RETURN_KEY, self.submit_callback)
        self.theme.set_theme_color()  # Theme the form.
        self.display(INITAL_MESSAGE)  # Show the user the welcome message.


    def refresh_settings(self) -> None:
        '''Update all elements with varying settings. This makes it so the
            form doesn't need to be reset to apply settings, and settings
            changes can be viewed live as they are made.'''
        self.display_item = Settings.display_item  # The segment of the data objects to display.
        self.font_size = Settings.font_size
        self.font_style = Settings.typeface
        self.display_box.config(font=(self.font_style, self.font_size))
        self.theme.update_colors()
        self.theme.set_theme_color()


    def create_widgets(self) -> None:
        '''Create all form elements, and populate the form. This should
            only be called once when the form is being created.'''

        '''Form Layout Hierarchy:

            Main Frame
            |---Display Frame
            |   |---Display Box
            |---Content Frame
            |   |---Guess Frame
            |   |   |---Guess Label
            |   |   |---Guess Input
            |   |---Button Frame
            |   |   |---Submit Button
            |   |   |---Settings Button
        '''
        DEFAULT_FIXED_FONT: tuple = (self.font_style, FIXED_ELEMENT_FONT_SIZE)

        self.display_frame = Frame(self.frame)  # Create a frame to put the text display in.
        self.display_frame.pack(fill=BOTH, expand=1)  # Expand it to the size of the main frame.
        self.theme.add_to_group(self.display_frame, ThemeGroup.MAIN_GROUP)

        self.content_frame = Frame(self.frame)  # Create a frame to put all the elements that are not the display (i.e. the inputs).
        self.content_frame.pack(anchor=S, fill=X, expand=0)  # Make this frame fill just the bottom part of the screen it needs.
        self.theme.add_to_group(self.content_frame, ThemeGroup.MAIN_GROUP)

        self.guess_frame = Frame(self.content_frame)  # Create a frame to hold the guess input line.
        self.guess_frame.pack(fill=X, expand=1, padx=10, pady=10)  # Format the frame so it expands and has ample room.
        self.theme.add_to_group(self.guess_frame, ThemeGroup.MAIN_GROUP)

        self.button_frame = Frame(self.content_frame)  # Create a frame to hold the control buttons.
        self.button_frame.pack(fill=X, expand=1, padx=10, pady=10)  # Format the frame so it expands and has ample room.
        self.theme.add_to_group(self.button_frame, ThemeGroup.MAIN_GROUP)

        # Create the text box to display the questions and answers.
        self.display_box = Text(self.display_frame, font=(self.font_style, self.font_size), relief=FLAT, height=2)
        self.display_box.pack(fill=BOTH, expand=1, padx=5, pady=5)  # Fill the frame, leaving a small space around the edge.
        self.display_box.tag_config('f', justify=CENTER, wrap=WORD)
        # Disable the text box, since it is the display and should not
        # be edited by the user.
        self.display_box.config(state=DISABLED)
        self.theme.add_to_group(self.display_box, ThemeGroup.TEXT_BOX_GROUP)

        # Create the text the precedes the guess input box.
        self.guess_label = Label(self.guess_frame, text='Answer:', font=DEFAULT_FIXED_FONT)
        self.guess_label.pack(side=LEFT)
        self.theme.add_to_group(self.guess_label, ThemeGroup.LABEL_GROUP)

        # Create the input box where the user inputs their anwsers.
        self.guess_input = Entry(self.guess_frame, font=DEFAULT_FIXED_FONT, relief=FLAT)
        self.guess_input.pack(side=RIGHT, fill=X, expand=1, padx=5, pady=5)  # Expand the input box along the width of the frame.
        self.theme.add_to_group(self.guess_input, ThemeGroup.TEXT_BOX_GROUP)

        # Create the button for the user to submit their answer.
        self.submit_button = Button(self.button_frame, text='Begin', font=DEFAULT_FIXED_FONT,
                                    relief=FLAT, command=self.submit_callback)
        self.submit_button.pack(side=RIGHT, padx=3, pady=3)
        self.theme.add_to_group(self.submit_button, ThemeGroup.BUTTON_GROUP)

        # Create the button to open the settings window.
        self.settings_button = Button(self.button_frame, text='Settings', font=DEFAULT_FIXED_FONT,
                                      relief=FLAT, command=self.settings_callback)
        self.settings_button.pack(side=LEFT, padx=3, pady=3)
        self.theme.add_to_group(self.settings_button, ThemeGroup.BUTTON_GROUP)


    def submit_callback(self, event=None):
        '''Callback function for the 'submit' button. This callback controls
            grading the response and changing the form's state.'''

        if self.is_reviewing:  # Move on to the next question, displaying it to the user.
            if not self.progress_blocked:
                self.next_question()
                self.is_reviewing = False
                self.theme.set_theme_color()
                self.guess_input.delete(0, END)      
                self.submit_button.config(text="Submit")

        else:  # Get the user's answer and grade it.
            response: str = self.guess_input.get()
            correct: bool = self.grader.check(response)
            if correct:
                self.answer_correct()
            else:
                self.answer_wrong()
            
            self.is_reviewing = True  # The user is now reviewing the answer.
            self.submit_button.config(text="Next")
            

    def settings_callback(self):
        '''Callback function for the 'settings' button. This callback controls
            the settings window.'''
        if self.settings_form is None:
            self.settings_form = SettingsForm()


    def next_question(self) -> None:
        '''Move on to the next question, displaying it.'''
        self.grader.next()
        self.display(self.grader.get_display_question(self.display_item))

    
    def answer_correct(self) -> None:
        '''The answer was correct, display it and set the 'correct' color.'''
        self.display(self.grader.get_display_answer())
        self.theme.set_correct_color()


    def answer_wrong(self) -> None:
        '''The answer was wrong, display the correct answer and set the
            'incorrect' color, flashing the screen breifly.'''
        self.display(self.grader.get_display_answer())
        # Breifly flash the color of the screen.
        self.theme.set_incorrect_color()
        self.form.after(200, self.theme.set_theme_color)
        self.form.after(400, self.theme.set_incorrect_color)
        self.form.after(600, self.theme.set_theme_color)
        self.form.after(800, self.theme.set_incorrect_color)
        # Prevent the user from moving on too quickly and skipping over
        # the correct answer. This forces them to review for a breif period.
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
        '''Unlock the progress, allowing the user to move on after reviewing.'''
        self.progress_blocked = False


    def display(self, msg: str) -> None:
        '''Display a message string to the display text box.'''
        self.display_box.config(state=NORMAL)  # Allow the display text box to be edited.
        self.display_box.delete(0.0, END)  # Remove all text from the beginning to the end of the lines in the text box.
        self.display_box.insert(END, msg, 'f')  # Add the text that the user wants to display to the text box.
        self.display_box.config(state=DISABLED)  # Lock the display text box so that it can't be edited.


    def restart(self) -> None:
        '''Restart the form.'''
        self.form.destroy()
        self.return_status = FormReturnStatus.RESTART


    def update(self) -> FormReturnStatus:
        ''' Update the form screen.

            This is used to update the screen every 'tick' when this
            function is called.
        '''
        try:
            if self.settings_form is not None:
                self.settings_form = self.settings_form.update()
                self.refresh_settings()
                self.update_after_settings_finish = True
            elif self.update_after_settings_finish:
                # Only update the grader after the settings form has closed
                # since it reads data files to get it's data, and we want to
                # limit file reading as much as possible. That's why this isn't
                # in refresh_settings.
                self.grader = Grader(Settings.active_files)
                self.display("Settings updated questions")
                # Set that the user is reviewing, so the next question is
                # not automatically wrong when they hit the next button
                # directly after changing the settings (updating the grader).
                # This lets them view the next question as normal.
                self.is_reviewing = True
                self.update_after_settings_finish = False

            if not self.scheduled_actions.empty():
                self.scheduled_actions.get()()  # Execute the scheduled function.
            self.form.update_idletasks()
            self.form.update()
        except TclError:  # The form has been destroyed (i.e. on restart)
            return self.return_status
        return FormReturnStatus.RUNNING