import datetime
import os
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
    __version__ = "1.0"
    # # # # # End of header # # # #

    # sets the  path from which all scripts are run
    script_path = os.path.join(os.getcwd(), sys.argv[0])
    msg = ''
    params_XML = None
    reports_dir = ''
    log_dir = ''
    log_file = ''

    def __init__(self, config_json, backupset_json, storageset_json, fileset_json):
        """
        This method constructs the CommonOS class object with the basic
        methods needed to setup all script runs
        """
        super().__init__()
        self.config_json = config_json
        self.backupset_json = backupset_json
        self.storageset_json = storageset_json
        self.fileset_json = fileset_json
        self.setReportDir()  # set the reports dir path

    def setReportDir(self):
        """
        This method sets the report directory
        """
        self.reports_dir = os.path.join(str(Path.home()), 'reports')

        if not os.path.isdir(self.reports_dir):
            os.makedirs(self.reports_dir)

            if not os.path.exists(self.reports_dir):
                self.msg = 'Initial setup of reports dir failed, exiting script run!'
                print(f'{self.date()}: {self.msg}')
                logger_services.error(self, self.msg)
                sys.exit(1)  # halt the script

    def getReportDir(self):
        """
        This method returns the report directory set on the class
        """
        return self.reports_dir

    def haltScript(self):
        """
        This method stop the script  from executing
        """
        print(f'{self.date()}: {self.msg}')
        logger_services.error(self, self.msg)
        return None

    @staticmethod
    def getScriptName():
        """
        This method returns the script name
        """

        return str(os.path.basename(sys.argv[0])).split('.')[0]

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

    def getHostName(self):
        """
        This method returns the hostname of the machine
        """
        try:
            hostname = socket.gethostname()
        except Exception as error:
            print(f'{self.date()}: Cannot lookup hostname..see the following error')
            raise error
        else:
            return hostname

    def scriptRunCheck(self):
        """
        This method checks if the script about to be run is
        already running and returns a boolean value
        """
        pass
