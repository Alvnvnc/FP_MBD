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

# Fungsi utama untuk membuat trigger
def create_triggers():
    connection = create_connection()
    if connection:
        # Trigger PlayerAgeValidationTrigger
        trigger_player_age_validation = """
        CREATE TRIGGER PlayerAgeValidationTrigger
        BEFORE INSERT ON Player
        FOR EACH ROW
        BEGIN
            DECLARE MinimumAge INT DEFAULT 18;
            IF NEW.Umur < MinimumAge THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Player must be at least 18 years old.';
            END IF;
        END;
        """
        execute_sql_command(connection, trigger_player_age_validation)
        
        # Trigger TeamRosterLimitTrigger
        trigger_team_roster_limit = """
        CREATE TRIGGER TeamRosterLimitTrigger
        BEFORE INSERT ON Player_Team
        FOR EACH ROW
        BEGIN
            DECLARE MaxPlayers INT DEFAULT 10;
            DECLARE CurrentPlayerCount INT;
            SELECT COUNT(*) INTO CurrentPlayerCount
            FROM Player_Team
            WHERE Team_Team_ID = NEW.Team_Team_ID;
            IF CurrentPlayerCount >= MaxPlayers THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Cannot add more players. Team roster limit reached.';
            END IF;
        END;
        """
        execute_sql_command(connection, trigger_team_roster_limit)

        # Trigger untuk validasi format Detail_Player pada INSERT
        trigger_validate_detail_player_insert = """
        CREATE TRIGGER validate_player_team_detail_insert
        BEFORE INSERT ON Player_Team
        FOR EACH ROW
        BEGIN
            IF NEW.Detail_Player NOT REGEXP '^.+/.+$' THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Detail_Player does not follow the format "nama game/role"';
            END IF;
        END;
        """
        execute_sql_command(connection, trigger_validate_detail_player_insert)

        # Trigger untuk validasi format Detail_Player pada UPDATE
        trigger_validate_detail_player_update = """
        CREATE TRIGGER validate_player_team_detail_update
        BEFORE UPDATE ON Player_Team
        FOR EACH ROW
        BEGIN
            IF NEW.Detail_Player NOT REGEXP '^[a-zA-Z0-9 ]+/[a-zA-Z0-9 ]+$' THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Detail_Player does not follow the format "nama game/role"';
            END IF;
        END;
        """
        execute_sql_command(connection, trigger_validate_detail_player_update)

        # execute_sql_command(connection, trigger_validate_detail_player_insert)

        # Trigger untuk validasi format Detail_Player pada UPDATE
        trigger_validate_email_format = """
        CREATE TRIGGER ValidateEmailFormat
        BEFORE INSERT ON Player
        FOR EACH ROW
        BEGIN
            DECLARE email_pattern VARCHAR(100);
            
            SET email_pattern = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$';
            
            IF NEW.Email REGEXP email_pattern <> 1 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Invalid email format. Please enter a valid email address.';
            END IF;
        END
        """
        execute_sql_command(connection, trigger_validate_email_format)

        # Prevent duplicate player name
        trigger_prevent_duplicate_player_name = """
        CREATE TRIGGER prevent_duplicate_player_name
        BEFORE INSERT ON Player
        FOR EACH ROW
        BEGIN
            DECLARE existing_count INT;
            SELECT COUNT(*) INTO existing_count
            FROM Player
            WHERE Nama = NEW.Nama;
            IF existing_count > 0 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'A player with this name already exists.';
            END IF;
        END;
        """
        execute_sql_command(connection, trigger_prevent_duplicate_player_name)
        
        connection.close()

if __name__ == "__main__":
    create_triggers()