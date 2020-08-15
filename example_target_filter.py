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

    parser = NmapTargetParser()
 
    print('No filters:')
    targets = parser.parse('./tests/nmap/nmap_localhost.xml')

    for t in targets:
        print(t.prettify())

    # add a service filter; you can also filter on hosts and ports
    print('With filters:')
    parser.add_filters(
        servicefilter='(ss.*)|rpcbind|ipp'
    )
    targets = parser.parse('./tests/nmap/nmap_localhost.xml')

    for t in targets:
        print(t.prettify())



if __name__ == "__main__":
    main()