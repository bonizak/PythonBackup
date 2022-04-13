import os.path

import psycopg2
from configparser import ConfigParser
from CommonOs import OsServices as os_services


class CommonDB(os_services):
    """
    This class contains the methods to read the PostgreSQL BackupListDB and
    populate the arrays of dictionaries for each table

    Args
        Required: none
        Optional: none

    Alerts: Critical | WARN | ERROR

    Logging: none

    """

    __author__ = "Barry Onizak"
    __version__ = "20220410.1"

    # # # # # End of header # # # #
    BackupSet_AoD = []
    StorageSet_AoD = []
    FileSet_AoD = []
    Frequency_AOD = []

    def dbSetsCollect(self):

        dbConn = obj.dbConnect()
        self.dbGetBackupSets(dbConn)
        self.dbGetStorageSets(dbConn)
        self.dbGetFileSets(dbConn)
        self.dbGetFrequency(dbConn)
        return self.BackupSet_AoD, self.StorageSet_AoD, self.FileSet_AoD, self.Frequency_AOD

    def dbConnect(self):
        """ Connect to the PostgreSQL database server """
        dbConn = None
        try:
            # read connection parameters
            params = self.dbParser('../resource/database.ini', 'postgresql')

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database..')
            dbConn = psycopg2.connect(**params)

            # create a cursor
            cur = dbConn.cursor()

            # execute a statement
            cur.execute('SELECT version()')
            # display the PostgreSQL database server version
            print(f'PostgreSQL database version {cur.fetchone()[0]}')

            cur.execute("SELECT current_database()")
            print(f'Current database name {cur.fetchone()[0]}')

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if dbConn is not None:
                return dbConn

    def dbGetBackupSets(self, dbConn):
        try:
            cur = dbConn.cursor()
            sql = f'SELECT "b"."ID", "b"."BackupSetName", "b"."Versions", ' \
                  f' "b"."StorageSetID", ' \
                  f' "b"."FileSetID", ' \
                  f' "b"."FrequencyID" ' \
                  f'FROM "BKUP"."BackupSets" "b" ' \
                  f'ORDER BY "b"."ID" ASC'

            # f' INNER JOIN "BKUP"."StorageSets" "s" on "b"."StorageSetID" = "s"."ID" ' \
            # f' INNER JOIN "BKUP"."FileSets" "f" on "b"."FileSetID" = "f"."ID" ' \
            # f' INNER JOIN "BKUP"."Frequencies" "q" on "b"."FrequencyID" = "q"."ID" ' \
            cur.execute(sql)
            rowCount = cur.rowcount

            while rowCount > 0:
                rowData = cur.fetchone()
                row_set_dict = {"ID": rowCount, "BackupSetName": rowData[1], "Versions": rowData[2],
                                "StorageSetID": rowData[3], "FileSetID": rowData[4], "FrequencyID": rowData[5]}
                self.BackupSet_AoD.append(row_set_dict)
                rowCount -= 1

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if dbConn is None:
                dbConn.close()

    def dbGetStorageSets(self, dbConn, ssid):
        try:
            cur = dbConn.cursor()
            sql = f'SELECT "s"."ID", "s"."StorageSetname", "s"."StoragePath", "s"."DevicePathId" ' \
                  f'FROM "BKUP"."StorageSets" "s" ' \
                  f'WHERE "s"."ID" = {ssid}' \
                  f'ORDER BY "s"."ID" ASC'

            cur.execute(sql)
            rowCount = cur.rowcount

            while rowCount > 0:
                rowData = cur.fetchone()
                row_set_dict = {"ID": rowCount, "StorageSetName": rowData[1], "StorageSetPath": rowData[2],
                                "DevicePathID": rowData[3]}
                self.StorageSet_AoD.append(row_set_dict)
                rowCount -= 1

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if dbConn is None:
                dbConn.close()

    def dbGetFileSets(self, dbConn, fsid):
        try:
            cur = dbConn.cursor()
            sql = f'SELECT "f"."ID", "f"."FileSetName", ' \
                  f'"f"."Includes", "f"."Excludes", ' \
                  f'"f"."Compress", "f"."Recursive" ' \
                  f'FROM "BKUP"."FileSets" "f"  ' \
                  f'WHERE "f"."ID" = {fsid}' \
                  f'ORDER BY "f"."ID" ASC'

            cur.execute(sql)
            rowCount = cur.rowcount

            while rowCount > 0:
                rowData = cur.fetchone()
                row_set_dict = {"ID": rowCount, "FileSetName": rowData[1],
                                "Includes": rowData[2], "Excludes": rowData[3],
                                "Compress": rowData[4],  "Compress": rowData[5]}
                self.FileSet_AoD.append(row_set_dict)
                rowCount -= 1

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if dbConn is None:
                dbConn.close()

    def dbGetFrequency(self, dbConn, qid):
        try:
            cur = dbConn.cursor()
            sql = f'SELECT "q"."ID", "q"."Frequency", ' \
                  f'FROM "BKUP"."Frequencies" "q"  ' \
                  f'WHERE "q"."ID" = {qid}' \
                  f'ORDER BY "q"."ID" ASC'

            cur.execute(sql)
            rowCount = cur.rowcount

            while rowCount > 0:
                rowData = cur.fetchone()
                row_set_dict = {"ID": rowCount, "Frequency": rowData[1]}
                self.Frequency_AOD.append(row_set_dict)
                rowCount -= 1

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if dbConn is None:
                dbConn.close()

    def dbParser(self, filename, section):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db


# =================================
if __name__ == '__main__':
    obj = CommonDB()
    conn = obj.dbConnect()
    obj.dbGetBackupSets(conn)
    obj.dbGetStorageSets(conn)
    obj.dbGetFileSets(conn)
