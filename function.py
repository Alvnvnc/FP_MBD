import mysql.connector
from mysql.connector import Error

# Fungsi untuk membuat koneksi ke database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='unko',
            password='090303',
            database='esport_db'
        )
        if connection.is_connected():
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None

# Fungsi untuk menjalankan perintah SQL
def execute_sql_command(connection, command):
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
        print(f"Executed: {command}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Fungsi utama untuk membuat trigger
def create_function():
    connection = create_connection()
    if connection:
        # Function to calc number of total event
        function_total_event = """
        CREATE FUNCTION CalculateTotalEvents(team_id CHAR(6))
        RETURNS INT
        BEGIN
            DECLARE total_events INT;

            SELECT COUNT(*) INTO total_events
            FROM Event
            WHERE Team_Team_ID = team_id;

            RETURN total_events;
        END 
        """
        execute_sql_command(connection, function_total_event)

        # Function to calc avg player salary
        function_avg_player_salary = """
        CREATE FUNCTION CalculateAverageSalary(player_id CHAR(6))
        RETURNS NUMERIC(10,2)
        BEGIN
            DECLARE avg_salary NUMERIC(10,2);

            SELECT AVG(Jumlah_Pembayar) INTO avg_salary
            FROM Salary
            WHERE Player_Player_ID = player_id;

            RETURN avg_salary;
        END 
        """
        execute_sql_command(connection, function_avg_player_salary)

        # Function to calc total player 
        function_total_player = """
        CREATE FUNCTION CalculateTotalPlayers(team_id CHAR(6))
        RETURNS INT
        BEGIN
            DECLARE total_players INT;

            SELECT COUNT(*) INTO total_players
            FROM Player_Team
            WHERE Team_Team_ID = team_id;

            RETURN total_players;
        END
        """
        execute_sql_command(connection, function_total_player)
        
        connection.close()

if __name__ == "__main__":
    create_function()