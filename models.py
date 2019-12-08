import pymysql.cursors

DICT_OF_NAMES = {"CONDITION": "Condition Name ",
                 "MEASUREMENT": "Measurement Name ",
                 "SEQUENCE": "Sequence Name ",
                 "EXPERIMENT": "Measurement Value",
                 "CSV": "CSV File Name",
                 "TYPE": "Type"}


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
