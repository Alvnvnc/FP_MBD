import mysql.connector
from mysql.connector import Error

# Fungsi untuk membuat koneksi ke database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',
            password='Vincent35$',
            database='esport_db'
        )
        if connection.is_connected():
            print("Connected to database")
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

# Fungsi utama untuk membuat prosedur
def create_procedures():
    connection = create_connection()
    if connection:
        # Procedure CalculatePlayerSalaries
        procedure_calculate_player_salaries = """
        CREATE PROCEDURE CalculatePlayerSalaries()
        BEGIN
            DECLARE vPlayerID CHAR(6);
            DECLARE vEventPointsSum DECIMAL(10,2);
            DECLARE cur_player_events CURSOR FOR
                SELECT p.Player_ID, SUM(e.Points) * 1000 AS EventPointsSum
                FROM Player p
                JOIN Player_Team pt ON p.Player_ID = pt.Player_Player_ID
                JOIN Team t ON pt.Team_Team_ID = t.Team_ID
                JOIN Event e ON t.Team_ID = e.Team_Team_ID
                WHERE e.Tanggal_Event BETWEEN DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 1 MONTH) + INTERVAL 1 DAY AND LAST_DAY(CURDATE())
                GROUP BY p.Player_ID;
            DECLARE CONTINUE HANDLER FOR NOT FOUND BEGIN END;
            OPEN cur_player_events;
            calc_loop: LOOP
                FETCH cur_player_events INTO vPlayerID, vEventPointsSum;
                IF vPlayerID IS NULL THEN
                    LEAVE calc_loop;
                END IF;
                UPDATE Salary
                SET Jumlah_Pembayaran = vEventPointsSum
                WHERE Player_Player_ID = vPlayerID
                AND Tanggal_Pembayaran = LAST_DAY(CURDATE()) + INTERVAL 1 DAY;
            END LOOP;
            CLOSE cur_player_events;
        END;
        """
        execute_sql_command(connection, procedure_calculate_player_salaries)
        
        # Procedure CheckScheduleEventConsistency
        procedure_check_schedule_event_consistency = """
        CREATE PROCEDURE CheckScheduleEventConsistency()
        BEGIN
            DELETE e
            FROM Event e
            JOIN Schedule s ON e.Schedule_Schedule_ID = s.Schedule_ID
            WHERE e.Tanggal_Event <> s.Tanggal_Kegiatan;
        END;
        """
        execute_sql_command(connection, procedure_check_schedule_event_consistency)
        
        # Procedure TotalEventDuration
        procedure_total_event_duration = """
        CREATE PROCEDURE TotalEventDuration (
            IN TeamID VARCHAR(6)
        )
        BEGIN
            SELECT 
                t.Nama_Tim, 
                SUM(TIMESTAMPDIFF(HOUR, s.Waktu_Mulai, s.Waktu_Selesai)) AS TotalDurationHours
            FROM 
                Team t
            JOIN 
                Event e ON t.Team_ID = e.Team_Team_ID
            JOIN 
                Schedule s ON e.Schedule_Schedule_ID = s.Schedule_ID
            WHERE 
                t.Team_ID = TeamID
            GROUP BY 
                t.Nama_Tim;
        END;
        """
        execute_sql_command(connection, procedure_total_event_duration)

        connection.close()

if __name__ == "__main__":
    create_procedures()
