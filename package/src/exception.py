"""TODO: INSERT DOCSTRING."""
import traceback
import logging
from tkinter import messagebox

from package.src.pop_up import PopupForm

# Used to notify the other forms if an exception form exists so they can
# block their callbacks.
exception_form_exists = False


def _get_log():
    """Create and return a log object."""
    log_handler = logging.FileHandler("log.txt")
    log = logging.getLogger()
    log.addHandler(log_handler)
    return log


def error(msg: str) -> None:
    """Log and display handled errors (i.e. file not found)."""
    log = _get_log()
    log.warning("--- Logging warning ---\nwarning: %s", msg)
    print("warning:", msg)
    global exception_form_exists
    exception_form_exists = True
    PopupForm.create_popup("Notice", "Notice: ", msg)
    exception_form_exists = False


def unhandled_error(item, exc, val, tb) -> None:
    """Log and display unhandled errors (i.e. raised by tkinter)."""
    del item  # 'item' is not used in logging but required for the callback.
    log = _get_log()
    exception = traceback.TracebackException(exc, val, tb)
    log.exception("--- Logging unhandled exception ---", exc_info=exception)
    print(exception)
    messagebox.showerror("unhandled exception", "error: an unhandled \
        exception has occured <{}> see log for more details".format(val))


def form_exists() -> bool:
    """Return if a excpetion form currently exists."""
    return exception_form_exists
