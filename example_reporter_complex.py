
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
    # we'll need to execute something to produce results and errors
    se = ShellExecutor()
    
    # more complex reporter:
    # * create a directory 'banner_grab_ssh' to write all reports to
    # * define nc_<hostname>_<port>.log as the logfilename for each execution
    # * write errors to /tmp/errors_banner_grab_ssh instead of banner_grab_ssh/errors/
    reporter = Reporter(
        'banner_grab_{}'.format('ssh'),
        'nc_{}_{}.log'.format(REPORT_ID_HOST, REPORT_ID_PORT),
        '/tmp/errors_banner_grab_{}'.format('ssh')
    )

    parser = CSVTargetParser(skip_header=True)
    args_nc = [ARGUMENT_ID_HOST, ARGUMENT_ID_PORT]

    targets = parser.parse('./tests/targets_valid_and_invalid.csv')
    for t in targets: 
        # just execute nc and collect the result.
        res = se.exec_cmd(
            '/bin/nc', 
            args_nc, 
            t, 
            input=b'\n\n'
        )
        reporter.report(res, t)


if __name__ == "__main__":
    main()