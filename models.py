import pymysql.cursors as cursor


class DB_Connection:

    def __init__(self):
        connection = cursor.connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    password='',
                                    database='db_project')

    def insert_condition(self, query):
        print(query)
