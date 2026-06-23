import streamlit as st

# Updated School Login Data
school_passwords = {
    "Alliance Girls High School": "AGHS2026", "Alliance High School": "AHS2026",
    "Moi Girls Nairobi": "MGN2026", # Added school
    "Highridge Girls Secondary School": "HGSS2026", "Jamhuri High School": "JHS2026",
    "Kenya High School": "KHS2026", "Lenana School": "LS2026",
    "Limuru Girls' School": "LGS2026", "Mang'u High School": "MHS2026",
    "Nairobi School": "NS2026", "Pangani Girls High School": "PGHS2026",
    "St. George’s Girls’ Secondary School": "SGGS2026", "Starehe Boys' Centre": "SBC2026",
    "Starehe Girls' Centre": "SGC2026", "State House Boys High School": "SHB2026",
    "State House Girls High School": "SHG2026", "The Aga Khan High School - Nairobi": "AKHS2026",
    "Upper Hill School": "UHS2026"
}

st.set_page_config(page_title="Smart Kitchen App", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
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
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.title(f"Smart Kitchen: {st.session_state.school}")

    st.subheader("👥 Attendance")
    num_students = st.number_input("Number of Students Present", min_value=0, value=1000, step=50)
    
    st.markdown("---")

    # Horizontal Ingredient Selectors with Default Lists
    st.subheader("📋 Select Daily Menu & Grams")
    cols = st.columns(4)
    
    # Ingredient Lists
    carbs = ["Maize Flour (Ugali)", "Rice", "Wheat Flour (Chapati)"]
    proteins = ["Beans", "Green Grams", "Meat", "Chicken", "Peas"]
    veggies = ["Cabbage", "Kales", "Spinach"]
    fruits = ["Banana", "Apple", "Orange"]

    with cols[0]:
        carb_name = st.selectbox("Carb", carbs)
        carb_g = st.number_input("Grams/Stud", value=150)
    with cols[1]:
        prot_name = st.selectbox("Protein", proteins)
        prot_g = st.number_input("Grams/Stud ", value=90)
    with cols[2]:
        veg_name = st.selectbox("Veg", veggies)
        veg_g = st.number_input("Grams/Stud  ", value=80)
    with cols[3]:
        fruit_name = st.selectbox("Fruit", fruits)
        fruit_g = st.number_input("Grams/Stud   ", value=120)

    # Calculation
    st.subheader("🧮 Requirements")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{carb_name}", f"{(num_students * carb_g / 1000):.1f} Kgs")
    c2.metric(f"{prot_name}", f"{(num_students * prot_g / 1000):.1f} Kgs")
    c3.metric(f"{veg_name}", f"{(num_students * veg_g / 1000):.1f} Kgs")
    c4.metric(f"{fruit_name}", f"{(num_students * fruit_g / 1000):.1f} Kgs")
