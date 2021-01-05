# I may or may not have borrowed this from Carberra Tutorials (who I got the insperation from to rebuild Twily like this)
# you can check his channel out @ https://www.youtube.com/channel/UC13cYu7lec-oOcqQf5L-brg
# or his discord.py rewrite repo @ https://github.com/Carberra/updated-discord.py-tutorial

# Thanks for the insperation :)

from sqlite3 import connect, OperationalError
from os.path import isfile

BUILDER_PATH = "./db/builder.sql"
try:
    DB_PATH = "./db/database.db"
    conc = connect(DB_PATH)
except OperationalError:
    from ..secrets import DB_BUILD_PATH
    conc = connect(DB_BUILD_PATH)
cur = conc.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    return inner


@with_commit
def build():
    """Runs the `script.sql` file"""
    if isfile(BUILDER_PATH):
        scriptexc(BUILDER_PATH)


def commit():
    """Commit"""
    conc.commit()


def close():
    """Closes the connection"""
    conc.close()


def field(command, *values):
    """Executes a command then fetchs the first field"""
    cur.execute(command, tuple(values))
    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    """Executes a command then fetches"""
    cur.execute(command, tuple(values))
    return cur.fetchone()


def records(command, *values):
    """Executes a command then fetches all"""
    cur.execute(command, tuple(values))
    return cur.fetchall()


def column(command, *values):
    """Executes a command then returns a column"""
    cur.execute(command, tuple(values))
    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    """Executes a command"""
    cur.execute(command, tuple(values))


def multi_execute(command, valueset):
    """Executes several commands"""
    cur.executemany(command, valueset)


def scriptexc(path):
    """Executes a script"""
    # I shouldn't code when I'm tired...
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())
