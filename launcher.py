from bot import twilight
import sys


def main():
    try:
        twilight.run()
    finally:
        exit_code = twilight.exit_code
        sys.exit(exit_code)


main()
