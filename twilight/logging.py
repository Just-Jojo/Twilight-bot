import logging.handlers
import sys
from contextlib import contextmanager


@contextmanager
def init_logging():
    try:
        # __enter__
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        dpylog = logging.getLogger("discord")
        dpylog.setLevel(logging.CRITICAL)

        fmt = logging.Formatter(
            "[{asctime}] [{levelname}] {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )
        stdout_handler = logging.StreamHandler(sys.stdout)  # Log to the console
        stdout_handler.setFormatter(fmt)
        root.addHandler(stdout_handler)
        logging.captureWarnings(True)

        all_fhandler = logging.handlers.RotatingFileHandler(
            filename="twilight.log", mode="a", encoding="utf-8"
        )
        all_fhandler.setFormatter(fmt)
        root.addHandler(all_fhandler)

        yield
    finally:
        # __exit__
        handlers = root.handlers[:]
        for hndlr in handlers:
            hndlr.close()
            root.removeHandler(hndlr)
