import json
import os
import pandas as pd
from CommonLogger import LoggerServices as logger_services


class JSON_Convert(logger_services):
    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")

    def convert_excel2json(self):
        convert_rc = False
        try:
            excel_file = os.path.join(self.resource_path, 'BackupList.xlsx')
            if os.path.exists(excel_file):
                self.xcel_2_json(excel_file, 'BackupSets', 'A:F')
                self.xcel_2_json(excel_file, 'StorageSets', 'A:C')
                self.xcel_2_json(excel_file, 'FileSets', 'A:F')
                return True
            else:
                raise FileNotFoundError
        except FileNotFoundError as ex:
            msg = f'No such File or Directory {excel_file}'
            logger_services.error(self, msg)
            return False

    def convert_json2excel(self):
        convert_rc = False
        try:
            resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")
            self.new_j2excel(f'{self.resource_path}/BackupSets.json')
            self.new_j2excel(f'{self.resource_path}/StorageSets.json')
            self.new_j2excel(f'{self.resource_path}/FileSets.json')
            return True
        except FileNotFoundError as ex:
            msg = f'No such File'
            print(msg)
            return False

    def xcel_2_json(self, excel_in, sheet_in, cols_in):
        if os.path.exists(os.path.abspath(excel_in)):
            excel_data_df = pd.read_excel(excel_in, sheet_name=sheet_in, usecols=cols_in)
            json_data = excel_data_df.to_json(orient='index')
            json_object = json.loads(json_data)

            with open(os.path.abspath(os.path.join(self.resource_path, f'{sheet_in}.json')), 'w') as jsonout:
                json.dump(json_object, jsonout, indent=5, sort_keys=False)
                print(f'Wrote {sheet_in}.json')

    def json_2_xcel(self, json_in):
        if os.path.exists(json_in):
            excel_sheet = os.path.basename(json_in)
            excel_file = os.path.join(os.path.join(self.resource_path, f'{excel_sheet}.xlsx'))
            with open(json_in) as json_file:
                json_in = json.load(json_file)
            df = pd.json_normalize(json_in)
            df.to_excel(excel_file, sheet_name=excel_sheet, index=False)
