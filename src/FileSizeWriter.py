import os

import pandas as pd
from openpyxl import load_workbook


class FSWriter:
    """
    This class contains the methods to read a sheet and write the file and folders listed there
    into another sheet with the size of the files or folders
    """
    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")

    def runit(self):
        FileSizeRows = []
        IncludesRead = self.read_fs_in()
        row_set_count = 0

        for index in range(len(IncludesRead)):
            for key in IncludesRead[index]:
                key_size = 0
                FileSizeRow = {}
                if key == "Includes" and os.path.isdir(IncludesRead[index][key]):
                    key_size = self.getFolderSize(IncludesRead[index][key])
                    print(f' Dir {IncludesRead[index][key]} is {key_size}')
                    FileSizeRow["Index"] = row_set_count
                    FileSizeRow["Path"] = IncludesRead[index][key]
                    FileSizeRow["Size"] = key_size
                    FileSizeRows.append(FileSizeRow)
                    row_set_count += 1
                elif key == "Includes" and os.path.isfile(IncludesRead[index][key]):
                    key_size = os.stat(IncludesRead[index][key]).st_size
                    print(f' File {IncludesRead[index][key]} is {key_size}')
                    FileSizeRow["Index"] = row_set_count
                    FileSizeRow["Path"] = IncludesRead[index][key]
                    FileSizeRow["Size"] = key_size
                    FileSizeRows.append(FileSizeRow)
                    row_set_count += 1
                else:
                    pass

        wfs_rc = self.write_fs(FileSizeRows)
        print(f' \nCaptured {len(IncludesRead)} file sets')

    def getFolderSize(self, folder):
        total_size = os.path.getsize(folder)
        for item in os.listdir(folder):
            itempath = os.path.join(folder, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += self.getFolderSize(itempath)
        return total_size

    def read_fs_in(self):
        """
        This method reads in a sheet and writes the specific columns into an array of dictionaries
        """
        resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")
        wb = load_workbook(os.path.join(self.resource_path, "BackupList.xlsx"))
        sheetset = {'FileSets': 3}
        IncludesRead = []

        for ws in wb:
            if ws.title in sheetset.keys():
                worksheet = wb[ws.title]

                row_sets = [worksheetsets for worksheetsets in worksheet.iter_rows(
                    min_row=2, max_col=sheetset[ws.title], min_col=1, values_only=True)
                            if None not in worksheetsets]
                row_set_count = 0
                for row_set in row_sets:
                    row_set_dict = {}
                    if worksheet.title == "FileSets":
                        for index in range(len(row_set)):
                            if index == 0:
                                row_set_dict["Index"] = row_set_count
                            elif index == 1:
                                row_set_dict["FileSetName"] = row_set[index]
                            elif index == 2:
                                row_set_dict["Includes"] = row_set[index]
                            else:
                                raise AttributeError

                        IncludesRead.append(row_set_dict)
                        row_set_count += 1
        return IncludesRead

    def write_fs(self, fs_dict):
        """
        This method writes a supplied dictionary to the FileSizes sheet of the BackupList.xlsx workbook using pandas.
        :param fs_dict:
        :return:
        """
        wb = load_workbook(os.path.join(self.resource_path, "BackupList.xlsx"))
        writer = pd.ExcelWriter(os.path.join(self.resource_path, "BackupList.xlsx"), engine='openpyxl')
        writer.book = wb
        writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)

        df = pd.DataFrame(data=fs_dict)
        df.to_excel(writer, sheet_name="FileSizes", startcol=0, startrow=0,
                    columns=['Path', 'Size'],
                    index_label='Index')
        writer.save()
        return df.size
