import logging

from loopy.helpers.logging import init_logger
from loopy.parsing.TargetParser import CSVTargetParser
from loopy.execution.Executor import ShellExecutor

from loopy.constants.Parsing import TARGET_LAYOUT_ID_HOST, TARGET_LAYOUT_ID_PORT, TARGET_LAYOUT_ID_SERVICE
from loopy.constants.Arguments import ARGUMENT_ID_HOST, ARGUMENT_ID_PORT, ARGUMENT_ID_SERVICE
from loopy.constants.Reporting import REPORT_ID_HOST, REPORT_ID_PORT, REPORT_ID_SERVICE


def main():
    init_logger()

    # this parser processes a CSV file in a non-default format (service;host;port)
    parser = CSVTargetParser(
        skip_header=True,
        format = [
            TARGET_LAYOUT_ID_SERVICE, 
            TARGET_LAYOUT_ID_HOST, 
            TARGET_LAYOUT_ID_PORT
        ],
        seperator=';'
    )
    targets = parser.parse('./tests/targets_format2.csv')

    for t in targets:
        print(t.prettify())

if __name__ == "__main__":
    main()