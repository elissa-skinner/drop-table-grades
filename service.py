from models import *

DICT_OF_NAMES = {"CONDITION": "Condition Name ",
                 "MEASUREMENT": "Measurement Name ",
                 "SEQUENCE": "Sequence Name ",
                 "EXPERIMENT": "Experiment Name ",
                 "CSV": "CSV File Name ",
                 "TYPE": "Type"}

db = DB_Connection()

'''
determine which query to preform from success page
'''


def insert_into_db(results):
    if DICT_OF_NAMES["CONDITION"] in results:
        return db.insert_new_condition(results)
    elif DICT_OF_NAMES["MEASUREMENT"] in results:
        return db.insert_new_measurement(results)
    elif DICT_OF_NAMES["SEQUENCE"] in results:
        return db.insert_new_sequence(results)
    elif DICT_OF_NAMES["EXPERIMENT"] in results:
        return db.insert_new_experiment(results)
    elif DICT_OF_NAMES["CSV"] in results:
        return db.read_csv_file(results)
    else:
        print("GOT OTHER FOR results: ", results)
        return "That's weird, got: " + str(results)


def compare_exp(results):
    exp1 = results["Experiment #1 "]
    exp2 = results["Experiment #2 "]
    if not db.is_exp(exp1) or not db.is_exp(exp2):
        print("bad experiment names")
        return None

    return db.side_by_side(exp1, exp2)


def get_meas():
    return db.get_meas_from_db()


def get_exp(result):
    experiment_id = result
    experiment_tokens = experiment_id.split('_')
    seq_name = experiment_tokens[0]
    experiment_tokens = experiment_tokens[1:]

    conditions = {}
    for j in range(0, len(experiment_tokens), 2):
        condition = experiment_tokens[j]
        condition_value = experiment_tokens[j + 1]
        conditions[condition] = condition_value

    query = get_exp_info_query(seq_name, conditions)
    tuples = db.get_exp_info(query)
    return tuples


def get_mult_exp_info(result):
    s = []
    c = {}
    m = []
    for key in result:
        if "Sequence" in key:
            s.append(result[key])
        elif "Condition" in key:
            if "Value" in key:
                c[cond_name] = result[key]
            else:
                cond_name = result[key]
        elif "Measurement" in key:
            m.append(result[key])

    if len(m) == 0:
        m = None

    return db.execute_query(get_mult_exp_info_query(s, c, m))


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
