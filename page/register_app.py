import streamlit as st
import bcrypt
from database.user_database.login import create_connection

def register():
    st.title("Register")

    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    password_confirmation = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != password_confirmation:
            st.error("Passwords do not match")
        else:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                st.error("Username already taken")
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                connection.commit()
                st.success("Registration successful! You can now login.")
            cursor.close()
            connection.close()

if __name__ == "__main__":
    register()
