from bot import twilight
import sys


def main():
    """Runs Twilight

    It will exit with the proper code
    """
    try:
        twilight.run()
    except KeyboardInterrupt:
        print("Exiting Twilight!")
        twilight.close()
    finally:
        exit_code = twilight.exit_code
        sys.exit(exit_code)


main()
