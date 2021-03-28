"""
MIT License

Copyright (c) 2020-2021 Jojo#7711

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

import asyncio
from tkinter import *
from tkinter import messagebox
import os  # I think?


dev: bool = False
no_cogs: bool = False
is_running = False
title = "Twilight launcher GUI"
CLEAR = "CLS" if os.name == "nt" else "CLEAR"

async def _a_run_bot():
    cmd = "py -m twilight"
    if dev:
        cmd += " --dev"
    if no_cogs:
        cmd += " --no-cogs"
    while True:
        x = await asyncio.create_subprocess_shell(cmd)
        await x.communicate()
        if x.returncode != 2:
            break
        await asyncio.create_subprocess_shell("cls")


def run_bot():
    global is_running
    if is_running:
        messagebox.showwarning(title=title, message="Twilight is already runnning!")
        return None
    is_running = True
    return asyncio.get_event_loop().create_task(_a_run_bot())


async def _a_kill_process():
    """This one's a weird one

    It iterates over the tasks and tries to
    """
    for task in asyncio.all_tasks():
        if str(task).split()[2] == "_a_run_bot":  # Fucking weird
            task.cancel()
            messagebox.showinfo(title="Stopped Twilight")
            return


def kill_process():
    global is_running
    if not is_running:
        messagebox.showwarning(title=title, message="Twilight is not running!")
        return None
    is_running = False
    return asyncio.get_event_loop().create_task(_a_kill_process())


def update_no_cogs():
    global no_cogs
    no_cogs = not no_cogs


def update_dev():
    global dev
    dev = not dev


async def run_tk(root: Tk):
    try:
        while True:
            root.update()
            await asyncio.sleep(0.05)
    except TclError as exc:
        pass


async def main():
    loop = asyncio.get_event_loop()
    root = Tk()
    root.title = title
    root.maxsize(800, 550)
    root.configure(background="purple")
    root.geometry("800x550")
    Button(root, text="Run Twilight", command=run_bot, width=35, height=1).grid(
        row=8, column=1, padx=350
    )
    Button(
        root,
        text="Shutdown Twilight (This shouldn't be ran)",
        command=kill_process,
        width=35,
        height=1,
    ).grid(row=9, column=1, padx=350)
    throw_away = IntVar()
    Checkbutton(
        root,
        text="Set whether dev should be enabled or not",
        variable=throw_away,
        command=update_dev,
    ).grid(row=15, column=1, padx=10)
    throw_away1 = IntVar()
    Checkbutton(
        root,
        text="Set whether the bot should run without cogs",
        variable=throw_away1,
        command=update_no_cogs,
    ).grid(row=20, column=1, padx=10)
    await run_tk(root)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.create_subprocess_shell("cls"))
    loop.run_until_complete(main())
    for task in asyncio.all_tasks(loop):
        loop.run_until_complete(task)
    print("Done!")
    os.system("pause")
