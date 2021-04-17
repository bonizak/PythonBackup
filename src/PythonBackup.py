import argparse
import datetime
import json
import os
import socket
import sys
import tarfile
import time

import Target_File_Builder as tfb
from CommonLogger import LoggerServices as logger_services
from CommonOs import OsServices as os_services


class PythonBackup(logger_services, os_services):
    def __init__(self, config_json, backupset_json, storageset_json, fileset_json):
        super().__init__()
        self.config_json = config_json
        self.backupset_json = backupset_json
        self.storageset_json = storageset_json
        self.fileset_json = fileset_json
        self.skipping = True
        self.args = ""

    def parseCommandLine(self):
        """
        This method sets up, parses and returns the command line arguments passed to script, it inherits
        common command line arguments such as notify ops from the CommonArgs.py
         """
        try:
            parser = argparse.ArgumentParser(prog=str(sys.argv[0]),
                                             usage='%(prog)s Backups a database or a list of databases in the mode '
                                                   'specified.')
            parser.add_argument(
                "frequency",
                help=f'Pass the backup frequency from DAILY, WEEKLY, MONTHLY, or ARCHIVE')
            self.args = parser.parse_args()
        except Exception as e:
            print(
                f'An exception occurred which caused the command line argument to not parse, investigate {e}')
        else:
            return self.args

    def run_object(self, frequency):
        uc_frequency = frequency.upper()
        logger_services.info(self, f'Starting {os.uname()[1]} backup')
        self.load_json()
        self.backup_start(uc_frequency)
        logger_services.info(self, f'Completed {os.uname()[1]} backup')

    def backup_start(self, frequency):
        json_in = self.backupset_json

        # loop thru backup_set system json
        for major_key in json_in:
            if "BackupSets" in major_key:
                for buSet in json_in[major_key]:
                    # reset the keys each loop
                    backupset_name = None
                    file_set_name = None
                    storage_path = None
                    # storage_set_name = None
                    backup_versions = 1
                    include_files_list = []
                    exclude_files_list = []
                    self.skipping = True
                    print(buSet)
                    for key in buSet:
                        if "BackupSetName" in key:
                            backupset_name = buSet["BackupSetName"]
                        if "StorageSetName" in key:
                            storage_path = self.storage_path_getter(buSet["StorageSetName"])
                            # storage_set_name = buSet["StorageSetName"]
                        if "FileSetName" in key:
                            include_files_list = self.fileset_includes_getter(buSet["FileSetName"])
                            exclude_files_list = self.fileset_excludes_getter(buSet["FileSetName"])
                            file_set_name = buSet["FileSetName"]
                        if "Frequency" in key and frequency in str(buSet["Frequency"]).upper():
                            self.skipping = False
                        if "Versions" in key:
                            backup_versions = buSet["Versions"]
                    # end of for key in buSet

                    if self.skipping:
                        logger_services.info(self,
                                             f" Skipping Backup Set \'{backupset_name}\' as "
                                             f"it is not scheduled for today\n")
                        continue
                    elif not os.path.exists(storage_path):
                        logger_services.error(self,
                                              f" Skipping Backup Set \'{backupset_name}\' as "
                                              f"Storage Path \'{storage_path}\' does not exist.")
                        continue
                    else:
                        logger_services.info(self, f'Running BackupSet {backupset_name} '
                                                   f'for FileSet {file_set_name} '
                                                   f'using StoragePath {storage_path}')
                        logger_services.debug(self, f' Includes {include_files_list}')
                        logger_services.debug(self, f' Excludes {exclude_files_list}')

                    # remove any excluded files from the includes list
                    if len(exclude_files_list) > 0:
                        for excl in exclude_files_list:
                            if excl in include_files_list:
                                include_files_list.remove(excl)

                    # Determine the archive file name based on the current versions
                    archive_target_basefile = os.path.join(storage_path, backupset_name, f'{backupset_name}')
                    logger_services.debug(self, f"Searching for the number of {archive_target_basefile}* files")
                    archive_builder = tfb.Target_File_Builder(f'{archive_target_basefile}', backup_versions)
                    archive_file = archive_builder.archive_target_file
                    archive_rc = self.write_tar_file(archive_file, include_files_list, True)
                    logger_services.info(self, f'Back up of Backup Set Name {backupset_name} '
                                               f'into {archive_file} '
                                               f'returned {archive_rc}\n')
                # loop thru backup sets
            # end of if BackupSets
        # end of major_key loop

    def load_config(self):
        resource_path = os.path.join(os.path.dirname(os.path.abspath(os.curdir)), "resource")
        json_in_file = ""
        try:
            json_in_file = f'{resource_path}/config.json'
            with open(json_in_file, "r") as read_json:
                self.config_json = json.load(read_json)
                return self.config_json
        except FileNotFoundError as fnfe:
            print(f" {fnfe}: Unable to find {json_in_file}")
            sys.exit(1)

    def load_json(self):
        resource_path = os.path.join(os.path.dirname(os.path.abspath(os.curdir)), "resource")
        json_in_file = ""
        try:
            json_in_file = f'{resource_path}/config.json'
            with open(json_in_file, "r") as read_json:
                self.config_json = json.load(read_json)

            json_in_file = f'{resource_path}/BackupSets.json'
            with open(json_in_file, "r") as read_json:
                self.backupset_json = json.load(read_json)

            json_in_file = f'{resource_path}/StorageSets.json'
            with open(json_in_file, "r") as read_json:
                self.storageset_json = json.load(read_json)

            json_in_file = f'{resource_path}/FileSets.json'
            with open(json_in_file, "r") as read_json:
                self.fileset_json = json.load(read_json)

        except FileNotFoundError as fnfe:
            logger_services.critical(self, f" {fnfe}: Unable to find {json_in_file}")
            sys.exit(1)

    def get_backupset_json(self):
        return self.backupset_json

    def get_storageset_json(self):
        return self.storageset_json

    def get_fileset_json(self):
        return self.fileset_json

    def get_config_json(self):
        return self.config_json

    def storage_path_getter(self, storageSet_needle):
        json_in = self.storageset_json

        for major_key in json_in:
            if "StorageSets" in major_key:
                for sSet in json_in[major_key]:
                    for key in sSet:
                        if "StorageSetName" in key and storageSet_needle in sSet[key]:
                            return sSet["StoragePath"]

    def fileset_includes_getter(self, filesetname_needle):
        json_in = self.fileset_json

        fs_includes = []

        for major_key in json_in:
            if "FileSets" in major_key:
                for sSet in json_in[major_key]:
                    for key in sSet:
                        if "FileSetName" in key and filesetname_needle in sSet[key]:
                            for fs in sSet["IncludePaths"]:
                                fs_includes.append(fs)

        return fs_includes

    def fileset_excludes_getter(self, filesetname_needle):
        json_in = self.fileset_json

        fs_excludes = []

        for major_key in json_in:
            if "FileSets" in major_key:
                for sSet in json_in[major_key]:
                    for key in sSet:
                        if "FileSetName" in key and filesetname_needle in sSet[key]:
                            for fs in sSet["ExcludePaths"]:
                                fs_excludes.append(fs)

        return fs_excludes

    @staticmethod
    def getScriptName():
        """
        This method returns the script name
        """

        return str(os.path.basename(sys.argv[0])).split('.')[0]

    @staticmethod
    def file_date():
        """This method returns a formatted string of the date in YYYYMMDD format"""
        return datetime.datetime.now().strftime('%Y%m%d')

    @staticmethod
    def date():
        """This method returns a formatted string of the date in YYYYMMDDhhmmss format"""
        return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

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
    def separationBar():
        """
        This method returns a separation
        bar to be used as part of
        the common template
        """
        return 75*f'*'

    @staticmethod
    def separationBar2():
        """
        This method returns a separation
        bar to be used as part of
        the common template
        """
        return 75*f'#'

    @staticmethod
    def is_file_older_than_x_days(file, days=1):
        file_time = os.path.getmtime(file)
        # Check against 24 hours
        return (time.time() - file_time) / 3600 > 24 * days

    def write_tar_file(self, target, sources, recursive):
        """ Tar and compress the sources into the target """
        try:
            with tarfile.open(target, 'w:gz') as tar_out:
                for src in sources:
                    tar_out.add(src, recursive=recursive)

            tar_out.close()
            return 0
        except OSError as oserr:
            return oserr


# =================================
if __name__ == '__main__':
    obj = PythonBackup(None, None, None, None)
    config_json = obj.load_config()
    obj.getLogger(__name__, config_json)
    args = obj.parseCommandLine()
    obj.display_template(sys.argv[1:], args)
    obj.run_object(sys.argv[1])
