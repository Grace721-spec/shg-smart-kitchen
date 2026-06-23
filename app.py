import streamlit as st

# School Login Data
school_passwords = {
    "Alliance Girls High School": "AGHS2026", "Alliance High School": "AHS2026",
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

# Login Logic
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

    # 1. User-Editable Menu (The "Old" way you liked)
    st.subheader("📋 Edit Today's Menu")
    carb_item = st.text_input("Carbohydrate", "Rice")
    carb_grams = st.number_input("Grams per student", value=150)
    
    protein_item = st.text_input("Protein", "Dry beans")
    protein_grams = st.number_input("Grams per student", value=90)

    veg_item = st.text_input("Vegetable", "Cabbage")
    veg_grams = st.number_input("Grams per student", value=80)

    fruit_item = st.text_input("Fruit", "Banana")
    fruit_grams = st.number_input("Grams per student", value=120)

    # 2. Calculation
    st.subheader("🧮 Ingredient Requirements")
    num_students = st.number_input("Number of Students", min_value=0, value=1000, step=50)

    if st.button("Calculate"):
        st.write(f"**Calculated Requirements for {num_students} students:**")
        st.info(f"{carb_item}: {(num_students * carb_grams/1000):.1f} Kgs")
        st.info(f"{protein_item}: {(num_students * protein_grams/1000):.1f} Kgs")
        st.info(f"{veg_item}: {(num_students * veg_grams/1000):.1f} Kgs")
        st.info(f"{fruit_item}: {(num_students * fruit_grams/1000):.1f} Kgs")

    st.markdown("---")

    # 3. Waste Tracker
    st.subheader("📉 Waste & Savings Tracker")
    wasted = st.number_input("Food Wasted (Kgs)", min_value=0.0)
    saved = st.number_input("Food Saved (Kgs)", min_value=0.0)
    
    if st.button("Submit Waste Report"):
        if wasted > saved:
            st.error(f"Net Loss: {wasted - saved:.1f} Kgs")
        else:
            st.success(f"Net Efficiency: Saved {saved - wasted:.1f} Kgs!")
