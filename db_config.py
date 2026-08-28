
import mysql.connector
from mysql.connector import Error



# Create connection
def connect_db():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "sapna0867",
            database = "inventory")
        if connection.is_connected():
            return connection
    except Error as e:
            print("Error While connecting to MySQL:",e)
            return None


