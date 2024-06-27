import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',
            password='Vincent35$',
            database='streamlit_auth_esport'
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
