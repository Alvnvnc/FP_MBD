import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import create_engine, text
import os

# Fungsi untuk membuat koneksi ke database menggunakan SQLAlchemy
def create_connection():
    try:
        engine = create_engine('mysql+mysqlconnector://alvn:Vincent35$@localhost/esport_db')
        return engine
    except Exception as err:
        st.error(f"Error: {err}")
        return None

# Fungsi untuk memuat data dari tabel
def load_data(table_name):
    engine = create_connection()
    if engine:
        with engine.connect() as connection:
            query = text(f"SELECT * FROM {table_name}")
            data = pd.read_sql(query, connection)
            return data
    else:
        return pd.DataFrame()

# Fungsi untuk menampilkan data schedule dengan HTML dan CSS
def display_schedule_data(data):
    st.subheader("Schedule Overview")

    css = """
    <style>
        .schedule-card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
        }
        .schedule-card h3 {
            color: #333;
            margin-bottom: 10px;
        }
        .schedule-card p {
            margin: 5px 0;
            color: #666;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    def format_timedelta(td):
        if pd.isna(td):
            return "None"
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    for _, row in data.iterrows():
        if isinstance(row['Waktu_Mulai'], pd.Timestamp):
            start_time = row['Waktu_Mulai'].strftime("%H:%M:%S")
        else:
            start_time = format_timedelta(row['Waktu_Mulai'])

        if isinstance(row['Waktu_Selesai'], pd.Timestamp):
            end_time = row['Waktu_Selesai'].strftime("%H:%M:%S")
        else:
            end_time = format_timedelta(row['Waktu_Selesai'])

        st.markdown(f"""
        <div class="schedule-card">
            <h3>{row['Jenis_Kegiatan']}</h3>
            <p><b>Tanggal Kegiatan:</b> {row['Tanggal_Kegiatan'].strftime("%Y-%m-%d")}</p>
            <p><b>Waktu Mulai:</b> {start_time}</p>
            <p><b>Waktu Selesai:</b> {end_time}</p>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan data pemain dalam bentuk kartu
