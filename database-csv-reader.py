import csv
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='password',
                             database='drop_table_grades')
cursor = connection.cursor()


def str_is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def str_is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def str_is_bool(s):
    if s == "T" or s == "F" or s == "0" or s == "1":
        return True
    else:
        return False


def read_csv_file(csv_path):
    with open(csv_path, 'r') as csv_file:
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

            cursor.execute("SELECT * FROM sequences s WHERE s.seq_name = '" + seq_name + "'")
            tuples = cursor.fetchall()

            if len(tuples) == 0:
                print("Sequence " + seq_name + " is not stored in the database."
                                               " Please enter its information in the gui.")
                all_seqs_found = False
                break

            try:
                cursor.execute("INSERT INTO experiments "
                               "VALUES ('" + experiment_id + "', '" + seq_name + "')")
            except Exception as e:
                print(str(e))

            all_conditions_found = True
            for j in range(0, len(experiment_tokens), 2):
                condition = experiment_tokens[j]
                condition_value = experiment_tokens[j + 1]

                cursor.execute("SELECT * FROM conditions c WHERE c.cond_name = '" + condition + "'")
                tuples = cursor.fetchall()
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
                    cursor.execute("INSERT INTO experiment_conditions "
                                   "VALUES ('" + experiment_id + "', '" + condition + "', '" + condition_value + "')")
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
            connection.commit()
        except Exception as e:
            print(str(e))

        all_measurements_found = True

        for row in rows:
            measurement = row[0]
            cursor.execute("SELECT * FROM measurements WHERE meas_name = '" + measurement + "'")
            tuples = cursor.fetchall()

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
                    cursor.execute("INSERT INTO experiment_measurements "
                                   "VALUES ('" + experiment_id + "', '" + measurement + "' ,'" + meas_val + "')")
                    connection.commit()
                except Exception as e:
                    print(str(e))

            if not all_measurements_found:
                break

        if not all_measurements_found:
            print("Processing stopped because invalid measurement was found.")


read_csv_file("example.csv")
