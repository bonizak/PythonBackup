import os

from openpyxl import *
from CommonOs import OsServices as os_services


class Excel_Converter(os_services):
    """This class contains the methods used read and write MS Excel files
    Args
        Required: none
        Optional: none

    Logging: DEBUG

    """

    __author__ = "Barry Onizak"
    __version__ = "20210814.1"
    # # # # # End of header # # # #

    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")
    BackupSet_AoD = []
    StorageSet_AoD = []
    FileSet_AoD = []

    def excel_convert(self):
        """
        Entry method to perform the purpose of the class

        :return: self.BackupSet_AoD[], self.StorageSet_AoD[], self.FileSet_AoD[]
        """

        wb = load_workbook(os.path.join(self.resource_path, "BackupList.xlsx"))
        sheetset = {'BackupSets': 6, 'StorageSets': 4, 'FileSets': 6}

        for ws in wb:
            if ws.title in sheetset.keys():
                worksheet = wb[ws.title]

                row_sets = [worksheetsets for worksheetsets in worksheet.iter_rows(
                    min_row=2, max_col=sheetset[ws.title], min_col=1, values_only=True)
                            if None not in worksheetsets]

                row_set_count = 0
                for row_set in row_sets:
                    row_set_dict = {}
                    if worksheet.title == "BackupSets":
                        for index in range(len(row_set)):
                            if index == 0:
                                row_set_dict["Index"] = row_set_count
                            elif index == 1:
                                row_set_dict["BackupSetName"] = row_set[index]
                            elif index == 2:
                                row_set_dict["StorageSetName"] = row_set[index]
                            elif index == 3:
                                row_set_dict["FileSetName"] = row_set[index]
                            elif index == 4:
                                row_set_dict["Versions"] = row_set[index]
                            elif index == 5:
                                row_set_dict["Frequency"] = row_set[index]
                            else:
                                raise AttributeError

                        self.BackupSet_AoD.append(row_set_dict)
                        row_set_count += 1

                    elif worksheet.title == "StorageSets":
                        for index in range(len(row_set)):
                            if index == 0:
                                row_set_dict["Index"] = row_set_count
                            elif index == 1:
                                row_set_dict["StorageSetName"] = row_set[index]
                            elif index == 2:
                                row_set_dict["StoragePath"] = row_set[index]
                            elif index == 3:
                                row_set_dict["DeviceType"] = row_set[index]
                            else:
                                raise AttributeError

                        self.StorageSet_AoD.append(row_set_dict)
                        row_set_count += 1

                    elif worksheet.title == "FileSets":
                        for index in range(len(row_set)):
                            if index == 0:
                                row_set_dict["Index"] = row_set_count
                            elif index == 1:
                                row_set_dict["FileSetName"] = row_set[index]
                            elif index == 2:
                                row_set_dict["Includes"] = row_set[index]
                            elif index == 3:
                                row_set_dict["Excludes"] = row_set[index]
                            elif index == 4:
                                row_set_dict["Compress"] = row_set[index]
                            elif index == 5:
                                row_set_dict["Recurse"] = row_set[index]
                            else:
                                raise AttributeError

                        self.FileSet_AoD.append(row_set_dict)
                        row_set_count += 1

        os_services.debug(self, f' read {len(self.BackupSet_AoD)} Backup sets')
        os_services.debug(self, f' read {len(self.StorageSet_AoD)} Storage sets')
        os_services.debug(self, f' read {len(self.FileSet_AoD)} File sets')
        return self.BackupSet_AoD, self.StorageSet_AoD, self.FileSet_AoD
