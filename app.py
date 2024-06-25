import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt
from datetime import datetime
import os

# Fungsi untuk membuat koneksi ke database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_name',
            password='your_password',
            database='esport_db'
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        st.error(f'Error: {err}')
        return None

# Fungsi untuk memuat data dari tabel
def load_data(table_name):
    connection = create_connection()
    if connection:
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, connection)
        connection.close()
        return data
    else:
        return pd.DataFrame()

# Fungsi untuk menampilkan data pemain dalam bentuk kartu
def display_player_data(data):
    for _, row in data.iterrows():
        player_id = row['Player_ID']
        player_image = f"images/{player_id}.jpg"
        if not os.path.exists(player_image):
            player_image = "images/player_default.jpg"  # Gambar default jika tidak ada gambar pemain

        st.markdown(f"""
        <div style="display: flex; align-items: center; border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
            <img src="{player_image}" alt="Player Image" style="height: 100px; width: 100px; border-radius: 50%; margin-right: 20px;">
            <div>
                <h4>{row['Nama']}</h4>
                <p><b>ID:</b> {row['Player_ID']}</p>
                <p><b>Umur:</b> {row['Umur']}</p>
                <p><b>Email:</b> {row['Email']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
def display_salary_data(data):
    st.bar_chart(data.set_index('Player_Player_ID')['Jumlah_Pembayar'])

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

# Fungsi untuk menampilkan data schedule
def display_schedule_data(data):
    st.subheader("Schedule Overview")
    
    # Mengonversi kolom waktu menjadi datetime
    data['Waktu_Mulai'] = pd.to_datetime(data['Waktu_Mulai'], errors='coerce')
    data['Waktu_Selesai'] = pd.to_datetime(data['Waktu_Selesai'], errors='coerce')
    data['Tanggal_Kegiatan'] = pd.to_datetime(data['Tanggal_Kegiatan'], errors='coerce')
    data['Status'] = data.apply(lambda row: 'Selesai' if row['Waktu_Selesai'] < datetime.now() else 'Belum Selesai', axis=1)
    today = datetime.today()

    # Menampilkan aktivitas yang belum selesai berdasarkan hari ini
    st.subheader("Aktivitas yang Belum Selesai per Hari Ini")
    unfinished_activities = data[(data['Waktu_Selesai'] >= today) & (data['Status'] == 'Belum Selesai')]
    if not unfinished_activities.empty:
        st.write(unfinished_activities[['Jenis_Kegiatan', 'Tanggal_Kegiatan', 'Waktu_Mulai', 'Waktu_Selesai']])
    else:
        st.write("Tidak ada aktivitas yang belum selesai per hari ini.")

    # Kalender untuk memilih rentang tanggal aktivitas
    st.subheader("Aktivitas")
    end_date = st.date_input("Pilih tanggal selesai", today.date())
    date_filtered_activities = data[data['Tanggal_Kegiatan'] <= pd.to_datetime(end_date)]
    if not date_filtered_activities.empty:
        st.write(date_filtered_activities[['Jenis_Kegiatan', 'Tanggal_Kegiatan', 'Waktu_Mulai', 'Waktu_Selesai']])
    else:
        st.write("Tidak ada aktivitas pada rentang tanggal yang dipilih.")

    # Visualisasi aktivitas berdasarkan rentang tanggal yang dipilih
    st.subheader("Visualisasi Aktivitas Harian")
    if not date_filtered_activities.empty:
        chart = alt.Chart(date_filtered_activities).mark_bar().encode(
            x='Waktu_Mulai:T',
            x2='Waktu_Selesai:T',
            y=alt.Y('Jenis_Kegiatan:N', sort='-x'),
            color='Jenis_Kegiatan:N',
            tooltip=['Jenis_Kegiatan', 'Waktu_Mulai', 'Waktu_Selesai']
        ).properties(
            width=800,
            height=400,
            title='Timeline Aktivitas Harian'
        )

        st.altair_chart(chart, use_container_width=True)

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
    data = load_data("Player_Team")
    st.dataframe(data)
elif page == "Salary":
    st.header('Salary Table')
    data = load_data("Salary")
    display_salary_data(data)
elif page == "Schedule":
    st.header('Schedule Table')
    data = load_data("Schedule")
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
