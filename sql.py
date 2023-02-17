import mysql.connector as conn
import logging
import scrapper

logging.basicConfig(filename="sql_operations.log", level=logging.DEBUG, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")


class MySQL_operations():

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_connection(self):
        try:
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.password, database=self.database)
            cursor = mydb.cursor()
            self.mydb = mydb
            self.cursor = cursor
            logging.info("Connection to DB successful")
            print("Connection to DB successful")
        except Exception as e:
            logging.error("Exception occurred", e)

    def insert_data(self, values):
        try:
            self.values = values
            self.cursor.execute(f"INSERT INTO {self.database}.YTVideoDetails VALUES({self.values})")
            self.mydb.commit()
            logging.info("Insertion successful")
            print("Insertion successful")
        except Exception as e:
            logging.error("Exception occurred", e)