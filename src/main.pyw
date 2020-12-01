"""TODO: INSERT DOCSTRING."""
from main_form import MainForm
from main_form import FormReturnStatus
import logging
from tkinter import messagebox
from file_reader import FileReader


def main_loop() -> None:
    """TODO: INSERT DOCSTRING."""
    while True:
        FileReader.load_settings()
        main_form: MainForm = MainForm()
        form_status: FormReturnStatus = FormReturnStatus.RUNNING

        while form_status is FormReturnStatus.RUNNING:
            form_status = main_form.update()

        if form_status is FormReturnStatus.RESTART:
            continue
        break


if __name__ == '__main__':

    try:
        main_loop()
    except Exception as e:
        log_handler = logging.FileHandler("log.txt")
        log = logging.getLogger()
        log.addHandler(log_handler)
        log.exception("--- Logging unhandled exception ---")
        print("error: {}".format(e))
        messagebox.showerror(
            "unhandled exception",
            ("error: an unhandled exception has occured <{}> see log for more "
             "details").format(e))
