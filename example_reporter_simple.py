
import logging

from loopy.helpers.logging import init_logger
from loopy.parsing.TargetParser import CSVTargetParser, NmapTargetParser, NessusTargetParser
from loopy.execution.Executor import ShellExecutor
from loopy.reporting.Reporter import Reporter

from loopy.constants.Parsing import TARGET_LAYOUT_ID_HOST, TARGET_LAYOUT_ID_PORT, TARGET_LAYOUT_ID_SERVICE
from loopy.constants.Arguments import ARGUMENT_ID_HOST, ARGUMENT_ID_PORT, ARGUMENT_ID_SERVICE
from loopy.constants.Reporting import REPORT_ID_HOST, REPORT_ID_PORT, REPORT_ID_SERVICE


def main():
    init_logger()
    se = ShellExecutor()
    # simple reporter: 
    # * creates ./loopy_reports/
    # * errors are logged to ./loopy_reports/errors/
    # * logs are written to ./loopy_reports/loopy_<host>_<port>.log
    reporter = Reporter()
    parser = CSVTargetParser(skip_header=True)
    args_nc = [ARGUMENT_ID_HOST, ARGUMENT_ID_PORT]

    targets = parser.parse('./tests/targets_valid_and_invalid.csv')
    for t in targets: 
        res = se.exec_cmd(
            '/bin/nc', 
            args_nc, 
            t, 
            input=b'\n\n'
        )
        reporter.report(res, t)

if __name__ == "__main__":
    main()