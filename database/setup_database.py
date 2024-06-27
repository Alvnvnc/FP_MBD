import mysql.connector
from mysql.connector import Error

def create_connection(database=None):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',
            password='Vincent35$',
            database=database
        )
        if connection.is_connected():
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None

def create_database():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS esport_db")
            print("Database created successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def create_tables():
    connection = create_connection("esport_db")
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create tables
            tables = [
                '''
                CREATE TABLE IF NOT EXISTS Player (
                    Player_ID CHAR(6) PRIMARY KEY,
                    Nama VARCHAR(50),
                    Umur INTEGER,
                    Email VARCHAR(30),
                    Detail_Player VARCHAR(100)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS Team (
                    Team_ID CHAR(6) PRIMARY KEY,
                    Nama_Tim VARCHAR(30),
                    Pelatih VARCHAR(50)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS Player_Team (
                    Player_Player_ID CHAR(6),
                    Team_Team_ID CHAR(6),
                    PRIMARY KEY (Player_Player_ID, Team_Team_ID),
                    FOREIGN KEY (Player_Player_ID) REFERENCES Player(Player_ID),
                    FOREIGN KEY (Team_Team_ID) REFERENCES Team(Team_ID)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS Salary (
                    Salary_ID CHAR(6) PRIMARY KEY,
                    Jumlah_Pembayar NUMERIC(10,2),
                    Tanggal_Pembayar DATE,
                    Deskripsi VARCHAR(150),
                    Player_Player_ID CHAR(6),
                    FOREIGN KEY (Player_Player_ID) REFERENCES Player(Player_ID)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS Schedule (
                    Schedule_ID CHAR(6) PRIMARY KEY,
                    Jenis_Kegiatan VARCHAR(50),
                    Tanggal_Kegiatan DATE,
                    Waktu_Mulai TIME,
                    Waktu_Selesai TIME,
                    Team_Team_ID CHAR(6),
                    FOREIGN KEY (Team_Team_ID) REFERENCES Team(Team_ID)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS Event (
                    Event_ID CHAR(6) PRIMARY KEY,
                    Jenis_Event VARCHAR(30),
                    Tanggal_Event DATE,
                    Deskripsi_Event VARCHAR(20),
                    Schedule_Schedule_ID CHAR(6),
                    FOREIGN KEY (Schedule_Schedule_ID) REFERENCES Schedule(Schedule_ID)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS Sponsor (
                    Sponsor_ID CHAR(6) PRIMARY KEY,
                    Nama_Sponsor VARCHAR(50),
                    Kontak_Sponsor VARCHAR(50)
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS Sponsor_Team (
                    Sponsor_ID CHAR(6),
                    Team_ID CHAR(6),
                    PRIMARY KEY (Sponsor_ID, Team_ID),
                    FOREIGN KEY (Sponsor_ID) REFERENCES Sponsor(Sponsor_ID),
                    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
                )
                '''
            ]

            for table in tables:
                cursor.execute(table)
            
            # Add indexes
            indexes = [
                "CREATE INDEX idx_player_nama ON Player (Nama)",
                "CREATE INDEX idx_team_nama_tim ON Team (Nama_Tim)",
                "CREATE INDEX idx_salary_player_id ON Salary (Player_Player_ID)",
                "CREATE INDEX idx_schedule_team_id ON Schedule (Team_Team_ID)",
                "CREATE INDEX idx_event_schedule_id ON Event (Schedule_Schedule_ID)"
            ]
            
            for index in indexes:
                cursor.execute(index)

            connection.commit()
            print('Tables and indexes created successfully')
        except Error as e:
            print(f'Error: {e}')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        print("Failed to create tables, no connection to database")

def main():
    create_database()
    create_tables()

if __name__ == '__main__':
    main()
