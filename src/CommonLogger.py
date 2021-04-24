import datetime
import logging
import platform
import sys
import os

from pathlib import Path


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
    log_file = ""


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

    def getLogger(self, name, config_json):
        """
        This method creates and returns a object used to log each script run
        """
        self.log_file = self.setLogFile()
        log_level = self.get_log_level(config_json)
        # logger = logging.getLogger(sys.argv[0].strip(".\\"))
        logger = logging.getLogger(name)
        logging.basicConfig(filename=self.log_file, level=log_level,
                            format=' %(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

        return logger

    def get_log_level(self, json_in):
        """
        This method gets the log_level setting from the config_json
        """
        log_level = "DEBUG"
        for major_key in json_in:
            if "Config" in major_key:
                for cfg_Set in json_in[major_key]:
                    for key in cfg_Set:
                        if "LOG_LEVEL" in key:
                            log_level = cfg_Set["LOG_LEVEL"]
        return log_level

    def openlogfile(self):
        """
        This method opens the logfile and prepends the starting info
        """
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
        This method returns a 30 char separation bar
        """
        return 30 * f'='

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

    def notset(self, msg):
        """
        This method takes a message and logs it as a
        NOTSET message to the script run log
        """
        logging.log(self, msg)
        return None
