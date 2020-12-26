"""TODO: INSERT DOCSTRING."""
import traceback
import logging
from tkinter import messagebox


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
    messagebox.showwarning("warning", "warning: {}".format(msg))


def unhandled_error(item, exc, val, tb) -> None:
    """Log and display unhandled errors (i.e. raised by tkinter)."""
    del item  # 'item' is not used in logging but required for the callback.
    log = _get_log()
    exception = traceback.TracebackException(exc, val, tb)
    log.exception("--- Logging unhandled exception ---", exc_info=exception)
    print(exception)
    messagebox.showerror("unhandled exception", "error: an unhandled \
        exception has occured <{}> see log for more details".format(val))
