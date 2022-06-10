import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

from logger.Logger import Logger
from models.Credentials import Credentials
from services.interfaces.PersistenceFactory import PersistenceFactory


class MySqlPersistenceService(PersistenceFactory):

    def __init__(self, databaseName, tableName):
        self.databaseName = databaseName
        self.tableName = tableName

    def verifyDatabaseConnectivity(self, credentials: Credentials):
        try:
            connection = msql.connect(
                host=credentials.host,
                user=credentials.user,
                password=credentials.password)

            if connection.is_connected():
                Logger.log(
                    "Verified connection to database: '{}'".format(
                        self.databaseName))

        except Error as e:
            Logger.logError("Error while connecting to MySQL: {}".format(e))

    def feedDatabase(self, dataframe, credentials: Credentials):
        try:
            connection = msql.connect(
                host=credentials.host,
                user=credentials.user,
                password=credentials.password)

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("use {};".format(self.databaseName))
                cursor.execute("select database();")
                record = cursor.fetchone()[0]

                for i, row in dataframe.iterrows():
                    sql = "INSERT INTO {}.{} VALUES (%s, %s, %s, %s)".format(
                        self.databaseName, self.tableName)
                    cursor.execute(sql, tuple(row))
                    Logger.log(
                        "Record {}/{} inserted into database.".format(i + 1, len(dataframe)))
                    connection.commit()

        except Error as e:
            Logger.logError("Error while connecting to MySQL: {}".format(e))

    def getAllFromTable(self, credentials: Credentials):
        try:
            connection = msql.connect(
                host=credentials.host,
                user=credentials.user,
                password=credentials.password)

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("use {};".format(self.databaseName))
                cursor.execute("select database();")
                record = cursor.fetchone()[0]

                sql = "SELECT * from {};".format(self.tableName)
                tableRecords = pd.read_sql(sql, connection)
                print(tableRecords)

        except Error as e:
            Logger.logError("Error while connecting to MySQL: {}".format(e))

    def cleanTable(self, credentials: Credentials):
        try:
            connection = msql.connect(
                host=credentials.host,
                user=credentials.user,
                password=credentials.password)

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("use {};".format(self.databaseName))
                cursor.execute("select database();")
                record = cursor.fetchone()[0]

                sql = "DELETE FROM {};".format(self.tableName)
                cursor.execute(sql)
                connection.commit()

                result = cursor.fetchall()
                for i in result:
                    Logger.log(i)

        except Error as e:
            Logger.logError("Error while connecting to MySQL: {}".format(e))
