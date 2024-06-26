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
                SELECT pe.Player_ID, SUM(pe.EventPoints) * 1000 AS EventPointsSum
                FROM PlayerEvents pe
                INNER JOIN Event e ON pe.Event_ID = e.Event_ID
                WHERE e.Tanggal_event BETWEEN DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 1 MONTH) + INTERVAL 1 DAY AND LAST_DAY(CURDATE())
                GROUP BY pe.Player_ID;
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
        
        # Procedure GenerateTeamPerformanceReport
        procedure_generate_team_performance_report = """
        CREATE PROCEDURE GenerateTeamPerformanceReport (
            IN TeamID VARCHAR(6),
            IN ReportPeriod VARCHAR(20)
        )
        BEGIN
            DECLARE StartDate DATE;
            DECLARE EndDate DATE;
            CASE ReportPeriod
                WHEN 'Monthly' THEN
                    SET StartDate = DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 1 MONTH) + INTERVAL 1 DAY;
                    SET EndDate = LAST_DAY(CURDATE());
                WHEN 'Quarterly' THEN
                    SET StartDate = DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 3 MONTH) + INTERVAL 1 DAY;
                    SET EndDate = LAST_DAY(CURDATE());
                WHEN 'Annual' THEN
                    SET StartDate = DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 1 YEAR) + INTERVAL 1 DAY;
                    SET EndDate = LAST_DAY(CURDATE());
                ELSE
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Invalid ReportPeriod. Supported values are Monthly, Quarterly, or Annual.';
            END CASE;
            IF ReportPeriod = 'Monthly' OR ReportPeriod = 'Quarterly' OR ReportPeriod = 'Annual' THEN
                SELECT t.Nama_Tim, p.Nama, SUM(e.Points) AS TotalPoints
                FROM Team t
                JOIN Player_Team pt ON t.Team_ID = pt.Team_Team_ID
                JOIN Player p ON pt.Player_Player_ID = p.Player_ID
                JOIN PlayerEvents e ON p.Player_ID = e.Player_ID
                JOIN Event ev ON e.Event_ID = ev.Event_ID
                WHERE t.Team_ID = TeamID
                AND ev.Tanggal_event BETWEEN StartDate AND EndDate
                GROUP BY t.Nama_Tim, p.Nama
                ORDER BY TotalPoints DESC;
            END IF;
        END;
        """
        execute_sql_command(connection, procedure_generate_team_performance_report)
        
        connection.close()

if __name__ == "__main__":
    create_procedures()
