import mysql.connector
from mysql.connector import Error

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

def insert_data(connection):
    try:
        cursor = connection.cursor()

        # Data pemain
        cursor.execute("INSERT INTO Player (Player_ID, Nama, Umur, Email) VALUES ('P001', 'Alice', 25, 'alice@example.com')")
        cursor.execute("INSERT INTO Player (Player_ID, Nama, Umur, Email) VALUES ('P002', 'Bob', 30, 'bob@example.com')")
        cursor.execute("INSERT INTO Player (Player_ID, Nama, Umur, Email) VALUES ('P003', 'Charlie', 22, 'charlie@example.com')")
        cursor.execute("INSERT INTO Player (Player_ID, Nama, Umur, Email) VALUES ('P004', 'Dave', 28, 'dave@example.com')")
        cursor.execute("INSERT INTO Player (Player_ID, Nama, Umur, Email) VALUES ('P005', 'Eve', 26, 'eve@example.com')")

        # Data tim
        cursor.execute("INSERT INTO Team (Team_ID, Nama_Tim) VALUES ('T001', 'Team A')")
        cursor.execute("INSERT INTO Team (Team_ID, Nama_Tim) VALUES ('T002', 'Team B')")
        cursor.execute("INSERT INTO Team (Team_ID, Nama_Tim) VALUES ('T003', 'Team C')")

        # Data hubungan pemain dan tim dengan detail role
        cursor.execute("INSERT INTO Player_Team (Player_Player_ID, Team_Team_ID, Anggota, Pelatih, Detail_Player) VALUES ('P001', 'T001', 'Alice, Bob', 'Coach A', 'Mobile Legends/Marksman')")
        cursor.execute("INSERT INTO Player_Team (Player_Player_ID, Team_Team_ID, Anggota, Pelatih, Detail_Player) VALUES ('P002', 'T001', 'Alice, Bob', 'Coach A', 'Mobile Legends/Tank')")
        cursor.execute("INSERT INTO Player_Team (Player_Player_ID, Team_Team_ID, Anggota, Pelatih, Detail_Player) VALUES ('P003', 'T002', 'Charlie, Dave', 'Coach B', 'Dota 2/Carry')")
        cursor.execute("INSERT INTO Player_Team (Player_Player_ID, Team_Team_ID, Anggota, Pelatih, Detail_Player) VALUES ('P004', 'T002', 'Charlie, Dave', 'Coach B', 'Dota 2/Support')")
        cursor.execute("INSERT INTO Player_Team (Player_Player_ID, Team_Team_ID, Anggota, Pelatih, Detail_Player) VALUES ('P005', 'T003', 'Eve', 'Coach C', 'CS:GO/Sniper')")

        # Data gaji
        cursor.execute("INSERT INTO Salary (Salary_ID, Jumlah_Pembayar, Tanggal_Pembayar, Deskripsi, Player_Player_ID) VALUES ('S001', 5000.00, '2024-01-01', 'Monthly Salary', 'P001')")
        cursor.execute("INSERT INTO Salary (Salary_ID, Jumlah_Pembayar, Tanggal_Pembayar, Deskripsi, Player_Player_ID) VALUES ('S002', 6000.00, '2024-01-01', 'Monthly Salary', 'P002')")
        cursor.execute("INSERT INTO Salary (Salary_ID, Jumlah_Pembayar, Tanggal_Pembayar, Deskripsi, Player_Player_ID) VALUES ('S003', 7000.00, '2024-01-01', 'Monthly Salary', 'P003')")
        cursor.execute("INSERT INTO Salary (Salary_ID, Jumlah_Pembayar, Tanggal_Pembayar, Deskripsi, Player_Player_ID) VALUES ('S004', 8000.00, '2024-01-01', 'Monthly Salary', 'P004')")
        cursor.execute("INSERT INTO Salary (Salary_ID, Jumlah_Pembayar, Tanggal_Pembayar, Deskripsi, Player_Player_ID) VALUES ('S005', 9000.00, '2024-01-01', 'Monthly Salary', 'P005')")

        # Data jadwal
        cursor.execute("INSERT INTO Schedule (Schedule_ID, Jenis_Kegiatan, Tanggal_Kegiatan, Waktu_Mulai, Waktu_Selesai) VALUES ('SC001', 'Training', '2024-06-21', '08:00:00', '10:00:00')")
        cursor.execute("INSERT INTO Schedule (Schedule_ID, Jenis_Kegiatan, Tanggal_Kegiatan, Waktu_Mulai, Waktu_Selesai) VALUES ('SC002', 'Match', '2024-07-01', '14:00:00', '16:00:00')")
        cursor.execute("INSERT INTO Schedule (Schedule_ID, Jenis_Kegiatan, Tanggal_Kegiatan, Waktu_Mulai, Waktu_Selesai) VALUES ('SC003', 'Training', '2024-07-05', '09:00:00', '11:00:00')")

        # Data event
        cursor.execute("INSERT INTO Event (Event_ID, Jenis_Event, Tanggal_Event, Deskripsi_Event, Team_Team_ID, Schedule_Schedule_ID) VALUES ('E001', 'Match', '2024-06-22', 'Quarter Finals', 'T001', 'SC001')")
        cursor.execute("INSERT INTO Event (Event_ID, Jenis_Event, Tanggal_Event, Deskripsi_Event, Team_Team_ID, Schedule_Schedule_ID) VALUES ('E002', 'Match', '2024-07-02', 'Semi Finals', 'T002', 'SC002')")
        cursor.execute("INSERT INTO Event (Event_ID, Jenis_Event, Tanggal_Event, Deskripsi_Event, Team_Team_ID, Schedule_Schedule_ID) VALUES ('E003', 'Match', '2024-07-06', 'Finals', 'T003', 'SC003')")

        # Data sponsor
        cursor.execute("INSERT INTO Sponsor (Sponsor_ID, Nama_Sponsor, Kontak_Sponsor) VALUES ('SP001', 'Sponsor A', 'contact@sponsorA.com')")
        cursor.execute("INSERT INTO Sponsor (Sponsor_ID, Nama_Sponsor, Kontak_Sponsor) VALUES ('SP002', 'Sponsor B', 'contact@sponsorB.com')")
        cursor.execute("INSERT INTO Sponsor (Sponsor_ID, Nama_Sponsor, Kontak_Sponsor) VALUES ('SP003', 'Sponsor C', 'contact@sponsorC.com')")

        # Data hubungan sponsor dan tim
        cursor.execute("INSERT INTO Sponsor_Team (Sponsor_ID, Team_ID) VALUES ('SP001', 'T001')")
        cursor.execute("INSERT INTO Sponsor_Team (Sponsor_ID, Team_ID) VALUES ('SP002', 'T002')")
        cursor.execute("INSERT INTO Sponsor_Team (Sponsor_ID, Team_ID) VALUES ('SP003', 'T003')")

        connection.commit()
        print("Data inserted successfully")

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def main():
    connection = create_connection()
    if connection:
        insert_data(connection)
        connection.close()

if __name__ == "__main__":
    main()
