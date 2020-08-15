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
    parser = CSVTargetParser(skip_header=True)
    targets = parser.parse('./tests/targets.csv')
    
    # call nmap -vvv -p<port> <host>
    args_nmap = [
        '-vvv', 
        '-p{}'.format(ARGUMENT_ID_PORT), 
        ARGUMENT_ID_HOST
    ]
    for t in targets:
        logging.info('Executing nmap for target {}'.format(t.prettify()))
        logging.info('Result {}'.format(se.exec_cmd('nmap', args_nmap, t)['output']))

if __name__ == "__main__":
    main()