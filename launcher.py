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

import click
import subprocess as subp

import sys


def run(no_cogs: bool, dev: bool):
    while True:
        print("Starting Twilight...")
        cmd = ["py", "-m", "bot"]
        if no_cogs:
            cmd.append("--no-cogs")
        if dev:
            cmd.append("--dev")
        status = subp.call(cmd)
        if status != 4:
            break
        subp.run(["cls"])


@click.command()
@click.option("-nc", "--no-cogs", is_flag=True, default=False)
@click.option("-d", "--dev", is_flag=True, default=False)
def main(no_cogs, dev):
    run(no_cogs=no_cogs, dev=dev)
    print("Thank you for running!")


if __name__ == "__main__":
    main()
