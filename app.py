import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
import uuid

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

# Fungsi untuk menggenerate ID baru
def generate_id(prefix):
    return prefix + str(uuid.uuid4().hex[:3]).upper()

# Fungsi untuk menambahkan data baru ke tabel
def insert_data(query):
    engine = create_connection()
    if engine:
        try:
            with engine.connect() as connection:
                connection.execute(text(query))
                connection.commit()
                st.success("Data berhasil ditambahkan!")
        except Exception as e:
            st.error(f"Error: {e}")

# Fungsi untuk menghapus data dari tabel
def delete_data(table_name, id_column, id_value):
    engine = create_connection()
    if engine:
        try:
            with engine.connect() as connection:
                query = text(f"DELETE FROM {table_name} WHERE {id_column} = :id_value")
                connection.execute(query, {"id_value": id_value})
                connection.commit()
                st.success(f"Data dengan {id_column} = {id_value} berhasil dihapus!")
        except Exception as e:
            st.error(f"Error: {e}")

# Fungsi untuk menampilkan data Player_Team dalam bentuk kartu modern
def display_player_team_data(data, player_data, team_data):
    st.subheader("Team Players Overview")
    
    css = """
    <style>
        .team-player-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .team-player-card {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
            color: #333;
            padding: 20px;
            transition: transform 0.3s ease-in-out;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        .team-player-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        .team-player-card h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .team-player-card p {
            margin: 0;
            color: #666;
        }
        .team-player-detail {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #ddd;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.markdown('<div class="team-player-container">', unsafe_allow_html=True)
    
    for _, row in data.iterrows():
        player_name = player_data.loc[player_data['Player_ID'] == row['Player_Player_ID'], 'Nama'].values[0]
        team_name = team_data.loc[team_data['Team_ID'] == row['Team_Team_ID'], 'Nama_Tim'].values[0]

        st.markdown(f"""
        <div class="team-player-card">
            <h4>{team_name}</h4>
            <p><b>Anggota:</b> {row['Anggota']}</p>
            <p><b>Pelatih:</b> {row['Pelatih']}</p>
            <div class="team-player-detail">
                <p><b>Player:</b> {player_name}</p>
                <p><b>Detail:</b> {row['Detail_Player']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Delete {player_name} from {team_name}", key=f"delete_{row['Player_Player_ID']}_{row['Team_Team_ID']}"):
            delete_data("Player_Team", "Player_Player_ID", row['Player_Player_ID'])
            delete_data("Player_Team", "Team_Team_ID", row['Team_Team_ID'])
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Aplikasi Streamlit
st.title('Esport Database Viewer')

# Sidebar untuk navigasi
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Player", "Team Players", "Salary", "Schedule", "Event", "Sponsor"])

# Navigasi ke halaman yang dipilih
if page == "Player":
    st.header('Player Table')
    data = load_data("Player")
    st.subheader("Player Overview")
    
    css = """
    <style>
        .player-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .player-card {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
            color: #333;
            padding: 20px;
            transition: transform 0.3s ease-in-out;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        .player-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        .player-card h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .player-card p {
            margin: 0;
            color: #666;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.markdown('<div class="player-container">', unsafe_allow_html=True)
    
    for _, row in data.iterrows():
        st.markdown(f"""
        <div class="player-card">
            <h4>{row['Nama']}</h4>
            <p><b>Umur:</b> {row['Umur']}</p>
            <p><b>Email:</b> {row['Email']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Delete {row['Nama']}", key=f"delete_{row['Player_ID']}"):
            delete_data("Player", "Player_ID", row['Player_ID'])
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Add New Player")
    with st.form("player_form"):
        nama = st.text_input("Nama")
        umur = st.number_input("Umur", min_value=1, max_value=100, step=1)
        email = st.text_input("Email")
        submitted = st.form_submit_button("Submit")
        if submitted:
            player_id = generate_id("P")
            query = f"INSERT INTO Player (Player_ID, Nama, Umur, Email) VALUES ('{player_id}', '{nama}', {umur}, '{email}')"
            insert_data(query)
elif page == "Team Players":
    st.header('Team Players Table')
    player_data = load_data("Player")
    team_data = load_data("Team")
    data = load_data("Player_Team")
    display_player_team_data(data, player_data, team_data)
    st.subheader("Add New Player to Team")
    with st.form("player_team_form"):
        player_id = st.selectbox("Player ID", player_data['Player_ID'].tolist())
        team_id = st.selectbox("Team ID", team_data['Team_ID'].tolist())
        anggota = st.text_input("Anggota")
        pelatih = st.text_input("Pelatih")
        detail_player = st.text_input("Detail Player")
        submitted = st.form_submit_button("Submit")
        if submitted:
            query = f"INSERT INTO Player_Team (Player_Player_ID, Team_Team_ID, Anggota, Pelatih, Detail_Player) VALUES ('{player_id}', '{team_id}', '{anggota}', '{pelatih}', '{detail_player}')"
            insert_data(query)
elif page == "Salary":
    st.header('Salary Table')
    salary_data = load_data("Salary")
    player_data = load_data("Player")
    
    st.subheader("Salary Overview")
    salary_data = salary_data.merge(player_data[['Player_ID', 'Nama']], left_on='Player_Player_ID', right_on='Player_ID', how='left')
    salary_data = salary_data.set_index('Nama')['Jumlah_Pembayar']
    
    st.bar_chart(salary_data)

    st.markdown('<div class="salary-container">', unsafe_allow_html=True)
    
    for _, row in salary_data.iterrows():
        st.markdown(f"""
        <div class="salary-card">
            <h4>{row['Nama']}</h4>
            <p><b>Jumlah Pembayar:</b> {row['Jumlah_Pembayar']}</p>
            <p><b>Tanggal Pembayar:</b> {row['Tanggal_Pembayar']}</p>
            <p><b>Deskripsi:</b> {row['Deskripsi']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Delete Salary for {row['Nama']}", key=f"delete_{row['Salary_ID']}"):
            delete_data("Salary", "Salary_ID", row['Salary_ID'])
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Add New Salary")
    with st.form("salary_form"):
        player_id = st.selectbox("Player ID", player_data['Player_ID'].tolist())
        jumlah_pembayar = st.number_input("Jumlah Pembayar", min_value=0.0, step=0.01)
        tanggal_pembayar = st.date_input("Tanggal Pembayar")
        deskripsi = st.text_input("Deskripsi")
        submitted = st.form_submit_button("Submit")
        if submitted:
            salary_id = generate_id("S")
            query = f"INSERT INTO Salary (Salary_ID, Jumlah_Pembayar, Tanggal_Pembayar, Deskripsi, Player_Player_ID) VALUES ('{salary_id}', {jumlah_pembayar}, '{tanggal_pembayar}', '{deskripsi}', '{player_id}')"
            insert_data(query)
elif page == "Schedule":
    st.header('Schedule Table')
    data = load_data("Schedule")
    
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
        if st.button(f"Delete {row['Jenis_Kegiatan']} on {row['Tanggal_Kegiatan']}", key=f"delete_{row['Schedule_ID']}"):
            delete_data("Schedule", "Schedule_ID", row['Schedule_ID'])
            st.experimental_rerun()

    st.subheader("Add New Schedule")
    with st.form("schedule_form"):
        jenis_kegiatan = st.text_input("Jenis Kegiatan")
        tanggal_kegiatan = st.date_input("Tanggal Kegiatan")
        waktu_mulai = st.time_input("Waktu Mulai")
        waktu_selesai = st.time_input("Waktu Selesai")
        submitted = st.form_submit_button("Submit")
        if submitted:
            schedule_id = generate_id("SC")
            query = f"INSERT INTO Schedule (Schedule_ID, Jenis_Kegiatan, Tanggal_Kegiatan, Waktu_Mulai, Waktu_Selesai) VALUES ('{schedule_id}', '{jenis_kegiatan}', '{tanggal_kegiatan}', '{waktu_mulai}', '{waktu_selesai}')"
            insert_data(query)
elif page == "Event":
    st.header('Event Table')
    data = load_data("Event")
    
    st.subheader("Event Overview")
    css = """
    <style>
        .event-card {
            border-left: 4px solid #a3d2ca;
            padding-left: 20px;
            margin-bottom: 20px;
            background-color: #f7fff7;
            padding: 20px;
            border-radius: 10px;
            transition: transform 0.3s;
        }
        .event-card:hover {
            transform: scale(1.02);
        }
        .event-card h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .event-card p {
            margin: 5px 0;
            color: #666;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    for _, row in data.iterrows():
        st.markdown(f"""
        <div class="event-card">
            <h4>{row['Jenis_Event']} - {row['Tanggal_Event']}</h4>
            <p>{row['Deskripsi_Event']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Delete {row['Jenis_Event']} on {row['Tanggal_Event']}", key=f"delete_{row['Event_ID']}"):
            delete_data("Event", "Event_ID", row['Event_ID'])
            st.experimental_rerun()

    st.subheader("Add New Event")
    with st.form("event_form"):
        jenis_event = st.text_input("Jenis Event")
        tanggal_event = st.date_input("Tanggal Event")
        deskripsi_event = st.text_input("Deskripsi Event")
        team_id = st.selectbox("Team ID", load_data("Team")['Team_ID'].tolist())
        schedule_id = st.selectbox("Schedule ID", load_data("Schedule")['Schedule_ID'].tolist())
        submitted = st.form_submit_button("Submit")
        if submitted:
            event_id = generate_id("E")
            query = f"INSERT INTO Event (Event_ID, Jenis_Event, Tanggal_Event, Deskripsi_Event, Team_Team_ID, Schedule_Schedule_ID) VALUES ('{event_id}', '{jenis_event}', '{tanggal_event}', '{deskripsi_event}', '{team_id}', '{schedule_id}')"
            insert_data(query)
elif page == "Sponsor":
    st.header('Sponsor Table')
    data = load_data("Sponsor")
    
    st.subheader("Sponsor Overview")
    css = """
    <style>
        .sponsor-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .sponsor-card {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
            color: #333;
            padding: 20px;
            transition: transform 0.3s ease-in-out;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        .sponsor-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        .sponsor-card h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .sponsor-card p {
            margin: 0;
            color: #666;
        }
        .sponsor-card img {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.markdown('<div class="sponsor-container">', unsafe_allow_html=True)
    
    for _, row in data.iterrows():
        sponsor_image = f"images/sponsor_{row['Nama_Sponsor']}.jpg"
        if not os.path.exists(sponsor_image):
            sponsor_image = "images/sponsor_default.jpg"  # Gambar default jika tidak ada gambar sponsor

        st.markdown(f"""
        <div class="sponsor-card">
            <img src="{sponsor_image}" alt="Sponsor Image">
            <h4>{row['Nama_Sponsor']}</h4>
            <p><b>Kontak:</b> {row['Kontak_Sponsor']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Delete {row['Nama_Sponsor']}", key=f"delete_{row['Sponsor_ID']}"):
            delete_data("Sponsor", "Sponsor_ID", row['Sponsor_ID'])
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Add New Sponsor")
    with st.form("sponsor_form"):
        nama_sponsor = st.text_input("Nama Sponsor")
        kontak_sponsor = st.text_input("Kontak Sponsor")
        submitted = st.form_submit_button("Submit")
        if submitted:
            sponsor_id = generate_id("SP")
            query = f"INSERT INTO Sponsor (Sponsor_ID, Nama_Sponsor, Kontak_Sponsor) VALUES ('{sponsor_id}', '{nama_sponsor}', '{kontak_sponsor}')"
            insert_data(query)

    st.subheader("Add Sponsor-Team Relationship")
    with st.form("sponsor_team_form"):
        sponsor_id = st.selectbox("Sponsor ID", load_data("Sponsor")['Sponsor_ID'].tolist())
        team_id = st.selectbox("Team ID", load_data("Team")['Team_ID'].tolist())
        submitted = st.form_submit_button("Submit")
        if submitted:
            query = f"INSERT INTO Sponsor_Team (Sponsor_ID, Team_ID) VALUES ('{sponsor_id}', '{team_id}')"
            insert_data(query)
