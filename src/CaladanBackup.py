import argparse
import datetime
import json
import os
import sys
import tarfile
import time
import re
from pathlib import Path

from CommonLogger import LoggerServices as logger_services
from CommonOs import OsServices as os_services
import Target_File_Builder as tfb


class PythonBackup(os_services, logger_services):
    def __init__(self):
        #super().__init__()
        #self.config_json = config_json
        #self.backupset_json = backupset_json
        #self.storageset_json = storageset_json
        #self.fileset_json = fileset_json
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

            group_0 = parser.add_mutually_exclusive_group()

            group_1 = parser.add_mutually_exclusive_group()
            self.args = parser.parse_args()
        except Exception as e:
            print(
                f'An exception occurred which caused the command line argument to not parse, investigate {e}')
        else:
            return self.args

    def run_object(self, frequency):
        logger_services.info(self, f'Starting {os.uname()[1]} backup')
        os_services.load_json(self)
        self.backup_start(frequency)
        logger_services.info(self, f'Completed {os.uname()[1]} backup')

    def backup_start(self, frequency):
        json_in = self.backup_set_decoder()

        backupset_name = None
        file_set_name = None
        storage_path = None
        storage_set_name = None
        backup_versions = 1
        include_files_list = []
        exclude_files_list = []
        self.skipping = True
        mounted = True

        # loop thru backup_set system json
        for major_key in json_in:
            if "BackupSets" in major_key:
                # loop thru backup sets
                for sSet in json_in[major_key]:
                    self.skipping = True  # reset skipping before every backup set
                    # collect backup set fields
                    for key in sSet:
                        if "BackupSetName" in key:
                            backupset_name = sSet[key]
                        if "StorageSetName" in key:
                            storage_path = self.storage_path_getter(sSet[key])
                            storage_set_name = sSet[key]
                        if "FileSetName" in key:
                            include_files_list = self.fileset_includes_getter(sSet[key])
                            exclude_files_list = self.fileset_excludes_getter(sSet[key])
                            file_set_name = sSet[key]
                        if "Frequency" in key and frequency in sSet["Frequency"]:
                            self.skipping = False
                        if "Versions" in key:
                            backup_versions = sSet["Versions"]

                    if re.search(rf'^{storage_path}', "Archives"):
                        if not os.path.ismount(storage_path):
                            mounted = False

                    if self.skipping:
                        logger_services.info(self,
                                             f" Skipping Backup Set \'{backupset_name}\' as "
                                             f"it is not scheduled for today\n")
                        continue
                    elif not mounted:
                        logger_services.info(self,
                                             f" Skipping Backup Set \'{backupset_name}\' as "
                                             f"Storage Path \'{storage_path}\' is not mounted")
                    else:
                        self.skipping = False
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

                    # end of for key in sSet
                # end of for sSet
            # end of if BackupSets
        # end of major_key loop

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
    def backup_set_decoder():
        config_path = os.path.join(Path.home(), ".config", os_services.getScriptName())
        with open(f'{config_path}/BackupSets.json', "r") as backupset_json:
            return json.load(backupset_json)

    @staticmethod
    def file_date():
        """This method returns a formatted string of the date in YYYYMMDD format"""
        return datetime.datetime.now().strftime('%Y%m%d')

    @staticmethod
    def date():
        """This method returns a formatted string of the date in YYYYMMDDhhmmss format"""
        return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    @staticmethod
    def is_file_older_than_x_days(file, days=1):
        file_time = os.path.getmtime(file)
        # Check against 24 hours
        return (time.time() - file_time) / 3600 > 24 * days

    def write_tar_file(self, target, sources, recursive):

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
    obj = PythonBackup()
    obj.getLogger()
    args = obj.parseCommandLine()
    obj.display_template(sys.argv[1:], args)
    obj.run_object(sys.argv[1])
