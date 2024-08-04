#!/usr/bin/env python

import argparse
import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

    from app.main import main  # isort:skip noqa
    from app.device_manager import list_devices  # isort:skip noqa

    # set up argument parser
    parser = argparse.ArgumentParser(description="placeholder")
    parser.add_argument(
        "-d", "--devices", action="store_true", help="List online devices"
    )
    parser.add_argument("-m", "--main", action="store_true", help="Run main program")

    # parse arguments
    args = parser.parse_args()

    # determine which function to run based on arguments
    if args.devices:
        list_devices()
    else:
        main()
