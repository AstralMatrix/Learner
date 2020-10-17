import logging
import traceback
from tkinter import messagebox


def _get_log():
    ''' create and return a log object '''
    log_handler = logging.FileHandler("log.txt")
    log = logging.getLogger()
    log.addHandler(log_handler)
    return log


def error(msg: str) -> None:
    ''' Log and display handled errors (i.e. file not found) '''
    log = _get_log()
    log.error("--- Logging error ---\nerror: {}".format(msg))
    print("error:", msg)
    messagebox.showerror("error", "error: {}".format(msg))


def unhandled_error(item, exc, val, tb) -> None:
    ''' Log and display unhandled errors (i.e. raised by tkinter) '''
    log = _get_log()
    exception = traceback.TracebackException(exc, val, tb)
    log.exception("--- Logging unhandled exception ---", exc_info=exception)
    print(exception)
    messagebox.showerror("unhandled exception", "error: an unhandled exception has occured <{}> please see log for more details".format(val))


