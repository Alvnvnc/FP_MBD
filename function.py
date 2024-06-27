import mysql.connector
from mysql.connector import Error

# Function to create a connection to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',
            password='Vincent35$',
            database='esport_db'
        )
        if connection.is_connected():
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None

# Function to execute SQL commands
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

# Main function to create functions
def create_functions():
    connection = create_connection()
    if connection:
        try:
            # Function to calculate total events
            function_total_event = """
            CREATE FUNCTION CalculateTotalEvents(team_id CHAR(6))
            RETURNS INT
            DETERMINISTIC
            BEGIN
                DECLARE total_events INT;
                SELECT COUNT(*) INTO total_events
                FROM Event e
                JOIN Schedule s ON e.Schedule_Schedule_ID = s.Schedule_ID
                WHERE s.Team_Team_ID = team_id;
                RETURN total_events;
            END
            """
            execute_sql_command(connection, function_total_event)

            # Function to calculate average player salary
            function_avg_player_salary = """
            CREATE FUNCTION CalculateAverageSalary(player_id CHAR(6))
            RETURNS NUMERIC(10,2)
            DETERMINISTIC
            BEGIN
                DECLARE avg_salary NUMERIC(10,2);
                SELECT AVG(Jumlah_Pembayar) INTO avg_salary
                FROM Salary
                WHERE Player_Player_ID = player_id;
                RETURN avg_salary;
            END
            """
            execute_sql_command(connection, function_avg_player_salary)

            # Function to calculate total players
            function_total_player = """
            CREATE FUNCTION CalculateTotalPlayers(team_id CHAR(6))
            RETURNS INT
            DETERMINISTIC
            BEGIN
                DECLARE total_players INT;
                SELECT COUNT(*) INTO total_players
                FROM Player_Team
                WHERE Team_Team_ID = team_id;
                RETURN total_players;
            END
            """
            execute_sql_command(connection, function_total_player)

            # New function to calculate total sponsors
            function_total_sponsors = """
            CREATE FUNCTION CalculateTotalSponsors(team_id CHAR(6))
            RETURNS INT
            DETERMINISTIC
            BEGIN
                DECLARE total_sponsors INT;
                SELECT COUNT(*) INTO total_sponsors
                FROM Sponsor_Team
                WHERE Team_ID = team_id;
                RETURN total_sponsors;
            END
            """
            execute_sql_command(connection, function_total_sponsors)

        except Error as e:
            print(f"Error creating functions: {e}")
        finally:
            connection.close()
    else:
        print("Failed to create database connection.")

if __name__ == "__main__":
    create_functions()