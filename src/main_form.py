import tkinter as tk
from tkinter import BOTH, X, Y, N, S, E, W, FLAT, CENTER, WORD, DISABLED, LEFT, RIGHT, TOP, BOTTOM
from form_status import FormReturnStatus
from time import sleep
from grader import Grader


INIT_SCREEN_SIZE: str = '854x405'
MIN_SCREEN_SIZE: (int, int) = (400, 200)
SCREEN_TITLE: str = "Learner"


class MainForm(object):

    def __init__(self):
        self.return_status: FormReturnStatus = FormReturnStatus.STOP

        self.grader: Grader = Grader(["../data/example.json"])

        self.form = tk.Tk()
        self.form.geometry(INIT_SCREEN_SIZE)
        self.form.minsize(MIN_SCREEN_SIZE[0], MIN_SCREEN_SIZE[1])
        self.form.title(SCREEN_TITLE)

        self.all_elements = []

        self.frame = tk.Frame(self.form)  # Create a (main) frame on the screen to hold all the elements.
        self.frame.pack(fill=tk.BOTH, expand=1)  # Make the main frame fit the size of the window.
        self.all_elements.append(self.frame)  # Add the frame to all elements, since it is an element.

        self.font_style = "verdana"
        self.font_size = 12

        self.create_widgets()


    def create_widgets(self):

        self.display_frame = tk.Frame(self.frame)  # Create a frame to put the text display in.
        self.display_frame.pack(fill=BOTH, expand=1)  # Place the frame in the window.
        self.all_elements.append(self.display_frame)  # Add the frame to the array of all the elements.

        self.content_frame = tk.Frame(self.frame)  # Create a frame to put all the elements that are not the display.
        self.content_frame.pack(anchor=S, fill=X, expand=1)  # Make this frame fill the entire bottom half of the screen
        self.all_elements.append(self.content_frame)  # Add the frame to the array of all the elements.

        self.guess_frame = tk.Frame(self.content_frame)  # Create a frame to hold the guess input line
        self.guess_frame.pack(fill=X, expand=1, padx=10, pady=10)  # Format the frame so it expands and had ample room.
        self.all_elements.append(self.guess_frame)  # Add the frame to the array of all the elements.

        self.button_frame = tk.Frame(self.content_frame)  # Create a frame to hold the control button.
        self.button_frame.pack(fill=X, expand=1, padx=10, pady=10)  # Format the frame so it expands and had ample room.
        self.all_elements.append(self.button_frame)  # Add the frame to the array of all the elements.

        self.display_box = tk.Text(self.display_frame, font=(self.font_style, self.font_size), relief=FLAT, height=2)
        self.display_box.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.display_box.tag_config('f', justify=CENTER, wrap=WORD)
        self.display_box.config(state=DISABLED)
        self.all_elements.append(self.display_box)

        self.guess_label = tk.Label(self.guess_frame, text='Answer:', font=(self.font_style, 12))
        self.guess_label.pack(side=LEFT)
        self.all_elements.append(self.guess_label)

        self.guess_input = tk.Entry(self.guess_frame, font=(self.font_style, 12), relief=FLAT)
        self.guess_input.pack(side=RIGHT, fill=X, expand=1, padx=5, pady=5)
        self.all_elements.append(self.guess_input)

        self.submit_button = tk.Button(self.button_frame, text='Begin', font=(self.font_style, 12), relief=FLAT, command=self.submit_callback)
        self.submit_button.pack(side=RIGHT, padx=3, pady=3)
        self.all_elements.append(self.submit_button)

        self.settings_button = tk.Button(self.button_frame, text='Settings', font=(self.font_style, 12), relief=FLAT, command=self.settings_callback)
        self.settings_button.pack(side=LEFT, padx=3, pady=3)
        self.all_elements.append(self.settings_button)


    def submit_callback(self):
        correct: bool = self.grader.check(self.guess_input.get())
        if correct:
            print("correct")
            self.grader.next()
            print(self.grader.display)
        else:
            print("wrong")
            print(self.grader.display)


    def settings_callback(self):
        pass


    def restart(self) -> None:
        self.form.destroy()
        self.return_status = FormReturnStatus.RESTART

    def update(self) -> FormReturnStatus:
        ''' Update the form screen.

            This is used to update the screen every 'tick' when this
            function is called.
        '''
        try:
            self.form.update_idletasks()
            self.form.update()
        except tk.TclError:
            return self.return_status
        return FormReturnStatus.RUNNING