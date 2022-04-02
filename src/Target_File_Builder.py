import os
import re
import sys

from CommonLogger import LoggerServices as logger_services
from CommonOs import OsServices as os_services


class Target_File_Builder(os_services):
    """
        This class contains the  methods to roll a provided number of files to archive.
    """

    __author__ = "Barry Onizak"
    __version__ = "20220401.1"

    # # # # # End of header # # # #
    def __init__(self, archive_target_file, versions):
        super().__init__()
        self.versions = versions
        self.archive_target_file = archive_target_file
        self.create_target_file()

    def create_target_file(self):
        archive_target_filename_path = os.path.dirname(self.archive_target_file)
        archive_target_basename = os.path.basename(self.archive_target_file)
        archive_target_basename = archive_target_basename.split('_')[0]
        logger_services.debug(self, f'Looking for {archive_target_basename} files in {archive_target_filename_path}')

        # remove any excessive archive target files
        if os.path.isdir(archive_target_filename_path):
            atf_list = self.atfp_scan(archive_target_filename_path)
            while len(atf_list) >= self.versions:
                if len(atf_list) > 0:
                    # equal to or exceeded versions count - delete the oldest file
                    atf_eldest = os.path.join(archive_target_filename_path, sorted(atf_list)[0])
                    logger_services.debug(self, f'Deleting {atf_eldest}')
                    try:
                        os.remove(atf_eldest)
                    except OSError as oserr:
                        os_services.error(self, f'Error {oserr} trying to delete {atf_eldest}')
                        sys.exit(1)
                    atf_list = self.atfp_scan(archive_target_filename_path)
                else:
                    logger_services.debug(self, f'No previous files exist.')
        else:
            os.makedirs(archive_target_filename_path)

        self.archive_target_file = os.path.join(
            archive_target_filename_path, f'{archive_target_basename}_{self.file_date()}.tgz')
        logger_services.debug(self, f'New archive target file is {self.archive_target_file}')
        return self.archive_target_file

    def atfp_scan(self, archive_target_filename_path):
        archive_target_basename = os.path.basename(self.archive_target_file)
        if '_' in archive_target_basename:
            archive_target_basename = archive_target_basename.split('_')[0]

        atf_list = []

        with os.scandir(archive_target_filename_path) as atfp_scan:
            for entry in atfp_scan:
                if not entry.name.startswith('.') and entry.is_file():
                    if re.search(rf'^{archive_target_basename}', entry.name):
                        atf_list.append(entry.name)
            logger_services.debug(self, f'{len(atf_list)} files found')
            for atf in atf_list:
                logger_services.debug(self, f'  {atf}')
        return atf_list
