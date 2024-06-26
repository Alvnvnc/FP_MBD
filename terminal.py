import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Fungsi untuk membuat koneksi ke database menggunakan mysql.connector
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='esport_db',
            user='alvn',
            password='Vincent35$'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Fungsi untuk menjalankan kueri SQL
def run_query(query):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            if query.strip().lower().startswith('select'):
                records = cursor.fetchall()
                columns = cursor.column_names
                df = pd.DataFrame(records, columns=columns)
                return df
            else:
                connection.commit()
                return None
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Aplikasi Streamlit
st.title('MySQL Terminal')

st.subheader("Enter SQL Query")

query = st.text_area("SQL Query", height=150)
if st.button("Execute"):
    if query.strip():
        result = run_query(query)
        if result is not None:
            st.write(result)
        else:
            st.success("Query executed successfully.")
