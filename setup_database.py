import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',
            password='Vincent35$'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS esport_db")
            print('Database created successfully')
            cursor.close()
            connection.close()
    except Error as e:
        print(f'Error: {e}')

def create_tables_and_insert_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='alvn',
            password='Vincent35$',
            database='esport_db'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Create tables
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Player (
                Player_ID CHAR(6) PRIMARY KEY,
                Nama VARCHAR(50),
                Umur INTEGER,
                Email VARCHAR(30)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Team (
                Team_ID CHAR(6) PRIMARY KEY,
                Nama_Tim VARCHAR(30),
                Anggota VARCHAR(50),
                Pelatih VARCHAR(50)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Player_Team (
                Player_Player_ID CHAR(6),
                Team_Team_ID CHAR(6),
                Detail_Player VARCHAR(100),
                PRIMARY KEY (Player_Player_ID, Team_Team_ID),
                FOREIGN KEY (Player_Player_ID) REFERENCES Player(Player_ID),
                FOREIGN KEY (Team_Team_ID) REFERENCES Team(Team_ID)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Salary (
                Salary_ID CHAR(6) PRIMARY KEY,
                Jumlah_Pembayar NUMERIC(10,2),
                Tanggal_Pembayar DATE,
                Deskripsi VARCHAR(150),
                Player_Player_ID CHAR(6),
                FOREIGN KEY (Player_Player_ID) REFERENCES Player(Player_ID)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Schedule (
                Schedule_ID CHAR(6) PRIMARY KEY,
                Jenis_Kegiatan VARCHAR(50),
                Tanggal_Kegiatan DATE,
                Waktu_Mulai TIME,
                Waktu_Selesai TIME
            );

            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Event (
                Event_ID CHAR(6) PRIMARY KEY,
                Jenis_Event VARCHAR(30),
                Tanggal_Event DATE,
                Deskripsi_Event VARCHAR(20),
                Team_Team_ID CHAR(6),
                Schedule_Schedule_ID CHAR(6),
                FOREIGN KEY (Team_Team_ID) REFERENCES Team(Team_ID),
                FOREIGN KEY (Schedule_Schedule_ID) REFERENCES Schedule(Schedule_ID)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sponsor (
                Sponsor_ID CHAR(6) PRIMARY KEY,
                Nama_Sponsor VARCHAR(50),
                Kontak_Sponsor VARCHAR(50)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sponsor_Team (
                Sponsor_ID CHAR(6),
                Team_ID CHAR(6),
                PRIMARY KEY (Sponsor_ID, Team_ID),
                FOREIGN KEY (Sponsor_ID) REFERENCES Sponsor(Sponsor_ID),
                FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
            )
            ''')

            # Insert sample data
            cursor.execute("INSERT INTO Player VALUES ('P001', 'Alice', 25, 'alice@example.com')")
            cursor.execute("INSERT INTO Player VALUES ('P002', 'Bob', 30, 'bob@example.com')")
            cursor.execute("INSERT INTO Team VALUES ('T001', 'Team A', 'Alice, Bob', 'Coach A')")
            cursor.execute("INSERT INTO Player_Team VALUES ('P001', 'T001', 'Detail 1')")
            cursor.execute("INSERT INTO Player_Team VALUES ('P002', 'T001', 'Detail 2')")
            cursor.execute("INSERT INTO Salary VALUES ('S001', 5000.00, '2024-01-01', 'Monthly Salary', 'P001')")
            cursor.execute("INSERT INTO Salary VALUES ('S002', 6000.00, '2024-01-01', 'Monthly Salary', 'P002')")
            cursor.execute("INSERT INTO Schedule VALUES ('SC001', 'Training', '2024-06-21', '08:00:00', '10:00:00')")
            cursor.execute("INSERT INTO Event VALUES ('E001', 'Match', '2024-06-22', 'Quarter Finals', 'T001', 'SC001')")
            cursor.execute("INSERT INTO Sponsor VALUES ('SP001', 'Sponsor A', 'contact@sponsor.com')")
            cursor.execute("INSERT INTO Sponsor_Team VALUES ('SP001', 'T001')")

            connection.commit()
            print('Tables created and sample data inserted successfully')
            cursor.close()
            connection.close()
    except Error as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    create_database()
    create_tables_and_insert_data()