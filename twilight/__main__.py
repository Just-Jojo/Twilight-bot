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

import argparse
import asyncio
import functools
import logging
import signal
import sys

import discord

from twilight.logging import init_logging

from .bot import ShutdownCodes, Twilight

log = logging.getLogger("twilight")


def parse_cli_stuff(sysargs):
    args = argparse.ArgumentParser(description="Main Twilight argument parser")
    args.add_argument(
        "--dev", "-d", action="store_true", help="Runs the bot in Dev mode"
    )
    args.add_argument(
        "--no-cogs", "-nc", action="store_true", help="Runs the bot with no cogs loaded"
    )
    args.add_argument(
        "--lock",
        "-l",
        action="store_true",
        help="Locks the bot to the servers it's already on",
    )
    return args.parse_args(sysargs)


async def shutdown_handler(bot: Twilight, signal_type=None, exit_code=None):
    if signal_type:
        log.info(f"{signal_type} received. Shutting down...")
        sys.exit(ShutdownCodes.SHUTDOWN)
    elif exit_code is None:
        log.info("Shutting down from unhandled exception.")

    if exit_code is not None:
        bot._exit_code = exit_code
    try:
        await bot.logout()
    finally:
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in pending]
        await asyncio.gather(*pending, return_exceptions=True)


async def global_exception_handler(
    twilight: Twilight, loop: asyncio.BaseEventLoop, context
):
    msg = context.get("exception", context["message"])
    if not isinstance(msg, (KeyboardInterrupt, SystemExit)):
        if isinstance(msg, Exception):
            log.critical("Caught unhandled exception in task:\n", exc_info=msg)
        else:
            log.critical(f"Caught unhandled exception in task: {msg}")


async def run_twilight(twilight: Twilight):
    try:
        await twilight.start()
    except discord.LoginFailure:
        log.critical(
            "Your token is invalid. Please make"
            " sure you have the proper token and run again."
        )
    except discord.PrivilegedIntentsRequired:
        log.critical("Please enable the required intents before running Twilight.")


def twilight_exception_handler(bot: Twilight, bot_task: asyncio.Future):
    try:
        bot_task.result()
    except (SystemExit, KeyboardInterrupt, asyncio.CancelledError):
        pass
    except Exception as exc:
        log.critical("The main bot task didn't die... owo", exc_info=exc)
        log.warning("Dying or something")
        bot.loop.create_task(shutdown_handler(bot))


def main():
    cli_flags = parse_cli_stuff(sys.argv[1:])
    twilight = None # Just in case we can't actually initialize Twilight
    with init_logging():

        try:
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)

            twilight = Twilight(cli_flags=cli_flags)
            exc_handler = functools.partial(global_exception_handler, twilight)
            loop.set_exception_handler(exc_handler)

            future = loop.create_task(run_twilight(twilight=twilight))
            fut_handler = functools.partial(twilight_exception_handler, twilight)
            future.add_done_callback(fut_handler)

            loop.run_forever()
        except KeyboardInterrupt:
            log.info("Shutting down...")
            loop.run_until_complete(
                shutdown_handler(bot=twilight, signal_type=signal.SIGINT)
            )
        except SystemExit as exc:
            log.info("Caught System exit")  # TODO Fix this lol
            loop.run_until_complete(shutdown_handler(twilight, None, exc.code))
        except Exception as exc:
            log.critical(f"Unhandled Exception {type(exc)}", exc_info=exc)
            loop.run_until_complete(
                shutdown_handler(twilight, None, ShutdownCodes.CRITICAL)
            )
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            log.info("Tidying up the Library")  # RIP Golden Oak's library ;-;
            loop.run_until_complete(asyncio.sleep(2))
            asyncio.set_event_loop(None)
            loop.stop()
            loop.close()
            if twilight is not None:
                exit_code = twilight._exit_code
            else:
                exit_code = 1
            sys.exit(exit_code)


if __name__ == "__main__":
    main()
