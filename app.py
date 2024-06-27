import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
import uuid
import datetime
from page.login_app import login
from page.register_app import register


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

# Function to execute a query and return a single result
def execute_query(query):
    engine = create_connection()
    if engine:
        try:
            with engine.connect() as connection:
                result = connection.execute(text(query)).scalar()
                return result
        except Exception as e:
            st.error(f"Error: {e}")
            return None

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

# Fungsi untuk menggenerate ID baru
def generate_id(prefix):
    return prefix + str(uuid.uuid4().hex[:3]).upper()





# Main application
def main():
    
    st.session_state.logged_in = False

    # Aplikasi Streamlit
    st.title('Esport Database Viewer')
    
    page = st.sidebar.radio("Choose a page", ["Login", "Register"])
    if page == "Login":
        login()
    elif page == "Register":
        register()

    if st.session_state.logged_in:
        st.write("Welcome to Esport Database Viewer!")

        # Sidebar untuk navigasi
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Player", "Team", "Salary", "Schedule", "Event", "Sponsor"])

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

        # Navigasi ke halaman yang dipilih
        if page == "Player":
            player_data = load_data("Player")
            team_data = load_data("Team")
            player_team_data = load_data("Player_Team")
            
            st.subheader("Player Overview")
            
            st.markdown(css, unsafe_allow_html=True)

            st.markdown('<div class="player-container">', unsafe_allow_html=True)
            
            for _, row in player_data.iterrows():
                teams = player_team_data[player_team_data['Player_Player_ID'] == row['Player_ID']]
                team_names = [team_data.loc[team_data['Team_ID'] == team_id, 'Nama_Tim'].values[0] for team_id in teams['Team_Team_ID']]
                teams_str = ", ".join(team_names) if team_names else "No team assigned"
                
                st.markdown(f"""
                <div class="player-card">
                    <h4>{row['Nama']}</h4>
                    <p><b>Umur:</b> {row['Umur']}</p>
                    <p><b>Email:</b> {row['Email']}</p>
                    <p><b>Teams:</b> {teams_str}</p>
                    <p><b>Detail:</b> {row['Detail_Player']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Delete {row['Nama']}", key=f"delete_{row['Player_ID']}"):
                    delete_data("Player_Team", "Player_Player_ID", row['Player_ID'])
                    delete_data("Player", "Player_ID", row['Player_ID'])
                    st.experimental_rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Add New Player")
            with st.form("player_form"):
                nama = st.text_input("Nama")
                umur = st.number_input("Umur", min_value=1, max_value=100, step=1)
                email = st.text_input("Email")
                detail = st.text_input("Detail")
                team_id = st.selectbox("Assign to Team", team_data['Team_ID'].tolist(), format_func=lambda x: team_data.loc[team_data['Team_ID'] == x, 'Nama_Tim'].values[0])
                submitted = st.form_submit_button("Submit")
                if submitted:
                    player_id = generate_id("P")
                    
                    # Insert into Player table
                    query = f"INSERT INTO Player (Player_ID, Nama, Umur, Email, Detail_Player) VALUES ('{player_id}', '{nama}', {umur}, '{email}', '{detail}')"
                    insert_data(query)
                    
                    # Insert into Player_Team table
                    player_team_query = f"INSERT INTO Player_Team (Player_Player_ID, Team_Team_ID) VALUES ('{player_id}', '{team_id}')"
                    insert_data(player_team_query)
                    
                    st.success(f"Player '{nama}' added successfully to team '{team_data.loc[team_data['Team_ID'] == team_id, 'Nama_Tim'].values[0]}'!")
                    st.experimental_rerun()


        elif page == "Team":
            team_data = load_data("Team")
            player_team_data = load_data("Player_Team")
            player_data = load_data("Player")
            
            st.subheader("Team Overview")
            
            st.markdown(css, unsafe_allow_html=True)

            st.markdown('<div class="player-container">', unsafe_allow_html=True)
            
            for _, row in team_data.iterrows():
                players = player_team_data[player_team_data['Team_Team_ID'] == row['Team_ID']]
                player_names = [player_data.loc[player_data['Player_ID'] == player_id, 'Nama'].values[0] for player_id in players['Player_Player_ID']]
                players_str = ", ".join(player_names) if player_names else "No players assigned"
                
                st.markdown(f"""
                <div class="player-card">
                    <h4>{row['Nama_Tim']}</h4>
                    <p><b>Coach:</b> {row['Pelatih']}</p>
                    <p><b>Players:</b> {players_str}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Delete {row['Nama_Tim']}", key=f"delete_{row['Team_ID']}"):
                    delete_data("Player_Team", "Team_Team_ID", row['Team_ID'])
                    delete_data("Team", "Team_ID", row['Team_ID'])
                    st.experimental_rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Add New Team")
            with st.form("team_form"):
                team_name = st.text_input("Team Name")
                coach_name = st.text_input("Coach Name")
                submitted_team = st.form_submit_button("Create Team")
                
                if submitted_team and team_name and coach_name:
                    team_id = generate_id("T")
                    query = f"INSERT INTO Team (Team_ID, Nama_Tim, Pelatih) VALUES ('{team_id}', '{team_name}', '{coach_name}')"
                    insert_data(query)
                    st.success(f"Team '{team_name}' created successfully!")
                    st.experimental_rerun()

        elif page == "Salary":
            salary_data = load_data("Salary")
            player_data = load_data("Player")
            
            st.subheader("Salary Overview")
            salary_data = salary_data.merge(player_data[['Player_ID', 'Nama']], left_on='Player_Player_ID', right_on='Player_ID', how='left')
            st.markdown(css, unsafe_allow_html=True)
            salary_data.set_index('Nama', inplace=True)

            st.bar_chart(salary_data['Jumlah_Pembayar'])

            st.markdown('<div class="player-container">', unsafe_allow_html=True)

            # Display total average salary of all players
            st.subheader("Total Average Salary of All Players")
            query = "SELECT CalculateTotalAverageSalary()"
            total_avg_salary = execute_query(query)
            if total_avg_salary is not None:
                st.write(f"**Total Average Salary**: {total_avg_salary}")
            else:
                st.write("Failed to retrieve total average salary.")

            
            for _, row in salary_data.iterrows():
                st.markdown(f"""
                <div class="player-card">
                    <h4>{row.name}</h4>
                    <p><b>Jumlah Pembayar:</b> {row['Jumlah_Pembayar']}</p>
                    <p><b>Tanggal Pembayar:</b> {row['Tanggal_Pembayar']}</p>
                    <p><b>Deskripsi:</b> {row['Deskripsi']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Delete Salary for {row.name}", key=f"delete_{row['Salary_ID']}"):
                    delete_data("Salary", "Salary_ID", row['Salary_ID'])
                    st.experimental_rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Add New Salary")
            with st.form("salary_form"):
                player_dict = dict(zip(player_data['Nama'], player_data['Player_ID']))
                player_name = st.selectbox("Player", list(player_dict.keys()))
                player_id = player_dict[player_name]
                jumlah_pembayar = st.number_input("Jumlah Pembayar", min_value=0.0, step=0.01)
                tanggal_pembayar = st.date_input("Tanggal Pembayar")
                deskripsi = st.text_input("Deskripsi")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    salary_id = generate_id("S")
                    query = f"INSERT INTO Salary (Salary_ID, Jumlah_Pembayar, Tanggal_Pembayar, Deskripsi, Player_Player_ID) VALUES ('{salary_id}', {jumlah_pembayar}, '{tanggal_pembayar}', '{deskripsi}', '{player_id}')"
                    insert_data(query)
                    st.experimental_rerun()

        elif page == "Schedule":
            schedule_data = load_data("Schedule")
            team_data = load_data("Team")
            
            st.subheader("Schedule Overview")
            st.markdown(css, unsafe_allow_html=True)

            def format_timedelta(td):
                if pd.isna(td):
                    return "None"
                total_seconds = int(td.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours:02}:{minutes:02}:{seconds:02}"

            schedule_data = schedule_data.merge(team_data[['Team_ID', 'Nama_Tim']], left_on='Team_Team_ID', right_on='Team_ID', how='left')

            # Display total events for each team
            st.subheader("Total Schedule for Each Team")
            for _, row in team_data.iterrows():
                team_id = row['Team_ID']
                team_name = row['Nama_Tim']
                query = f"SELECT CalculateTotalSchedules('{team_id}')"
                total_sched = execute_query(query)
                if total_sched is not None:
                    st.write(f"**{team_name}**: {total_sched} schedules")
                else:
                    st.write(f"**{team_name}**: Failed to retrieve total schedules")

            for _, row in schedule_data.iterrows():
                if isinstance(row['Waktu_Mulai'], pd.Timestamp):
                    start_time = row['Waktu_Mulai'].strftime("%H:%M:%S")
                else:
                    start_time = format_timedelta(row['Waktu_Mulai'])

                if isinstance(row['Waktu_Selesai'], pd.Timestamp):
                    end_time = row['Waktu_Selesai'].strftime("%H:%M:%S")
                else:
                    end_time = format_timedelta(row['Waktu_Selesai'])

                st.markdown(f"""
                <div class="player-card">
                    <h3>{row['Jenis_Kegiatan']}</h3>
                    <p>{row['Nama_Tim']}</p>
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
                team_id = st.selectbox("Team", team_data['Team_ID'].tolist(), format_func=lambda x: team_data.loc[team_data['Team_ID'] == x, 'Nama_Tim'].values[0])
                submitted = st.form_submit_button("Submit")
                if submitted:
                    schedule_id = generate_id("SC")
                    query = f"INSERT INTO Schedule (Schedule_ID, Jenis_Kegiatan, Tanggal_Kegiatan, Waktu_Mulai, Waktu_Selesai, Team_Team_ID) VALUES ('{schedule_id}', '{jenis_kegiatan}', '{tanggal_kegiatan}', '{waktu_mulai}', '{waktu_selesai}', '{team_id}')"
                    insert_data(query)

        if page == "Event":
            event_data = load_data("Event")
            schedule_data = load_data("Schedule")
            team_data = load_data("Team")

            st.subheader("Event Overview")
            
            st.markdown(css, unsafe_allow_html=True)

            # Menggabungkan data event dengan data schedule dan team
            event_data = event_data.merge(schedule_data, left_on='Schedule_Schedule_ID', right_on='Schedule_ID', how='left')
            event_data = event_data.merge(team_data[['Team_ID', 'Nama_Tim']], left_on='Team_Team_ID', right_on='Team_ID', how='left')

            for _, row in event_data.iterrows():
                start_time = (datetime.datetime.min + row['Waktu_Mulai']).time()
                end_time = (datetime.datetime.min + row['Waktu_Selesai']).time()
                st.markdown(f"""
                <div class="player-card">
                    <h4>{row['Jenis_Event']} - {row['Tanggal_Event']}</h4>
                    <p>{row['Deskripsi_Event']}</p>
                    <p><b>Jenis Kegiatan:</b> {row['Jenis_Kegiatan']}</p>
                    <p><b>Tanggal Kegiatan:</b> {row['Tanggal_Kegiatan']}</p>
                    <p><b>Waktu Mulai:</b> {start_time.strftime('%H:%M')}</p>
                    <p><b>Waktu Selesai:</b> {end_time.strftime('%H:%M')}</p>
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
                schedule_nama = st.selectbox("Nama Kegiatan", schedule_data['Jenis_Kegiatan'].tolist())
                submitted = st.form_submit_button("Submit")
                if submitted:
                    event_id = generate_id("E")
                    schedule_id = schedule_data[schedule_data['Jenis_Kegiatan'] == schedule_nama]['Schedule_ID'].values[0]
                    query = f"INSERT INTO Event (Event_ID, Jenis_Event, Tanggal_Event, Deskripsi_Event, Schedule_Schedule_ID) VALUES ('{event_id}', '{jenis_event}', '{tanggal_event}', '{deskripsi_event}', '{schedule_id}')"
                    insert_data(query)

        elif page == "Sponsor":
            sponsor_data = load_data("Sponsor")
            
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
            
            for _, row in sponsor_data.iterrows():
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
                # Load sponsor and team data
                sponsor_data = load_data("Sponsor")
                team_data = load_data("Team")

                # Create dictionaries to map names to IDs
                sponsor_dict = dict(zip(sponsor_data['Nama_Sponsor'], sponsor_data['Sponsor_ID']))
                team_dict = dict(zip(team_data['Nama_Tim'], team_data['Team_ID']))

                # Use selectbox with names, but store IDs
                sponsor_name = st.selectbox("Sponsor", list(sponsor_dict.keys()))
                team_name = st.selectbox("Team", list(team_dict.keys()))

                submitted = st.form_submit_button("Submit")
                if submitted:
                    sponsor_id = sponsor_dict[sponsor_name]
                    team_id = team_dict[team_name]
                    query = f"INSERT INTO Sponsor_Team (Sponsor_ID, Team_ID) VALUES ('{sponsor_id}', '{team_id}')"
                    insert_data(query)
                    st.success(f"Added relationship: Sponsor '{sponsor_name}' with Team '{team_name}'")

if __name__ == "__main__":
    main()

