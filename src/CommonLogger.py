import datetime
import logging
import os
import sys
from pathlib import Path

from openpyxl import load_workbook


class LoggerServices:
    """
    This class contains the various methods needed to log and notify
    messages in a log file for each script run
    
     Args
        Required: none
        Optional: none

    Alerts: Critical | WARN | ERROR

    Logging: none
    
    """
    __author__ = "Barry Onizak"
    __version__ = "0.01"

    # # # # # End of header # # # #
    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")
    log_file = ""
    log_level = ""


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

    def setLogFile(self):
        """
        This method sets log file to be written to for each script run
        """
        return os.path.join(self.getLogDir(),
                            f'{str(os.path.basename(sys.argv[0])).replace(".py", "")}.{self.file_date()}.log')

    def getLogDir(self):
        """
        This method sets the logs directory
        """
        log_dir = os.path.join(str(Path.home()), 'logs', self.getScriptName())

        if os.path.isdir(log_dir):
            return log_dir
        else:
            os.makedirs(log_dir)
            if not os.path.exists(log_dir):
                msg = 'Initial setup of logs dir not done, exiting script run!'
                print(f'{self.date()}: {msg}')
                sys.exit(1)
            else:
                return log_dir

    def getLogger(self, name):
        """
        This method creates and returns a object used to log each script run
        """
        self.log_file = self.setLogFile()
        self.log_level = self.get_log_level()
        logger = logging.getLogger(name)
        logging.basicConfig(filename=self.log_file, level=self.log_level,
                            format=' %(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        self.openlogfile()
        return logger

    def starting_template(self, parameter_list, args):
        """
        This method takes a list of cmd line args
        passed and displays each running script in a similar view
        """
        self.info(f'Initialising python script {self.getScriptName()}')
        self.info(f"Extracting input params: {(' '.join(map(str, parameter_list)))}")
        self.info(f"Log Level {self.log_level}")
        return None

    def ending_template(self, parameter_list, args):
        """
        This method takes a list of cmd line args
        passed and displays each running script in a similar view
        """
        self.info(f'\nEnd of {self.getScriptName()}\n\n')
        return None

    def get_log_level(self):
        """
        This method reads in the AppConfig sheet from BackupList.xlsx workbook in the
        resources directory of this project, and extracts the Log_Level value.

        :return: Count of rows read in and written to  FileSystemsIn{}
        """
        wb = load_workbook(os.path.join(self.resource_path, "BackupList.xlsx"))
        worksheet = wb["AppConfig"]

        row_sets = [worksheetsets for worksheetsets in worksheet.iter_rows(
            min_row=3, max_row=3, min_col=1, max_col=2, values_only=True)
                    if None not in worksheetsets]
        return row_sets[0][1]

        return log_level

    def openlogfile(self):
        """
        This method opens the logfile and prepends the starting info
        """
        self.log_file = self.setLogFile()
        try:
            if os.path.exists(self.log_file):
                fo = open(self.log_file, 'a', encoding='utf-8')
                print(f'\nUsing logfile {self.log_file}')
            else:
                fo = open(self.log_file, 'w', encoding='utf-8')
                print(f'\nCreated logfile {self.log_file}')

            fo.write("\n\n")
            fo.write(self.startScriptLine())
            fo.write("\n")
            fo.close()
        except IOError as ioe:
            msg = f'Log file {self.log_file} write error. {ioe}.'
            print(f'{self.date()}: {msg}')

    @staticmethod
    def getScriptName():
        """
        This method returns the script name
        """
        return str(os.path.basename(sys.argv[0])).split('.')[0]

    def startScriptLine(self):
        """
        This method returns the script logfile opening info
        """
        script_path = os.path.normpath(os.path.join(os.popen("pwd").read().strip('\n'), str(sys.argv[0])))
        if not os.path.isfile(script_path):
            print('No such script name in toolkit folder...exiting')
            sys.exit(1)

        script_start = f'{self.separationBar()} \n Starting script {script_path} \n{self.separationBar()}'
        return script_start

    @staticmethod
    def separationBar():
        """
        This method returns a 90 char separation bar
        """
        return 90 * f'='

    def critical(self, msg):
        """
        This method takes a message and logs it as a
        CRITICAL to the script run log
        """
        logging.critical(msg)
        return None

    def error(self, msg):
        """
        This method takes a message and logs it as an
        ERROR  to the script run log
        """
        logging.error(msg)
        return None

    def warn(self, msg):
        """
        This method takes a message and logs it as an
        WARNING to the script run log
        """
        logging.warning(msg)
        return None

    def info(self, msg):
        """
        This method takes a message and logs it as an
        INFO to the script run log
        """
        logging.info(msg)
        return None

    def debug(self, msg):
        """
        This method takes a message and logs it as a
        DEBUG message to the script run log
        """
        logging.debug(msg)
        return None
