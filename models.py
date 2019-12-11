import pymysql.cursors
import csv
from service import *

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
        if DICT_OF_NAMES["CSV"] not in results:
            print("ERROR - improper elements in dict")
            return

        with open(results[DICT_OF_NAMES["CSV"]], 'r') as csv_file:
            reader = csv.reader(csv_file)
            rows = [row for row in reader]

            start_row = rows[0]
            rows = rows[1:]
            all_seqs_found = True

            for i in range(1, len(start_row)):
                experiment_id = str(start_row[i])
                experiment_tokens = experiment_id.split('_')

                seq_name = experiment_tokens[0]
                experiment_tokens = experiment_tokens[1:]

                self.cursor.execute("SELECT * FROM sequences s WHERE s.seq_name = '" + seq_name + "'")
                tuples = self.cursor.fetchall()

                if len(tuples) == 0:
                    print("Sequence " + seq_name + " is not stored in the database."
                                                   " Please enter its information in the gui.")
                    all_seqs_found = False
                    break

                try:
                    self.cursor.execute("INSERT INTO experiments "
                                        "VALUES ('" + experiment_id + "', '" + seq_name + "')")
                except Exception as e:
                    print(str(e))

                all_conditions_found = True
                for j in range(0, len(experiment_tokens), 2):
                    condition = experiment_tokens[j]
                    condition_value = experiment_tokens[j + 1]

                    self.cursor.execute("SELECT * FROM conditions c WHERE c.cond_name = '" + condition + "'")
                    tuples = self.cursor.fetchall()
                    if len(tuples) == 0:
                        print("Condition " + condition + " is not stored in the database. "
                                                         "Please enter its information in the gui.")
                        all_conditions_found = False
                        break

                    condition_type = tuples[0][1]
                    if condition_type == "int":
                        if not str_is_int(condition_value):
                            print("Value for condition " + condition + " of " + condition_value + " is not an int.")
                            all_conditions_found = False
                            break
                    elif condition_type == "bool":
                        if not str_is_bool(condition_value):
                            print("Value for condition " + condition + " of " + condition_value + " is not a bool.")
                            all_conditions_found = False
                            break
                    elif condition_type == "float":
                        if not str_is_float(condition_value):
                            print("Value for condition " + condition + " of " + condition_value + " is not a float.")
                            all_conditions_found = False
                            break

                    # condition is now verified
                    try:
                        self.cursor.execute("INSERT INTO experiment_conditions "
                                            "VALUES ('" + experiment_id + "', '" + condition + "', '"
                                            + condition_value + "')")
                    except Exception as e:
                        print(str(e))

                if not all_conditions_found:
                    break

            if not all_seqs_found:
                print("Processing stopped because invalid sequence was found.")
                return
            elif not all_conditions_found:
                print("Processing stopped because invalid condition was found.")
                return

            try:
                self.connection.commit()
            except Exception as e:
                print(str(e))

            all_measurements_found = True

            for row in rows:
                measurement = row[0]
                self.cursor.execute("SELECT * FROM measurements WHERE meas_name = '" + measurement + "'")
                tuples = self.cursor.fetchall()

                if len(tuples) == 0:
                    print("Measurement " + measurement + " is not stored in the database."
                                                         " Please enter its information in the gui.")
                    all_measurements_found = False
                    break

                measurement_type = tuples[0][1]
                for i in range(1, len(row)):
                    experiment_id = start_row[i]
                    meas_val = row[i]

                    if meas_val is None or meas_val == "":
                        continue

                    if measurement_type == "int":
                        if not str_is_int(meas_val):
                            print("Value for measurement " + measurement + " of " + meas_val + " is not an int.")
                            all_measurements_found = False
                            break
                    if measurement_type == "bool":
                        if not str_is_bool(meas_val):
                            print("Value for measurement " + measurement + " of " + meas_val + " is not a bool.")
                            all_measurements_found = False
                            break
                    if measurement_type == "float":
                        if not str_is_float(meas_val):
                            print("Value for measurement " + measurement + " of " + meas_val + " is not a float.")
                            all_measurements_found = False
                            break
                    try:
                        self.cursor.execute("INSERT INTO experiment_measurements "
                                            "VALUES ('" + experiment_id + "', '" + measurement + "' ,'"
                                            + meas_val + "')")
                        self.connection.commit()
                    except Exception as e:
                        print(str(e))

                if not all_measurements_found:
                    break

            if not all_measurements_found:
                print("Processing stopped because invalid measurement was found.")
