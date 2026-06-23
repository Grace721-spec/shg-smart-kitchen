import streamlit as st

# 1. School Data Dictionary
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

# 2. Login Logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Centralized Login Form
    st.title("🔐 Smart Kitchen Login")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_school = st.selectbox("Select Your School", list(school_passwords.keys()))
        password = st.text_input("Enter Password", type="password")
        
        if st.button("Login"):
            if password == school_passwords.get(selected_school):
                st.session_state.logged_in = True
                st.session_state.school = selected_school
                st.rerun()
            else:
                st.error("Incorrect password!")
else:
    # 3. Main Dashboard (Your original structure)
    st.title(f"Smart Kitchen Management: {st.session_state.school}")
    
    tab1, tab2 = st.tabs(["📊 Inventory & Stats", "🧮 Food Requirement Calculator"])

    with tab1:
        st.subheader("Manage Inventory")
        st.write("Track your proteins, vegetables, and food waste here.")
        # Add your inventory display code here

    with tab2:
        st.subheader("Food Requirement Calculator")
        num_students = st.number_input("Enter Number of Students", min_value=0, value=500)
        
        if st.button("Calculate Needed Kgs"):
            st.write(f"**Based on {num_students} students, you need:**")
            st.success(f"Maize Flour: {num_students * 0.25} Kgs")
            st.success(f"Beans: {num_students * 0.15} Kgs")
            st.success(f"Vegetables: {num_students * 0.10} Kgs")

    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
