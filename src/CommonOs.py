import datetime
import os
import platform
import sys
from pathlib import Path

from CommonLogger import LoggerServices as logger_services


class OsServices(logger_services):
    """This class contains the common OS methods used across all scripts. 
    
    All common OS methods for setting up the various directories, getting OS related env, loading various OS env vars

    Args
        Required: none
        Optional: none

    Alerts: Critical | WARN | ERROR

    Logging: none
    
    """

    __author__ = "Barry Onizak"
    __version__ = "20220328.2"
    # # # # # End of header # # # #

    def __init__(self):
        """
        This method constructs the CommonOS class object with the basic
        methods needed to setup all script runs
        """
        super().__init__()
        # sets the  path from which all scripts are run
        self.script_path = os.path.join(os.getcwd(), sys.argv[0])
        self.setReportDir()
        self.msg = ''
        
    def setReportDir(self):
        """
        This method sets the report directory based on the OS
        """
        if self.whichOs() == 'Windows':
            self.reports_dir = os.path.join(os.path.normpath(os.getcwd()), os.pardir, 'reports')
        else:
            self.reports_dir = os.path.join(str(Path.home()), 'reports')

        if not os.path.isdir(self.reports_dir):
            os.makedirs(self.reports_dir)

            if not os.path.exists(self.reports_dir):
                self.msg = 'Initial setup of reports dir not done, exiting script run!'
                print(f'{self.date()}: {self.msg}')
                logger_services.critical(self, self.msg)
                self.notify(logger_services.notify_list)
                sys.exit(1)  # halt the script

    def getReportDir(self):
        """
        This method returns the report directory set on the class
        """
        return self.reports_dir

    def whichOs(self):
        """
        This method returns a string
        of the current OS type
        """
        return platform.system()

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
