import logging
import re

from libnmap.parser import NmapParser
from nessus_report_parser import parse_nessus_xml

from loopy.helpers.LoopyExceptions import LoopyError, LoopyFileError, LoopyParsingError, LoopyArgumentError, LoopyValueError
from loopy.constants.Parsing import KNOWN_TARGET_LAYOUT_IDS, TARGET_LAYOUT_ID_HOST, TARGET_LAYOUT_ID_PORT, TARGET_LAYOUT_ID_SERVICE, DEFAULT_TARGET_LAYOUT
from loopy.targets.TargetClass import Target

## base class
class TargetParser:
    def __init__(self):
        self._hostfilter = None
        self._portfilter = None
        self._servicefilter = None        

    def _open(self, filename):
        try:
            return open(filename, 'r')
        except Exception: 
            raise LoopyFileError(filename, 'Error opening file.')

    def _to_target_obj(self, host, port, service):
        if self._check_filters(host, port, service):
            return Target(host, port, service)
        return None

    def add_filters(self, hostfilter=None, portfilter=None, servicefilter=None):
        self._hostfilter = hostfilter
        self._portfilter = portfilter
        self._servicefilter = servicefilter


    def _regex_filter(self, regex_filter, value):
        if not re.compile(regex_filter).match(value):
            return False
        return True


    def _check_filters(self, host, port, service):
        if self._hostfilter:
            if not self._regex_filter(self._hostfilter, host):
                logging.info('Ignoring {}:{}/{} because of hostfilter'.format(host, port, service))
                return False
 
        if self._portfilter:
            if isinstance(self._portfilter, int):
                if self._portfilter != port:
                    logging.info('Ignoring {}:{}/{} because of portfilter'.format(host, port, service))
                    return False
            elif isinstance(self._portfilter, list):
                if not port in self._portfilter:
                    logging.info('Ignoring {}:{}/{} because of portfilter (list)'.format(host, port, service))
                    return False

        if self._servicefilter:
            if not self._regex_filter(self._servicefilter, service):
                logging.info('Ignoring {}:{}/{} because of servicefilter'.format(host, port, service))
                return False

        return True


class NmapTargetParser(TargetParser):
    def __init__(self, use_ips=True, use_hosts=False):
        super(NmapTargetParser, self).__init__()
        self._use_ips = use_ips
        self._use_hosts=use_hosts

    def _parse_nmap_target(self, host, service):
        results = list()
        
        host_addr = host.address
        hostnames = host.hostnames
        port = service.port
        service = service.service

        
        if self._use_ips:
            target = self._to_target_obj(host_addr, port, service)
            if target:
                results.append(target)
        if self._use_hosts:
            for h in set(hostnames):
                target = self._to_target_obj(h, port, service)

                if target:
                    results.append(target)
        
        return results


    def parse(self, filename):
        results = list()
        try:
            nmap_results = NmapParser.parse_fromfile(filename)
        except:
            raise LoopyParsingError(filename, 'Unable to open file.')

        for host in nmap_results.hosts:
            for service in host.services:
                try:
                    targets = self._parse_nmap_target(host, service)
                except LoopyError:
                    logging.error('Ignoring invalid Nmap service {}'.format(service))
                    continue

                if len(targets) > 0:
                    results = results + targets

        return results


class NessusTargetParser(TargetParser):
    def __init__(self):
        super(NessusTargetParser, self).__init__()

    def _parse_nessus_target(self):
        pass

    def parse(self, filename):
        results = list()
        f = self._open(filename)
        try:
            nessus_results = parse_nessus_xml(f.read())
            #print(nessus_results)
            
            h = nessus_results['report']['host']
            print(h['name'])
        except:
            raise LoopyParsingError(filename, 'Invalid Nessus file {}.'.format(filename))
 

        return None

## parse character separated files
class CSVTargetParser(TargetParser):

    def __init__(self, skip_header=False, format=DEFAULT_TARGET_LAYOUT, seperator=','):
        super(CSVTargetParser, self).__init__()
        self._format = format
        self._seperator = seperator
        self._skip_header = skip_header

    # map the user supplied identifiers to the known ones
    # returns dict in the form of KNOWN_IDENTIFIER -> INDEX IN USER SUPPLIED TARGET FORMAT 
    def _map_target_format(self):
        mapping = dict()
        for id_index in range(len(self._format)):
            identifier = self._format[id_index].lower()
            if not identifier in KNOWN_TARGET_LAYOUT_IDS:
                logging.warning('Ignoring unknown identifier {}'.format(identifier))

            # check which identifier we are currently examining
            for known_identifier in KNOWN_TARGET_LAYOUT_IDS:
                if known_identifier == identifier:
                    if known_identifier in mapping:
                        raise LoopyArgumentError('Identifier {} defined multiple times in target format.'.format(identifier))
                    mapping[identifier] = id_index

        return mapping

    def _parse_csv_target(self, target):
        mapping = self._map_target_format()
        
        arr = target.split(self._seperator)

        host = arr[mapping[TARGET_LAYOUT_ID_HOST]] 
        try:
            port = int(arr[mapping[TARGET_LAYOUT_ID_PORT]])
        except ValueError:
            raise LoopyValueError('Invalid port for target {}.'.format(target))
        service = arr[mapping[TARGET_LAYOUT_ID_SERVICE]]

        return self._to_target_obj(host, port, service)

    def parse(self, filename):
        results = list()
        try:
            f = self._open(filename)
        except:
            raise LoopyParsingError(filename, 'Unable to ope  file.')

        if self._skip_header:
            lines = f.readlines()[1:]
        else:
            lines = f.readlines()

        for l in lines:
            try:
                target = self._parse_csv_target(l)
            except LoopyError:
                logging.error('Ignoring invalid line {}'.format(l))
                continue

            if target:
                results.append(target)

        return results

