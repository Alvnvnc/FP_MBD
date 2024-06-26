import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',  # Ganti dengan user MySQL Anda
            password='Vincent35$',  # Ganti dengan password MySQL Anda
            database='esport_db'
        )
        if connection.is_connected():
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None

def truncate_tables(connection):
    try:
        cursor = connection.cursor()

        # Menonaktifkan foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Daftar nama tabel yang akan dihapus datanya
        tables = ['Player_Team', 'Salary', 'Schedule', 'Event', 'Sponsor_Team', 'Player', 'Team', 'Sponsor']

        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table}")
            print(f"Table {table} truncated successfully")

        # Mengaktifkan kembali foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        connection.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def main():
    connection = create_connection()
    if connection:
        truncate_tables(connection)
        connection.close()

if __name__ == "__main__":
    main()
