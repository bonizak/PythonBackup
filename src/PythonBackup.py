import argparse
import os
import socket
import sys
import tarfile
import time

import Target_File_Builder as tfb
from CommonOs import OsServices as os_services
from CommonTemplate import Template as Temp
from Excel_Converter import Excel_Converter as excel_conv
from FileSizeWriter import FSWriter as file_sizes
from Reload_Filesets import ReloadFileSets as reload_filesets
from Update_General import UpdateGeneral as updg


# from CommonLogger import LoggerServices as logger_services


class PythonBackup(Temp, updg, reload_filesets, file_sizes, excel_conv, os_services):
    """
    This class contains the methods to read the FileSets sheet and
    collects and updates the 'Estimated Size' cell for each row

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
        super().__init__()
        self.BackupSet_AoD = []
        self.StorageSet_AoD = []
        self.FileSet_AoD = []
        self.args = ""
        self.resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")

    def parseCommandLine(self):
        """
        This method sets up, parses and returns the command line arguments passed to script, it inherits
        common command line arguments such as notify ops from the CommonArgs.py
         """
        try:
            parser = argparse.ArgumentParser(prog=str(sys.argv[0]),
                                             usage="%(prog)s Back up your file systems according to the "
                                                   "information provided in a companion spreadsheet.")
                                                   
            parser.set_defaults(version=self.__version__)
            megroup = parser.add_mutually_exclusive_group()
            megroup.add_argument("-run_frequency", required=False,
                                 help=f'Pass the backup frequency value of DAILY, WEEKLY, MONTHLY, ARCHIVE or ANY')
            megroup.add_argument("-reload", action="store_true", required=False,
                                 help=f'Pass to reload the FileSet sheet of the BackupSetList.xlsx in the '
                                      f'resources directory. Review and edit the FileSets sheet once reloaded.')
            megroup.add_argument("-upd_general", action="store_true", required=False,
                                 help=f'Pass upd_general to copy any non-user files into the $USERHOME/GENERAL to be '
                                      f'captured during backups')
            megroup.add_argument("-refresh_sizes", action="store_true", required=False,
                                 help=f'Pass refresh_sizes to collect and update the file size sheet '
                                      f'of the BackupSetList.xlsx')

            self.args = parser.parse_args()
        except Exception as e:
            print(
                f'An exception occurred which caused the command line argument to not parse, investigate {e}')
        else:
            return self.args

    def run_PythonBackup(self):
        if self.args.reload:
            FileSetRows = reload_filesets.Build_FileSets(self)
            if len(FileSetRows) > 0:
                os_services.info(self, f"Reload of FileSets in BackupList.xlsx loaded {len(FileSetRows)} rows.")
            else:
                os_services.error(self, f"Reload of FileSets in BackupList.xlsx failed.")

        elif self.args.upd_general:
            updg_rc = updg.Collect_General_Files(self)
            if updg_rc > 0:
                os_services.info(self, f"Update of General folder loaded {updg_rc} rows.")
            else:
                os_services.error(self, f'Update of General files has failed.')

        elif self.args.refresh_sizes:
            file_sizes_rc = file_sizes.Collect_file_sizes(self)
            if file_sizes_rc > 0:
                os_services.info(self, f"File Size Refresh loaded {file_sizes_rc} rows.")
            else:
                os_services.error(self, f'Update of File Sizes refresh has failed.')

        elif self.args.run_frequency:
            os_services.info(self, f'Backing up host {socket.gethostname()}.\n')
            self.BackupSet_AoD, self.StorageSet_AoD, self.FileSet_AoD = excel_conv.excel_convert(self)
            self.backup_start(self.args.run_frequency)
            os_services.info(self, f'Completed {socket.gethostname()} backup')

        else:
            print(f"Missing a run type parameter of -reload, -upd_general, -refresh_sizes or -run_frequency. Exiting.")
            sys.exit(1)

    def backup_start(self, run_frequency):
        backup_list_in = self.BackupSet_AoD

        # loop through backup_sets
        for index in range(len(backup_list_in)):
            backup_set_name = ""
            file_set_name = ""
            storage_path = ""
            backup_versions = 1
            frequency = ""
            include_files_list = []
            exclude_files_list = []
            recurse = ""
            skipping = True
            for key in backup_list_in[index]:  # loop through backup set key fields
                if key == "BackupSetName":
                    backup_set_name = backup_list_in[index][key]
                    os_services.info(self, f'Checking BackupSet \'{backup_set_name}\' ')
                elif key == "StorageSetName":
                    storage_path = self.storage_path_getter(backup_list_in[index][key])
                    if storage_path is None:
                        os_services.warn(self, "Empty StoragePath. Skipping BackupSet")
                        break
                elif key == "FileSetName":
                    include_files_list = self.fileset_includes_getter(backup_list_in[index][key])
                    exclude_files_list = self.fileset_excludes_getter(backup_list_in[index][key])
                    recurse = self.fileset_recurse_getter(backup_list_in[index][key])
                    file_set_name = backup_list_in[index][key]
                elif key == "Frequency" and run_frequency.upper() == str(backup_list_in[index][key]).upper():
                    frequency = str(backup_list_in[index][key]).upper()
                    skipping = False
                elif key == "Versions":
                    backup_versions = backup_list_in[index][key]
                else:
                    pass

            try:
                if skipping:
                    os_services.warn(self, f" Skipping Backup Set {backup_set_name}"
                                           f" as it is not scheduled for today.\n")
                    continue
                elif not os.path.exists(storage_path):
                    os_services.warn(self, f"StoragePath {storage_path} is not mounted. Skipping BackupSet\n")
                    continue
                else:
                    os_services.info(self, f' FileSet: {file_set_name} ')
                    os_services.info(self, f' StoragePath: {storage_path}')
                    os_services.debug(self, f' Frequency: {frequency}')
                    os_services.debug(self, f'  Includes: {include_files_list} ')
                    os_services.debug(self, f'  Excludes: {exclude_files_list}')
                    os_services.debug(self, f'  Recurse: {recurse}')
            except Exception as ex:
                os_services.error(self, f"Exception with BackupSet {backup_set_name}. {ex}")
                os_services.error(self, f' FileSet: {file_set_name} ')
                os_services.error(self, f' StoragePath: {storage_path}')
                os_services.error(self, f' Frequency: {frequency}')
                os_services.error(self, f'  Includes: {include_files_list} ')
                os_services.error(self, f'  Excludes: {exclude_files_list}')
                os_services.error(self, f'  Recurse: {recurse}')
                continue

            # remove any excluded files from the includes list
            if len(exclude_files_list) > 0:
                for excl in exclude_files_list:
                    if excl in include_files_list:
                        include_files_list.remove(excl)

            # Determine the archive file name based on the current versions
            archive_target_basefile = os.path.join(storage_path, backup_set_name, f'{backup_set_name}')
            os_services.debug(self, f"Searching for the number of {archive_target_basefile}* files")
            os_services.debug(self, f"  keeping only {backup_versions} versions")
            archive_builder = tfb.Target_File_Builder(f'{archive_target_basefile}', backup_versions)
            archive_file = archive_builder.archive_target_file
            archive_rc = self.write_tar_file(archive_file, include_files_list, recurse)
            os_services.info(self, f'Back up of Backup Set Name {backup_set_name} '
                                   f'into {archive_file} '
                                   f'returned {archive_rc}\n')

    def storage_path_getter(self, storageSet_needle):
        storagesets_in = self.StorageSet_AoD

        for index in range(len(storagesets_in)):
            for key in storagesets_in[index]:
                if key == "StorageSetName" and storagesets_in[index]['StorageSetName'] == storageSet_needle:
                    return storagesets_in[index]["StoragePath"]

    def fileset_includes_getter(self, filesetname_needle):
        filesets_in = self.FileSet_AoD
        fs_includes = []

        for index in range(len(filesets_in)):
            for key in filesets_in[index]:
                if key == "FileSetName" and filesets_in[index]["FileSetName"] == filesetname_needle:
                    if os.path.exists(filesets_in[index]["Includes"]):
                        fs_includes.append(filesets_in[index]["Includes"])
                    else:
                        msg = f'  File Set {filesets_in[index]["Includes"]} does not exist. Remove it from' \
                              f' FileSets sheet in BackupList.xlsx '
                        os_services.warn(self, msg)
        return fs_includes

    def fileset_excludes_getter(self, filesetname_needle):
        filesets_in = self.FileSet_AoD
        fs_excludes = []

        for index in range(len(filesets_in)):
            for key in filesets_in[index]:
                if "FileSetName" in key and filesetname_needle in filesets_in[index][key]:
                    expaths = None
                    for expath in str(filesets_in[index]["Excludes"]).split(","):
                        if os.path.exists(expath):
                            if expaths is None:
                                expaths = f'{expath}'
                            else:
                                expaths = f'{expaths}, {expath}'
                    fs_excludes.append(expaths)

        return fs_excludes

    def fileset_recurse_getter(self, filesetname_needle):
        filesets_in = self.FileSet_AoD
        fs_recurse = False

        for index in range(len(filesets_in)):
            for key in filesets_in[index]:
                if key == "FileSetName" and filesets_in[index]["FileSetName"] == filesetname_needle:
                    if str(filesets_in[index]["Recurse"]).upper() == "YES":
                        fs_recurse = True
        return fs_recurse

    @staticmethod
    def is_file_older_than_x_days(file, days=1):
        file_time = os.path.getmtime(file)
        # Check against 24 hours
        return (time.time() - file_time) / 3600 > 24 * days

    def write_tar_file(self, target, sources, recursive):
        """ Tar and compress the sources into the target """
        if recursive is None:
            recursive = False
        try:
            with tarfile.open(target, 'w:gz') as tar_out:
                for src in sources:
                    os_services.debug(self, f'Processing {src} into backup')
                    tar_out.add(src, recursive=recursive)

            tar_out.close()
            return 0
        except OSError as oserr:
            return oserr


# =================================
if __name__ == '__main__':
    obj = PythonBackup()
    args = obj.parseCommandLine()
    obj.getLogger()
    obj.display_template(sys.argv[1:], args)
    obj.run_PythonBackup()
    obj.closelogfile()
