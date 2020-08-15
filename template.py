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

    """
    # Example code for your reference :)
    # * define a reporter so that successful and errornous execution is logged 
    # * parse a CSV 
    # * apply a filter to only scan services on port 22
    # * execute nc <host> <port> in a loop with user input 

    se = ShellExecutor()

    reporter = Reporter(
        'banner_grab_{}'.format('ssh'),
        'nc_{}_{}.log'.format(REPORT_ID_HOST, REPORT_ID_PORT),
    )

    parser = CSVTargetParser(skip_header=True)
    parser.add_filters(portfilter=22)

    targets = parser.parse('./tests/targets.csv')

    args_nc = [ARGUMENT_ID_HOST, ARGUMENT_ID_PORT]

    for t in targets:
        logging.info('Executing nc for target {}'.format(t.prettify()))
        res = se.exec_cmd('/bin/nc', args_nc, t, input=b'\n\n')
        logging.info('Result: {}'.format(res['output']))
        reporter.report(res, t)
    """

if __name__ == "__main__":
    main()