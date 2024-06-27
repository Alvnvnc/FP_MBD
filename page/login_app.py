import streamlit as st
import bcrypt
from database.user_database.login import create_connection

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            st.success("Logged In!")
            st.session_state.logged_in = True
        else:
            st.error("Incorrect username or password")

if __name__ == "__main__":
    login()
