import streamlit as st
import mysql.connector
import hashlib

#Database Connection Function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="Muthu44P@",     
        database="USERS"      
    )

#Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Registration Function
def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

#Login Verification Function
def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        stored_password = result[0]
        return hash_password(password) == stored_password
    return False

#Symptom Checker Section
def symptom_checker(username):
    st.subheader(f"Welcome {username}! Please Enter Your Symptoms:")
    symptoms = st.text_area("Describe your symptoms (Example: fever, cough, sore throat...)")

    if st.button("Check Possible Conditions"):
        if "fever" in symptoms.lower():
            st.success("Possible Conditions: Flu, COVID-19, Dengue, Typhoid.")
        elif "pain" in symptoms.lower():
            st.success("Possible Conditions: Arthritis, Muscle Strain, Injury.")
        elif "cough" in symptoms.lower():
            st.success("Possible Conditions: Common Cold, COVID-19, Bronchitis.")
        else:
            st.warning("No direct match found. Please consult a medical professional for proper diagnosis.")

#Streamlit UI
st.set_page_config(page_title="Medical Symptom Checker", page_icon="💉", layout="centered")
st.title("Medical_Symptom_checker - Login Page")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Select Option", menu)

#Session state for user authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""

#Login Page
if choice == "Login":
    st.subheader("Login Section")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success(f"Welcome {username}! You have successfully logged in.")
        else:
            st.error("Invalid Username or Password.")

#Registration Page
elif choice == "Register":
    st.subheader("Register Section")
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')

    if st.button("Register"):
        if register_user(new_user, new_password):
            st.success("Account created successfully! You can now log in.")
        else:
            st.warning("Username already exists. Please try another.")

#After Login: Show Symptom Checker
if st.session_state.logged_in:
    symptom_checker(st.session_state.user)

