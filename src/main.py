from main_form import MainForm
from form_status import FormReturnStatus
import logging


def main_loop() -> None:

    while True:
        main_form: MainForm = MainForm()
        form_status: FormReturnStatus = FormReturnStatus.RUNNING

        while form_status is FormReturnStatus.RUNNING:
            form_status = main_form.update()
        
        if form_status is FormReturnStatus.RESTART:
            main_form = MainForm()
        else:
            break


if __name__ == '__main__':

    try:
        main_loop()
    except Exception as e:
        log_handler = logging.FileHandler("log.txt")
        log = logging.getLogger()
        log.addHandler(log_handler)
        log.exception("unhandled exception:")
        print("error: {}".format(e))
