from models import TableModel

class TableService:
    def __init__(self):
        self.model = TableModel()

    def create(self, params):
        self.model.create(params["text"], params["Description"])



###########
# queries #
###########

# s: seq_name
# c: {cond_name: cond_val}
# query returns a list of experiment ids, measurement names, and measurement
# values that contain the given sequence and condition values. The given
# conditions may not be an exhaustive list for the conditions of a returned
# experiment.
def get_exp_info_query(s, c):
    query = "SELECT E.exp_id, meas_name, meas_val " \
            "FROM experiments E, experiment_conditions C, experiment_measurements M " \
            "WHERE E.exp_id = C.exp_id " \
            "AND E.exp_id = M.exp_id " \
            "AND seq_name = \"" + s + "\""

    for (condition, value) in c:
        query += " AND cond_name = \"" + condition + "\" " \
                  "AND cond_val = \"" + value + "\""

    return query

# exp1: experiment id
# exp2: experiment id
# query returns a list of measurement names, measurement values for exp1, and
# measurement values for exp2.
def get_side_by_side_query(exp1, exp2):
    query = "SELECT E1.meas_name, E1.meas_val, E2.meas_val " \
            "FROM experiment_measurements E1, experiment_measurements E2 " \
            "WHERE E1.exp_id = \"" + exp1 + "\" " \
            "AND E2.exp_id = \"" + exp2 + "\" " \
            "AND E1.meas_name = E2.meas_name"

    return query

# s: List<seq_name>
# c: Dict{cond_name: cond_val}
# m: List<meas_name> or None
# query returns a list of experiment ids, measurement names, and measurement
# values that contain one of the given sequences and at least one of the given
# condition values. If a list of measurements is included then only those
# specified measurements will be returned.
def get_exp_info_query(s, c, m):
    query = "SELECT E.exp_id, meas_name, meas_val " \
            "FROM experiments E, experiment_conditions C, experiment_measurements M " \
            "WHERE E.exp_id = C.exp_id " \
            "AND E.exp_id = M.exp_id "

    for sequence in s:
        query += " AND seq_name = \"" + sequence + "\""                     ### Houston we have a problem

    for (condition, value) in c:
        query += " AND cond_name = \"" + condition + "\"" \
                                                     "AND cond_val = \"" + value + "\""

    return query

### ^^this needs more work...a lot more work