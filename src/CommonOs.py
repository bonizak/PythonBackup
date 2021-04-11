import datetime
import json
import os
import platform
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
        # print(self.startScriptLine())
        # logger_services.info(self, self.startScriptLine())
        print(f'{self.date()}: Extracting input Params:', *parameter_list)
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

        if os.path.isdir(self.crontabs_dir):
            os.makedirs(self.crontabs_dir)

            if not os.path.exists(self.crontabs_dir):
                self.msg = 'Initial setup of crontab dir failed, exiting script run!'
                print(f'{self.date()}: {self.msg}')
                logger_services.error(self, self.msg)
                sys.exit(1)

    def getCronDir(self):
        """
        This method returns the cron
        directory set on the class
        """
        return self.crontabs_dir

    def haltScript(self):
        """
        This method stop the script  from executing if the
        instance is not active and
        notify, inactive instance
        """
        print(f'{self.date()}: {self.msg}')
        logger_services.error(self, self.msg)
        return None

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

    def getIpAddress(self):
        """
        This method returns the IP address of the host
        """
        try:
            ip_obj = socket.gethostbyname_ex(self.getHostName())
            ip_list = [ip for ip in ip_obj[2]]
        except Exception as error:
            print(f'{self.date()}: Cannot lookup IP address..see the following error')
            raise error
        else:
            return ip_list

    @staticmethod
    def getScriptName():
        """
        This method returns the script name
        """
        return str(os.path.basename(sys.argv[0])).split('.')[0]

    def extractCommonLogVars(self, msg_tuple):
        """
        This method takes an instance
        name and extract the variables
        needed from the params xml and
        instance db params xml and returns
        it to be used by the commonlog method
        """
        pass
        # get the params xml to extract -lf variables
        #param_xml = self.loadParamsXML()[0]
        # get the inst db params xml and extract the inst_commonlog for potential use
        #inst_db_param_xml = self.loadInstDbXML()[0]
        #notify_tag = [tags.findall('NOTIFICATION_OPTIONS') for tags in param_xml.findall(
            #'account')]  # select the notifications tag from params XML
        #notify_ops = [ops_tag for ops_tag in notify_tag[0][0].findall(
            #'option') if ops_tag.attrib.get('type') == '-lf']  # select the -lf ops tag
        #support_group = notify_ops[0].findall('support_group')[0].attrib.get(
            #'name')  # extract the support group
        #error_sev = notify_ops[0].findall('error_sev')[0].attrib.get('level')
        #warning_sev = notify_ops[0].findall(
            #'warning_sev')[0].attrib.get('level')
        #server_commonlog = notify_ops[0].findall('server_commonlog')[0].attrib.get(
            #'path').strip(" ")  # extract the server level commonlog path if set

        #inst_commonlog = [tags.findall('inst_commonlog') for tags in inst_db_param_xml.findall('instance')
                          #if tags.attrib.get(
                #'name').lower() == self.getInstName().lower()]  # extract the instance level common log path if it is set and use it instead
        ## print(len(inst_commonlog))
        #if len(inst_commonlog) != 0:  # check if the inst level common log comes back empty
            #used_commonlog = inst_commonlog[0][0].attrib.get('path').strip(
                #" ")  # use it if its not empty stripping away the spaces
            # print(used_commonlog)
        #else:
            # else use server level stripping away the space
            #used_commonlog = server_commonlog
        #if len(used_commonlog) == 0:  # make sure the commong log used is not also empty
            #self.msg = f' Cannot use the -lf option  if common log path is NULL in the xml resources, exiting'
            #print(f'{self.date()}: {self.msg}')
            #logger_services.error(self, self.msg)
        #if 'ERROR' in msg_tuple[0]:
            #error_sev = 'CRITICAL'
        #else:
            #error_sev = warning_sev
        #return [error_sev, used_commonlog, support_group]


    def scriptRunCheck(self):
        """
        This method checks if 
        the script about to be run is 
        already running against the instance
        and returns a boolean value
        """
        pass

    def load_json(self):
        config_path = os.path.join(Path.home(), ".config", self.getScriptName())
        with open(f'{config_path}/config.json', "r") as config_json:
            self.config_json = json.load(config_json)

        with open(f'{config_path}/BackupSets.json', "r") as backupset_json:
            self.backupset_json = json.load(backupset_json)

        with open(f'{config_path}/StorageSets.json', "r") as storageset_json:
            self.storageset_json = json.load(storageset_json)

        with open(f'{config_path}/FileSets.json', "r") as fileset_json:
            self.fileset_json = json.load(fileset_json)

    @staticmethod
    def separationBar():
        """
        This method returns a separation
        bar to be used as part of
        the common template
        """
        return '============================================================================='

    @staticmethod
    def separationBar2():
        """
        This method returns a separation
        bar to be used as part of
        the common template
        """
        return '##############################################################################'

    def log_file_path(self):
        """
        This method returns the
        path to log file that was
        generated for the 
        script that was run
        """
        print(f'See  {self.setLogFile()}')

    def setLogFile(self):
        """
        This method sets log file
        to be written to for each
        script run
        """
        return str(os.path.join(self.getLogDir(), f'{sys.argv[0]}.{self.file_date()}'))

    def setLogDir(self):
        """
        This method sets the logs
        directory based on the OS
        """
        if self.whichOs() == 'Windows':
            self.log_dir = os.path.join(os.path.normpath(os.getcwd()), 'logs')
        else:
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
