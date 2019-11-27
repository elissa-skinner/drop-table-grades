import mysql.connector


class Schema:
    def __init__(self):
        connection = mysql.connector.connect(host='localhost',
                                             port=3306,
                                             user='root',
                                             password='',
                                             database='db_project')

        cursor = connection.cursor()
        # create tables

    # def create_table(self):


class TableModel:   #TODO: make a class for each table
    TABLENAME = "TABLE"     # TODO: change tablename

    def __init__(self):
        connection = mysql.connector.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     password='',
                                     database='db_project')

        self.cursor = connection.cursor()

    def create(self, text, description):
        query = f'insert into {self.TABLENAME} ' \
                f'(Title, Description) ' \
                f'values ("{text}","{description}")'

        result = self.cursor.execute(query)
        return result

    # TODO: create methods for select, delete, and update
