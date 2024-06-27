import mysql.connector
from mysql.connector import Error

# Fungsi untuk membuat koneksi ke database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',  # ganti dengan user MySQL Anda
            password='Vincent35$',  # ganti dengan password MySQL Anda
            database='esport_db'
        )
        if connection.is_connected():
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None

# Fungsi untuk menghapus semua tabel dalam database
def drop_all_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        connection.commit()
        print("All tables dropped successfully")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Fungsi utama untuk menghapus semua tabel dalam database
def delete_database():
    connection = create_connection()
    if connection:
        drop_all_tables(connection)
        connection.close()

if __name__ == "__main__":
    delete_database()
