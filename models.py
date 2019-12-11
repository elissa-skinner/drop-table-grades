import pymysql.cursors
import csv
from service import *
from dbcsv import read_csv_file as read_csv
from dbcsv import parse_experiment_id as parse_experiment_id
from dbcsv import str_is_bool
from dbcsv import str_is_float
from dbcsv import  str_is_int

DICT_OF_NAMES = {"CONDITION": "Condition Name ",
                 "MEASUREMENT": "Measurement Name ",
                 "SEQUENCE": "Sequence Name ",
                 "EXPERIMENT": "Experiment Name ",
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
            return "ERROR"

        try:
            query = "INSERT INTO conditions (cond_name, type) " \
                    "VALUES (\"" + results[DICT_OF_NAMES["CONDITION"]] + \
                    "\", \"" + results[DICT_OF_NAMES["TYPE"]] + "\")"

            self.cursor.execute(query)

            self.connection.commit()

        except Exception as e:
            print(str(e))

    def insert_new_measurement(self, results):
        if DICT_OF_NAMES["MEASUREMENT"] not in results \
                or DICT_OF_NAMES["TYPE"] not in results:
            print("ERROR - improper elements in dict")
            return "ERROR"

        try:
            query = "INSERT INTO measurements (meas_name, type) " \
                    "VALUES (\"" + results[DICT_OF_NAMES["MEASUREMENT"]] + \
                    "\", \"" + results[DICT_OF_NAMES["TYPE"]] + "\")"

            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            return str(e)

    def insert_new_sequence(self, results):
        if DICT_OF_NAMES["SEQUENCE"] not in results:
            print("ERROR - improper elements in dict")
            return "ERROR"

        try:
            query = "INSERT INTO sequences (seq_name, filename, description) " \
                    "VALUES (%s, %s, %s)"

            vals = [results[DICT_OF_NAMES["SEQUENCE"]],
                    results[DICT_OF_NAMES["FILENAME"]] if DICT_OF_NAMES["FILENAME"] in results else None,
                    results[DICT_OF_NAMES["DESCRIPTION"]] if DICT_OF_NAMES["DESCRIPTION"] in results else None]

            self.cursor.execute(query, vals)
            self.connection.commit()

        except Exception as e:
            return str(e)

    def is_exp(self, exp_id):
        try:
            self.cursor.execute("SELECT * FROM experiments WHERE exp_id = \"" + exp_id + "\"")
            return len(self.cursor.fetchall()) != 0

        except Exception as e:
            print(str(e))

    def insert_new_experiment(self, results):
        experiment_id = results[DICT_OF_NAMES["EXPERIMENT"]]
        parse_experiment_id(self.connection, self.cursor, experiment_id)

        all_measurements_found = True

        for measurement in results:
            if measurement != DICT_OF_NAMES["EXPERIMENT"]:
                meas_val = results[measurement]
                self.cursor.execute("SELECT * FROM measurements WHERE meas_name = %s;", (measurement,))
                tuples = self.cursor.fetchall()

                if len(tuples) == 0:
                    print("Measurement " + measurement + " is not stored in the database."
                                                         " Please enter its information in the gui.")
                    all_measurements_found = False
                    break

                measurement_type = tuples[0][1]
                if meas_val is None or meas_val == "":
                    continue

                if measurement_type == "int":
                    if not str_is_int(meas_val):
                        err_msg = "Value for measurement " + measurement + " of " + meas_val + " is not an int."
                        print(err_msg)
                        return err_msg
                if measurement_type == "bool":
                    if not str_is_bool(meas_val):
                        err_msg = "Value for measurement " + measurement + " of " + meas_val + " is not a bool."
                        print(err_msg)
                        return err_msg
                if measurement_type == "float":
                    if not str_is_float(meas_val):
                        err_msg = "Value for measurement " + measurement + " of " + meas_val + " is not a float."
                        print(err_msg)
                        return err_msg
                try:
                    self.cursor.execute("INSERT INTO experiment_measurements "
                                   "VALUES (%s,%s,%s);", (experiment_id, measurement, meas_val))
                    self.connection.commit()
                except Exception as e:
                    return str(e)

                if not all_measurements_found:
                    break

        if not all_measurements_found:
            print("Processing stopped because invalid measurement was found.")
            return "Processing stopped because invalid measurement was found."

    def get_meas_from_db(self):
        try:
            self.cursor.execute("SELECT * FROM measurements")
            return self.cursor.fetchall()

        except Exception as e:
            print(str(e))

    def read_csv_file(self, results):
        if DICT_OF_NAMES["CSV"] not in results:
            print("ERROR - improper elements in dict")
            return "ERROR"

        return read_csv(self.connection, self.cursor, results[DICT_OF_NAMES["CSV"]])

    def side_by_side(self, exp1, exp2):
        try:
            query = "SELECT E1.meas_name, E1.meas_val, E2.meas_val " \
                    "FROM experiment_measurements E1, experiment_measurements E2 " \
                    "WHERE E1.exp_id = \"" + exp1 + "\" " \
                    "AND E2.exp_id = \"" + exp2 + "\" " \
                    "AND E1.meas_name = E2.meas_name"
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Exception as e:
            print(str(e))
