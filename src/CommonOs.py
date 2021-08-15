import datetime
import os
import socket
import sys
from pathlib import Path

from CommonLogger import LoggerServices as logger_services


class OsServices(logger_services):
    """This class contains the common OS methods used across all scripts. 
    
    All common OS methods for setting up the various directories, getting OS related env, loading various OS env vars

    Args
        Required: none
        Optional: none

    Logging: ERROR
    
    """

    __author__ = "Barry Onizak"
    __version__ = "20210814.1"
    # # # # # End of header # # # #

    def __init__(self):
        """
        This method constructs the CommonOS class object with the basic
        methods needed to setup all script runs
        """
        super().__init__()
        # sets the  path from which all scripts are run
        self.script_path = os.path.join(os.getcwd(), sys.argv[0])
        self.reports_dir = self.setReportDir()  # set the reports dir path
        self.crontabs_dir = self.setCronDir()  # the cron dir under UNIX/LINUX
        self.msg = ''

    def setReportDir(self):
        """
        This method sets the report directory
        """
        reports_dir = os.path.join(str(Path.home()), 'reports')

        if not os.path.isdir(reports_dir):
            os.makedirs(reports_dir)

            if not os.path.exists(reports_dir):
                self.msg = 'Initial setup of reports dir failed, exiting script run!'
                print(f'{self.date()}: {self.msg}')
                logger_services.error(self, self.msg)
                sys.exit(1)  # halt the script
        return reports_dir

    def getReportDir(self):
        """
        This method returns the report directory set on the class
        """
        return self.reports_dir

    def setCronDir(self):
        """
        This method sets the cron  directory
        """
        crontabs_dir = os.path.join(str(Path.home()), 'crontabs')

        if not os.path.isdir(crontabs_dir):
            os.makedirs(crontabs_dir)

            if not os.path.exists(crontabs_dir):
                self.msg = 'Initial setup of crontab dir failed, exiting script run!'
                print(f'{self.date()}: {self.msg}')
                logger_services.error(self, self.msg)
                sys.exit(1)
        return crontabs_dir

    def getCronDir(self):
        """
        This method returns the cron directory set on the class
        """
        return self.crontabs_dir

    def haltScript(self):
        """
        This method stop the script  from executing
        """
        print(f'{self.date()}: {self.msg}')
        logger_services.error(self, self.msg)
        return None

    @staticmethod
    def date():
        """
        This method returns a formatted string of the date in YYYY/MM/DD/hh/mm/ss format
        """
        return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    @staticmethod
    def file_date():
        """
        This method returns a formatted date string in YYYYMMDD for appending to file names
        """
        return datetime.datetime.now().strftime('%Y%m%d')

    def scriptRunCheck(self):
        """
        This method checks if the script about to be run is
        already running and returns a boolean value
        """
        pass
