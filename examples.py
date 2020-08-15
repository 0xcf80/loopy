"""
Examples to demonstrate how this project can be used to implement a "quick and dirty" multi-execution wrapper.
"""

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

    # shell executor helper class
    se = ShellExecutor()

    # reporting helper class
    reporter = Reporter(
        'banner_grab_{}'.format('ssh'),
        'nc_{}_{}.log'.format(REPORT_ID_HOST, REPORT_ID_PORT),
    )

    # parse a CSV file in default format (host,port,service)
    parser = CSVTargetParser(skip_header=True)
    targets = parser.parse('./tests/targets.csv')

    # this parser processes a CSV file in a different format (service;host;port)
    parser2 = CSVTargetParser(
        skip_header=True,
        format = [
            TARGET_LAYOUT_ID_SERVICE, 
            TARGET_LAYOUT_ID_HOST, 
            TARGET_LAYOUT_ID_PORT
        ],
        seperator=';'
    )
    targets2 = parser2.parse('./tests/targets_format2.csv')

    # example executing nc on all targets; nc will hang and wait for input, so send 2 newlines
    args_nc = [ARGUMENT_ID_HOST, ARGUMENT_ID_PORT]

    for t in targets:
        logging.info('Executing nc for target {}'.format(t.prettify()))
        res = se.exec_cmd('/bin/nc', args_nc, t, input=b'\n\n')['output']
        logging.info('Result {}'.format(res))
        reporter.report(res, t)

    # simple example demonstrating use of custom args passed to the program (here nmap)
    args_nmap = ['-vvv', '-p{}'.format(ARGUMENT_ID_PORT), ARGUMENT_ID_HOST]

    for t in targets:
        logging.info('Executing nmap for target {}'.format(t.prettify()))
        logging.info('Result {}'.format(se.exec_cmd('nmap', args_nmap, t)['output']))

    # do some filtering on targets. 
    # host, service can be regex, port int or list of ints
    parser.add_filters(
        hostfilter='127.*',
        portfilter=[22,34835],
        servicefilter='(ss.*)|rpcbind'
    )

    targets_filter = parser.parse('./tests/targets_filter.csv')

    # target parsing tests
    for t in targets_filter:
        logging.info('Testing CSV with filters')
        print(t.prettify())

    ##
    # testcases. to be moved. 
    # target parsing tests
    for t in targets2:
        logging.info('Testing CSV with different order')
        print(t.prettify())
 
    # testing correct logging of stdout and stderr
    targets_invalid = parser.parse('./tests/targets_valid_and_invalid.csv')
    for t in targets_invalid: 
        reporter.report(se.exec_cmd('/bin/nc', args_nc, t, input=b'\n\n'), t)

    reporter_custom_error_dir = Reporter(
        'banner_grab_{}'.format('ssh'),
        'nc_{}_{}.log'.format(REPORT_ID_HOST, REPORT_ID_PORT),
        '/tmp/errors_banner_grab_{}'.format('ssh')
    )

    for t in targets_invalid: 
        reporter_custom_error_dir.report(se.exec_cmd('/bin/nc', args_nc, t, input=b'\n\n'), t)

    # parse an Nmap file
    nmap_parser = NmapTargetParser(use_hosts=True)
    nmap_parser_no_hosts = NmapTargetParser()

    nmap_targets = nmap_parser.parse('./tests/nmap/nmap_localhost.xml')

    # parse an Nmap file with filters
    nmap_parser_no_hosts.add_filters(
        servicefilter='(ss.*)|rpcbind|ipp'
    )

    nmap_targets_filter_no_hosts = nmap_parser_no_hosts.parse('./tests/nmap/nmap_localhost.xml')

    
    print('nmap filtered scan results (hostnames and nfs should be missing):')
    for t in nmap_targets_filter_no_hosts:
        print(t.prettify())
    
    # trigger some exception
    #print(parser.parse('./tests/targets.cs'))

    #nessus_parser = NessusTargetParser()
    #nessus_targets = nessus_parser.parse('./tests/nessus/example_nessus.xml')
    # not a valid nessus file
    #nessus_parser.parse('./tests/targets.csv')

    #for t in nessus_targets:
    #    print(t.prettify())

if __name__ == "__main__":
    main()