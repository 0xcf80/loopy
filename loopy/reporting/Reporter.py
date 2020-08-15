import logging
import os

from pathlib import Path

from loopy.helpers.LoopyExceptions import LoopyFileError, LoopyInputError

from loopy.constants.Reporting import REPORT_ID_HOST, REPORT_ID_PORT, REPORT_ID_SERVICE
from loopy.constants.Parsing import TARGET_LAYOUT_ID_UNKNOWN_SERVICE


class Reporter:
    def __init__(self, 
            report_dir_placeholder='./loopy_reports/', 
            report_filename_placeholder='loopy_{}_{}.log'.format(REPORT_ID_HOST, REPORT_ID_PORT), 
            error_dir_placeholder=None):
        self._report_dir_placeholder = report_dir_placeholder
        self._report_filename_placeholder = report_filename_placeholder
        if error_dir_placeholder:
            self._error_dir_placeholder = error_dir_placeholder
        else:
            self._error_dir_placeholder = os.path.join(report_dir_placeholder, 'errors')
        self._report_dir = None
        self._error_dir = None


    # build a file or directory name from a string that contains placeholders for host, port, ... 
    def _build_report_name_str(self, report_name_str, target):
        host = self._sanitize__str_for_filename(target.get_host())

        report_name_str = report_name_str.replace(REPORT_ID_HOST, host)
        report_name_str = report_name_str.replace(REPORT_ID_PORT, str(target.get_port()))
        if target.get_service():
            service = self._sanitize__str_for_filename(target.get_service())
            report_name_str = report_name_str.replace(REPORT_ID_SERVICE, service)
        else:
            report_name_str = report_name_str.replace(REPORT_ID_SERVICE, TARGET_LAYOUT_ID_UNKNOWN_SERVICE)
        
        return report_name_str


    # try to create the report directory and file
    def _open_report_file(self, target):
        if not self._report_dir:
            try:
                self._report_dir = self._build_report_name_str(
                    self._report_dir_placeholder, 
                    target
                )
                Path(self._report_dir).mkdir(parents=True, exist_ok=True)
            except:
                raise LoopyFileError(self._report_dir, 'Error creating report directory {}'.format(self._report_dir))
        file_name = os.path.join(self._report_dir, self._build_report_name_str(self._report_filename_placeholder, target))

        try:
            f = open(file_name, 'w+')
        except:
            raise LoopyFileError(file_name, 'Error opening report file for writing {}'.format(file_name))

        return f

    # try to create the report directory and file for failed commands
    # TODO: maybe we can merge this with _open_report_file()
    def _open_error_file(self, target):
        if not self._error_dir:
            try:
                self._error_dir = self._build_report_name_str(
                    self._error_dir_placeholder, 
                    target
                )
                Path(self._error_dir).mkdir(parents=True, exist_ok=True)
            except:
                raise LoopyFileError(self._error_dir, 'Error creating error directory {}'.format(self._report_dir))
        file_name = os.path.join(self._error_dir, self._build_report_name_str(self._report_filename_placeholder, target))

        try:
            f = open(file_name, 'w+')
        except:
            raise LoopyFileError(file_name, 'Error opening error file for writing {}'.format(file_name))

        return f


    def _sanitize__str_for_filename(self, filename):
        badchars = [':', '/']
        for c in badchars:
            filename = filename.replace(c, '_')
        return filename
    

    def report(self, result, target):
        # simple string to log
        if isinstance(result, str):
            f = self._open_report_file(target)
            f.write(result)
        # dict with output (e.g. stdout) and errors (e.g. stderr) as returned by Executor class
        elif isinstance(result, dict) and ('output' in result) and ('errors' in result):
            if result['output']: 
                f = self._open_report_file(target)
                f.write(result['output'])
            if result['errors']:
                f = self._open_error_file(target)
                f.write(result['errors'])
        else:
            raise LoopyInputError('Invalid result passed to reporter function {}'.format(result))