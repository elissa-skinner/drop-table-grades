from models import *

DICT_OF_NAMES = {"CONDITION": "Condition Name ",
                 "MEASUREMENT": "Measurement Name ",
                 "SEQUENCE": "Sequence Name ",
                 "EXPERIMENT": "Measurement Value ",
                 "CSV": "CSV File Name ",
                 "TYPE": "Type"}

db = DB_Connection()

'''
determine which query to preform from success page
'''
def insert_into_db(results):
    if DICT_OF_NAMES["CONDITION"] in results:
        db.insert_new_condition(results)
    elif DICT_OF_NAMES["MEASUREMENT"] in results:
        db.insert_new_measurement(results)
    elif DICT_OF_NAMES["SEQUENCE"] in results:
        db.insert_new_sequence(results)
    elif DICT_OF_NAMES["EXPERIMENT"] in results:


        db.insert_new_experiment(results)
    elif DICT_OF_NAMES["CSV"] in results:
        db.read_csv_file(results)

def compare_exp(results):
    exp1 = results["Experiment #1 "]
    exp2 = results["Experiment #2 "]
    if db.is_exp(exp1) and db.is_exp(exp2):
        print("good!")

def get_meas():
    return db.get_meas_from_db()

def get_exp(result):
    # parse result
    # get query
    # execute query
    print("getting result")
#    parse_seq(result[])

###########
# queries #
###########

'''
s: seq_name
c: {cond_name: cond_val}
query returns a list of experiment ids, measurement names, and measurement
values that contain the given sequence and condition values. The given
conditions may not be an exhaustive list for the conditions of a returned
experiment.
'''
def get_exp_info_query(s, c):
    query = "SELECT E.exp_id, meas_name, meas_val " \
            "FROM experiments E, experiment_measurements M " \
            "WHERE E.exp_id = M.exp_id " \
            "AND seq_name = \"" + s + "\""

    query += "".join(" AND E.exp_id IN "
                     "(SELECT exp_id "
                     "FROM experiment_conditions "
                     "WHERE cond_name = \"" + key + "\" "
                                                    "AND cond_val = \"" + c[key] + "\")"
                     for key in c)

    return query


'''
exp1: experiment id
exp2: experiment id
query returns a list of measurement names, measurement values for exp1, and
measurement values for exp2.
'''
def get_side_by_side_query(exp1, exp2):
    query = "SELECT E1.meas_name, E1.meas_val, E2.meas_val " \
            "FROM experiment_measurements E1, experiment_measurements E2 " \
            "WHERE E1.exp_id = \"" + exp1 + "\" " \
                                            "AND E2.exp_id = \"" + exp2 + "\" " \
                                                                          "AND E1.meas_name = E2.meas_name"

    return query


'''
s: List<seq_name>
c: Dict{cond_name: cond_val}
m: List<meas_name> or None
query returns a list of experiment ids, measurement names, and measurement
values that contain one of the given sequences and at least one of the given
condition values. If a list of measurements is included then only those
specified measurements will be returned.
'''
def get_mult_exp_info_query(s, c, m):
    query = "SELECT DISTINCT E.exp_id, meas_name, meas_val " \
            "FROM experiments E, experiment_conditions C, experiment_measurements M " \
            "WHERE E.exp_id = C.exp_id " \
            "AND E.exp_id = M.exp_id " \
            "AND (" + " OR ".join("seq_name = \"" + sequence + "\"" for sequence in s) + \
            ") AND (" + " OR ".join("(cond_name = \"" + key + "\" AND cond_val = \"" + c[key] + "\")" for key in c) \
            + ")"

    if m is not None:
        query += " AND (" + " OR ".join("meas_name = \"" + measurement + "\"" for measurement in m) \
                 + ")"

    print(query)

    return query


###############
# Check types #
###############
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