def display_player_data(data):
    css = """
    <style>
        .player-card {
            display: flex;
            align-items: center;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #f9f9f9;
        }
        .player-card img {
            height: 100px;
            width: 100px;
            border-radius: 50%;
            margin-right: 20px;
        }
        .player-card div {
            display: flex;
            flex-direction: column;
        }
        .player-card h4 {
            margin: 0;
            color: #333;
        }
        .player-card p {
            margin: 5px 0;
            color: #666;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    for _, row in data.iterrows():
        player_id = row['Player_ID']
        player_image = f"images/{player_id}.jpg"
        if not os.path.exists(player_image):
            player_image = "images/player_default.jpg"  # Gambar default jika tidak ada gambar pemain

        st.markdown(f"""
        <div class="player-card">
            <img src="{player_image}" alt="Player Image">
            <div>
                <h4>{row['Nama']}</h4>
                <p><b>Umur:</b> {row['Umur']}</p>
                <p><b>Email:</b> {row['Email']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan data pemain berdasarkan tim
def display_team_player_data(team_data, player_team_data, player_data):
    css = """
    <style>
        .team-card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
        }
        .team-card h3 {
            color: #333;
            margin-bottom: 10px;
        }
        .player-card {
            display: flex;
            align-items: center;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #fff;
        }
        .player-card img {
            height: 80px;
            width: 80px;
            border-radius: 50%;
            margin-right: 20px;
        }
        .player-card div {
            display: flex;
            flex-direction: column;
        }
        .player-card h4 {
            margin: 0;
            color: #333;
        }
        .player-card p {
            margin: 5px 0;
            color: #666;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    for _, team in team_data.iterrows():
        st.markdown(f"<div class='team-card'><h3>{team['Nama_Tim']}</h3>", unsafe_allow_html=True)
        team_players = player_team_data[player_team_data['Team_Team_ID'] == team['Team_ID']]
        for _, player_team in team_players.iterrows():
            player = player_data[player_data['Player_ID'] == player_team['Player_Player_ID']].iloc[0]
            player_id = player['Player_ID']
            player_detail = player_team['Detail_Player']
            player_image = f"images/{player_id}.jpg"
            if not os.path.exists(player_image):
                player_image = "images/player_default.jpg"  # Gambar default jika tidak ada gambar pemain

            st.markdown(f"""
            <div class="player-card">
                <img src="{player_image}" alt="Player Image">
                <div>
                    <h4>{player['Nama']}</h4>
                    <p>{player_detail}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Fungsi untuk menampilkan data tim dalam bentuk kartu
def display_team_data(data):
    for _, row in data.iterrows():
        team_image = "images/team_default.jpg"
        st.markdown(f"""
        <div style="display: flex; align-items: center; border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
            <img src="{team_image}" alt="Team Image" style="height: 100px; width: 100px; border-radius: 50%; margin-right: 20px;">
            <div>
                <h4>{row['Nama_Tim']}</h4>
                <p><b>ID:</b> {row['Team_ID']}</p>
                <p><b>Anggota:</b> {row['Anggota']}</p>
                <p><b>Pelatih:</b> {row['Pelatih']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan data gaji dalam bentuk grafik
def display_salary_data(salary_data, player_data):
    # Gabungkan data salary dengan data player untuk mendapatkan nama pemain
    salary_data = salary_data.merge(player_data[['Player_ID', 'Nama']], left_on='Player_Player_ID', right_on='Player_ID', how='left')
    salary_data = salary_data.set_index('Nama')['Jumlah_Pembayar']
    
    st.bar_chart(salary_data)

# Fungsi untuk menampilkan statistik data pemain
def display_player_stats(data):
    st.subheader("Player Statistics")
    st.write("Average Age: ", data['Umur'].mean())
    st.write("Total Players: ", data['Player_ID'].count())

# Fungsi untuk menampilkan statistik data tim
def display_team_stats(data):
    st.subheader("Team Statistics")
    st.write("Total Teams: ", data['Team_ID'].count())

# Fungsi untuk menampilkan data event dalam bentuk timeline
def display_event_data(data):
    st.subheader("Event Timeline")
    if 'Jenis_Event' not in data.columns or 'Tanggal_Event' not in data.columns:
        st.error("Kolom 'Jenis_Event' atau 'Tanggal_Event' tidak ditemukan dalam tabel Event.")
        return
    for _, row in data.iterrows():
        st.markdown(f"""
        <div style="border-left: 4px solid #ddd; padding-left: 10px; margin-bottom: 10px;">
            <h4>{row['Jenis_Event']} - {row['Tanggal_Event']}</h4>
            <p><b>ID:</b> {row['Event_ID']}</p>
            <p><b>Team ID:</b> {row['Team_Team_ID']}</p>
            <p><b>Schedule ID:</b> {row['Schedule_Schedule_ID']}</p>
            <p><b>Deskripsi:</b> {row['Deskripsi_Event']}</p>
        </div>
        """, unsafe_allow_html=True)

# Aplikasi Streamlit
st.title('Esport Database Viewer')

# Sidebar untuk navigasi
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Player", "Team", "Player Team", "Salary", "Schedule", "Event", "Sponsor", "Sponsor Team"])

# Navigasi ke halaman yang dipilih
if page == "Player":
    st.header('Player Table')
    data = load_data("Player")
    display_player_stats(data)
    display_player_data(data)
elif page == "Team":
    st.header('Team Table')
    data = load_data("Team")
    display_team_stats(data)
    display_team_data(data)
elif page == "Player Team":
    st.header('Player Team Table')
    team_data = load_data("Team")
    player_team_data = load_data("Player_Team")
    player_data = load_data("Player")
    display_team_player_data(team_data, player_team_data, player_data)
elif page == "Salary":
    st.header('Salary Table')
    salary_data = load_data("Salary")
    player_data = load_data("Player")
    display_salary_data(salary_data, player_data)
elif page == "Schedule":
    st.header('Schedule Table')
    data = load_data("Schedule")
    
    # Convert datetime columns to proper format
    data['Tanggal_Kegiatan'] = pd.to_datetime(data['Tanggal_Kegiatan'], format='%Y-%m-%d', errors='coerce')
    
    display_schedule_data(data)
elif page == "Event":
    st.header('Event Table')
    data = load_data("Event")
    display_event_data(data)
elif page == "Sponsor":
    st.header('Sponsor Table')
    data = load_data("Sponsor")
    st.dataframe(data)
elif page == "Sponsor Team":
    st.header('Sponsor Team Table')
    data = load_data("Sponsor_Team")
    st.dataframe(data)
