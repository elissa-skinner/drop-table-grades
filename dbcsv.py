import csv
import service


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


def parse_experiment_id(connection, cursor, experiment_id, statements):
    experiment_tokens = experiment_id.split('_')

    seq_name = experiment_tokens[0]
    experiment_tokens = experiment_tokens[1:]

    cursor.execute("SELECT * FROM sequences s WHERE s.seq_name = %s;", (seq_name,))
    tuples = cursor.fetchall()

    if len(tuples) == 0:
        print("Sequence " + seq_name + " is not stored in the database."
                                       " Please enter its information in the gui.")
        return "Bad sequence"

    statements.append("INSERT INTO experiments VALUES ('%s','%s')" % (experiment_id, seq_name))

    all_conditions_found = True
    for j in range(0, len(experiment_tokens), 2):
        condition = experiment_tokens[j]
        condition_value = experiment_tokens[j + 1]

        cursor.execute("SELECT * FROM conditions c WHERE c.cond_name = %s;", (condition,))
        tuples = cursor.fetchall()
        if len(tuples) == 0:
            print("Condition " + condition + " is not stored in the database. "
                                             "Please enter its information in the gui.")
            return "Bad condition"

        condition_type = tuples[0][1]
        if condition_type == "Integer":
            if not str_is_int(condition_value):
                print("Value for condition " + condition + " of " + condition_value + " is not an int.")
                return "Bad condition"
        elif condition_type == "Boolean":
            if not str_is_bool(condition_value):
                print("Value for condition " + condition + " of " + condition_value + " is not a bool.")
                return "Bad condition"
        elif condition_type == "Float":
            if not str_is_float(condition_value):
                print("Value for condition " + condition + " of " + condition_value + " is not a float.")
                return "Bad condition"

        # condition is now verified
        statements.append("INSERT INTO experiment_conditions "
                          "VALUES ('%s','%s','%s');" % (experiment_id, condition, condition_value))

    return "Good"


def read_csv_file(connection, cursor, csv_path):
    try:
        with open(csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            rows = [row for row in reader]

            start_row = rows[0]
            rows = rows[1:]
            all_seqs_found = True
            all_conditions_found = True

            statements = []

            for i in range(1, len(start_row)):
                experiment_id = service.reorder_exp(str(start_row[i]))
                result = parse_experiment_id(connection, cursor, experiment_id, statements)

                if result == "Bad sequence":
                    all_seqs_found = False
                    break
                if result == "Bad condition":
                    all_conditions_found = False
                    break

            if not all_seqs_found:
                print("Processing stopped because invalid sequence was found.")
                return "Invalid sequence found"
            elif not all_conditions_found:
                print("Processing stopped because invalid condition was found.")
                return "Invalid condition found"

            try:
                connection.commit()
            except Exception as e:
                return str(e)

            all_measurements_found = True

            for row in rows:
                measurement = row[0]
                cursor.execute("SELECT * FROM measurements WHERE meas_name = %s;", (measurement,))
                tuples = cursor.fetchall()

                if len(tuples) == 0:
                    print("Measurement " + measurement + " is not stored in the database."
                                                         " Please enter its information in the gui.")
                    all_measurements_found = False
                    break

                measurement_type = tuples[0][1]
                for i in range(1, len(row)):
                    experiment_id = service.reorder_exp(start_row[i])
                    meas_val = row[i]

                    if meas_val is None or meas_val == "":
                        continue

                    if measurement_type == "Integer":
                        if not str_is_int(meas_val):
                            print("Value for measurement " + measurement + " of " + meas_val + " is not an int.")
                            all_measurements_found = False
                            break
                    if measurement_type == "Boolean":
                        if not str_is_bool(meas_val):
                            print("Value for measurement " + measurement + " of " + meas_val + " is not a bool.")
                            all_measurements_found = False
                            break
                    if measurement_type == "Float":
                        if not str_is_float(meas_val):
                            print("Value for measurement " + measurement + " of " + meas_val + " is not a float.")
                            all_measurements_found = False
                            break
                    try:
                        statements.append("INSERT INTO experiment_measurements "
                                          "VALUES ('%s','%s','%s');" % (experiment_id, measurement, meas_val))
                    except Exception as e:
                        return str(e)

                if not all_measurements_found:
                    break

            if not all_measurements_found:
                return "Invalid measurement value was found."

            for statement in statements:
                try:
                    cursor.execute(statement)
                    connection.commit()
                except Exception as e:
                    print(str(e))
    except Exception as e:
        return str(e)


