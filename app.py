import streamlit as st

# 1. Define your school dictionary with passwords
school_passwords = {
    "Alliance Girls High School": "AGHS2026",
    "Alliance High School": "AHS2026",
    "Highridge Girls Secondary School": "HGSS2026",
    "Jamhuri High School": "JHS2026",
    "Kenya High School": "KHS2026",
    "Lenana School": "LS2026",
    "Limuru Girls' School": "LGS2026",
    "Mang'u High School": "MHS2026",
    "Nairobi School": "NS2026",
    "Pangani Girls High School": "PGHS2026",
    "St. George’s Girls’ Secondary School": "SGGS2026",
    "Starehe Boys' Centre": "SBC2026",
    "Starehe Girls' Centre": "SGC2026",
    "State House Boys High School": "SHB2026",
    "State House Girls High School": "SHG2026",
    "The Aga Khan High School - Nairobi": "AKHS2026",
    "Upper Hill School": "UHS2026"
}

st.set_page_config(page_title="Smart Kitchen App", layout="wide")

st.sidebar.title("Login Portal")

# 2. Selectbox for school
selected_school = st.sidebar.selectbox("Select Your School", list(school_passwords.keys()))

# 3. Password input
password = st.sidebar.text_input("Enter School Password", type="password")

# 4. Initialize session state to track login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 5. Login Logic
if st.sidebar.button("Login"):
    if password == school_passwords[selected_school]:
        st.session_state.logged_in = True
        st.session_state.school = selected_school
    else:
        st.error("Incorrect password!")

# 6. Main Dashboard Area
if st.session_state.logged_in:
    st.title(f"Smart Kitchen Management: {st.session_state.school}")
    st.success("You are logged in.")
    
    # --- ADD YOUR KITCHEN FEATURES HERE ---
    st.write("Manage your inventory, meal plans, and supply requests below.")
    # Example: st.button("Check Inventory")
    
else:
    st.title("Smart Kitchen Management System")
    st.info("Please select your school and enter the password in the sidebar to log in.")
