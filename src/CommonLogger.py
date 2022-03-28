import datetime
import logging
import os
import platform
import sys
from pathlib import Path


class LoggerServices:
    """
    This class contains the various methods needed to log and notify
    messages in a log file for each script run

     Args
        Required: none
        Optional: none

    Alerts: As listed
    Level       Numeric value
    CRITICAL    50
    ERROR       40
    WARNING     30
    INFO        20
    DEBUG       10

    Logging: none

    """

    __author__ = "Barry Onizak"
    __version__ = "20220328.1"
    # # # # # End of header # # # #
    notify_list = []
    log_dir = ''
    log_file = ''
    msg = ''

    def whichOs(self):
        """
        This method returns a string
        of the current OS type
        """
        return platform.system()

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
        This method sets log file
        to be written to for each
        script run
        """
        self.setLogDir()
        fname = os.path.splitext(sys.argv[0])[0]
        self.log_file = os.path.join(self.getLogDir(), f'{fname}.{self.file_date()}.log')

    def setLogDir(self):
        """
        This method sets the logs
        directory based on the OS
        """
        if self.whichOs() == 'Windows':
            # On Windows "logs" is under the db2mptkt folder
            parent_db2mptkt = os.path.normpath(os.path.join(os.getcwd(), os.pardir))
            self.log_dir = os.path.join(parent_db2mptkt, 'logs')
        else:
            # on UNIX servers, "logs" is in the instance home
            self.log_dir = os.path.join(str(Path.home()), 'logs')

        if os.path.isdir(self.log_dir):
            return self.log_dir
        else:
            os.makedirs(self.log_dir)
            if not os.path.exists(self.log_dir):
                self.msg = 'Initial setup of logs dir not done, exiting script run!'
                print(f'{self.date()}: {self.msg}')
                sys.exit(1)
            else:
                return self.log_dir

    def getLogDir(self):
        """
        This method returns the log
        directory set on the class
        """
        return self.log_dir

    def getLogFile(self):
        """
        This method returns the log file set on the class for the script
        """
        return self.log_file

    def getLogger(self):
        """
        This method creates and returns
        a logger object used to log each
        script run
        """
        self.setLogFile()
        log_file = self.openlogfile()
        logger = logging.getLogger(sys.argv[0].strip(".\\"))
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format=' %(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        return logger

    def openlogfile(self):
        """ This method opens the logfile and prepends the starting info"""

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
            return self.log_file
        except IOError as e:
            self.msg = f'Log file {self.log_file} write error. {e}.'
            print(f'{self.date()}: {self.msg}')
            sys.exit(1)

    def startScriptLine(self):
        """This method returns the script logfile opening info """
        script_path = os.path.normpath(os.path.join(str(os.getcwd()).strip('\n'), str(sys.argv[0])))
        # checks if the script exist in the location before trying to run it
        if not os.path.isfile(script_path):
            print('No such script name in toolkit folder...exiting')
            sys.exit(1)

        script_start = f'{self.separationBar()} \n Starting script {script_path} \n{self.separationBar()}'
        return script_start

    def endingScriptLine(self):
        """
        This method returns the script logfile closing info
        """
        script_path = os.path.normpath(os.path.join(str(os.getcwd()).strip('\n'), str(sys.argv[0])))
        script_end = f'{self.separationBar()} \n End of script {script_path} \n{self.separationBar()}'
        return script_end

    def closelogfile(self):
        """
        This method appends the closing log info and closes the logfile
        """
        try:
            fo = open(self.log_file, 'a', encoding='utf-8')
            fo.write("\n")
            fo.write(self.endingScriptLine())
            fo.write("\n")
            fo.close()
            print(self.endingScriptLine())
        except IOError as ioe:
            msg = f'Log file {self.log_file} write error. {ioe}.'
            print(f'{self.date()}: {msg}')

        return self.log_file

    @staticmethod
    def separationBar():
        """
        This method returns a separation
        bar to be used as part of
        the common template
        """
        return '============================================================================='

    def critical(self, msg):
        """
        This method takes a message logs it as an
        CRITICAL message to the script run log
        and appends the msg to a notify list.
        CRITICAL is used for script ending error events requiring immediate attention via
        the highest level of alerting (eg. PAGEOUT).
        """
        logging.critical(msg)
        self.notify_list.append(('CRITICAL', msg))
        return None

    def error(self, msg):
        """
        This method takes a message logs it as an
        ERROR to the script run log
        and appends the msg to a notify list.
        ERROR is used for non-script ending error events requiring as soon as possible attention via
        the 2nd-highest level of alerting (eg. email).
        """
        logging.error(msg)
        self.notify_list.append(('ERROR', msg))
        return None

    def warn(self, msg):
        """
        This method takes a message logs it as an
        WARNING message to the script run log
        and appends the msg to a notify list.
        WARN is used for non-script ending events requiring next business day attention via
        the standard level of alerting (eg. email).
        """
        logging.warning(msg)
        self.notify_list.append(('WARNING', msg))
        return None

    def info(self, msg):
        """
        This method takes a message logs it as an
        INFO message to the script run log
        and appends the msg to a notify list.
        INFO is used for logging informational notifications not requiring any attention.
        """
        logging.info(msg)
        self.notify_list.append(('INFO', msg))
        return None

    def debug(self, msg):
        """
        This method takes a message logs it as an
        DEBUG message to the script run log
        and appends the msg to a notify list
        DEBUG is for development information collection. Default logging.level of higher than DEBUG would
        stop these messages from being logged.
        """
        logging.debug(msg)
        self.notify_list.append(('DEBUG', msg))
        return None
