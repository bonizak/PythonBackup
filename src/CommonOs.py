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
    crontabs_dir = ''
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
        self.setLogDir()  # set the logs dir path
        self.setCronDir()  # the cron dir under UNIX/LINUX

    def display_template(self, parameter_list, args):
        """
        This method takes a list of cmd line args
        passed and displays each running script in a similar view
        """
        logger_services.info(self, f''"Extracting input params: {}".format(' '.join(map(str, parameter_list))))
        return None

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

    def setCronDir(self):
        """
        This method sets the cron  directory
        """
        self.crontabs_dir = os.path.join(str(Path.home()), 'crontabs')

        if not os.path.isdir(self.crontabs_dir):
            os.makedirs(self.crontabs_dir)

            if not os.path.exists(self.crontabs_dir):
                self.msg = 'Initial setup of crontab dir failed, exiting script run!'
                print(f'{self.date()}: {self.msg}')
                logger_services.error(self, self.msg)
                sys.exit(1)

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

    def startScriptLine(self):
        """
        This method introduces the script that is about to be run and returns
        it in a variable to be called as a part of the Common Template
        """
        self.script_path = os.path.normpath(os.path.join(os.popen("pwd").read().strip(
            '\n'), str(sys.argv[0])))
        if not os.path.isfile(self.script_path):
            print('No such script name in toolkit folder...exiting')
            sys.exit(1)

        script_start = f'\n{self.separationBar()} \n Starting script {self.script_path} \n{self.separationBar()}'
        return script_start
