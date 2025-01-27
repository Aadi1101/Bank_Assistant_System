import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,       # Replace with your MySQL host, e.g., '127.0.0.1'
            user=DB_USER,   # Your MySQL username
            password=DB_PASSWORD, # Your MySQL password
            database=DB_NAME  # The database you want to connect to
        )

        if connection.is_connected():
            return connection
    except Exception as e:
        print(e)

def query_database(sql_query:str):
    result_list = []
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute(sql_query)
    for result in cursor.fetchall():
        result_list.append(result)
    cursor.close()
    connection.close()
    return str(result_list)

def get_user_id(username: str):
    result = None
    connection = db_connection()  # Ensure this establishes a valid DB connection
    cursor = connection.cursor()
    sql_query = 'SELECT UserID FROM Users WHERE Username = %s'
    try:
        cursor.execute(sql_query, (username,))
        row = cursor.fetchone()
        if row:
            result = row[0]
    except Exception as e:
        print(f"Error occurred while fetching user ID: {e}")
    finally:
        # Close cursor and connection to prevent resource leakage
        cursor.close()
        connection.close()

    return result
