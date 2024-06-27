import mysql.connector
from mysql.connector import Error

def create_connection():
    # Fungsi untuk membuat koneksi ke database
    # (sama seperti yang Anda miliki)
    pass

def execute_sql_command(connection, command):
    # Fungsi untuk menjalankan perintah SQL
    # (sama seperti yang Anda miliki)
    pass

def drop_all_triggers():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SHOW TRIGGERS")
            triggers = cursor.fetchall()
            for trigger in triggers:
                trigger_name = trigger[0]
                drop_trigger_query = f"DROP TRIGGER {trigger_name}"
                execute_sql_command(connection, drop_trigger_query)
                print(f"Trigger {trigger_name} dropped successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    drop_all_triggers()