"""
MIT License

Copyright (c) 2020 Jojo#7711

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys

import click

from bot import twilight
import logging.handlers  # Importing this imports logging and logging.handlers
from contextlib import contextmanager

log = logging.getLogger("launcher")


@contextmanager
def init_log():
    try:
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        dpylog = logging.getLogger("discord")
        dpylog.setLevel(logging.WARNING)

        fmt = logging.Formatter(
            "[{asctime}] [{levelname}] {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )
        stdout_handler = logging.StreamHandler(sys.stdout)  # Log to the console
        root.addHandler(stdout_handler)
        logging.captureWarnings(True)

        all_fhandler = logging.handlers.RotatingFileHandler(
            filename="twilight.log", mode="a", encoding="utf-8"
        )
        all_fhandler.setFormatter(fmt)
        root.addHandler(all_fhandler)

        yield
    finally:
        handlers = root.handlers[:]
        for hndlr in handlers:
            hndlr.close()
            root.removeHandler(hndlr)


@click.command()
@click.option("--no-cogs", is_flag=True)
@click.option("--dev", is_flag=True, default=False, flag_value=True)
def main(no_cogs, dev):
    try:
        twilight.run(no_cogs=no_cogs, dev=dev)
    except KeyboardInterrupt:
        log.info("Shutting down!")
        twilight.stop(1)
    finally:
        code = twilight.exit_code
        sys.exit(code)


if __name__ == "__main__":
    with init_log():  # `with` allows me to use the logging method and log stuff
        main()
