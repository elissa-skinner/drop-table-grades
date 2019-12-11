import pymysql.cursors
import csv
from service import *
from dbcsv import read_csv_file as read_csv

DICT_OF_NAMES = {"CONDITION": "Condition Name ",
                 "MEASUREMENT": "Measurement Name ",
                 "SEQUENCE": "Sequence Name ",
                 "EXPERIMENT": "Measurement Value",
                 "CSV": "CSV File Name ",
                 "TYPE": "Type",
                 "FILENAME": "Sequence File ",
                 "DESCRIPTION": "Sequence Description "}


class DB_Connection:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          port=3306,
                                          user='root',
                                          password='password',
                                          database='drop_table_grades')
        self.cursor = self.connection.cursor()

    def insert_new_condition(self, results):
        if DICT_OF_NAMES["CONDITION"] not in results \
                or DICT_OF_NAMES["TYPE"] not in results:
            print("ERROR - improper elements in dict")
            return

        try:
            query = "INSERT INTO conditions (cond_name, type) " \
                    "VALUES (\"" + results[DICT_OF_NAMES["CONDITION"]] + \
                    "\", \"" + results[DICT_OF_NAMES["TYPE"]] + "\")"

            self.cursor.execute(query)

            self.connection.commit()

        except Exception as e:
            print(e)

    def insert_new_measurement(self, results):
        if DICT_OF_NAMES["MEASUREMENT"] not in results \
                or DICT_OF_NAMES["TYPE"] not in results:
            print("ERROR - improper elements in dict")
            return

        try:
            query = "INSERT INTO measurements (meas_name, type) " \
                    "VALUES (\"" + results[DICT_OF_NAMES["MEASUREMENT"]] + \
                    "\", \"" + results[DICT_OF_NAMES["TYPE"]] + "\")"

            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print(e)

    def insert_new_sequence(self, results):
        if DICT_OF_NAMES["SEQUENCE"] not in results:
            print("ERROR - improper elements in dict")
            return

        try:
            query = "INSERT INTO sequences (seq_name, filename, description) " \
                    "VALUES (%s, %s, %s)"

            vals = [results[DICT_OF_NAMES["SEQUENCE"]],
                    results[DICT_OF_NAMES["FILENAME"]] if DICT_OF_NAMES["FILENAME"] in results else None,
                    results[DICT_OF_NAMES["DESCRIPTION"]] if DICT_OF_NAMES["DESCRIPTION"] in results else None]

            self.cursor.execute(query, vals)
            self.connection.commit()

        except Exception as e:
            print(e)

    def read_csv_file(self, results):
        read_csv(self.connection, self.cursor, results)
