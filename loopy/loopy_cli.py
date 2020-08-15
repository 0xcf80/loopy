import logging

from parsing.TargetParser import CSVTargetParser
from execution.Executor import ShellExecutor

from constants.Parsing import TARGET_LAYOUT_ID_HOST, TARGET_LAYOUT_ID_PORT, TARGET_LAYOUT_ID_SERVICE
from constants.Arguments import ARGUMENT_ID_HOST, ARGUMENT_ID_PORT, ARGUMENT_ID_SERVICE

def _init_logger():
    logging.basicConfig(level=logging.INFO)

def main():
    _init_logger()

    # TODO: 
    # * Argparse for default stuff

    logging.error('Not implemented as of now, check examples.py')

if __name__ == "__main__":
    main()