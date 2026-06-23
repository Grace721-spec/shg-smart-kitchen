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
    # 3. Main Dashboard
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.title(f"Smart Kitchen: {st.session_state.school}")

    # Menu Input
    st.subheader("📋 Daily Menu & Ingredients")
    menu_name = st.text_input("Today's Menu")
    ingredients = st.text_area("List Ingredients (e.g., Flour, Beef, Tomatoes)")
    if st.button("Save Menu"):
        st.success(f"Menu for '{menu_name}' saved.")

    st.markdown("---")

    # Calculator with High-Energy Toggle
    st.subheader("🧮 Smart Requirement Calculator")
    num_students = st.number_input("Number of Students Present", min_value=1, value=1000)
    energy_level = st.radio("Serving Intensity", ["Standard", "High-Energy (Sports)"])
    
    # Logic: 0.15kg (150g) vs 0.20kg (200g)
    multiplier = 0.15 if energy_level == "Standard" else 0.20

    if st.button("Calculate Daily Needs"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Maize Flour (Kgs)", f"{num_students * 0.25:.1f}")
        col2.metric("Proteins (Kgs)", f"{num_students * multiplier:.1f}")
        col3.metric("Vegetables (Kgs)", f"{num_students * 0.10:.1f}")

    st.markdown("---")

    # Waste Tracker
    st.subheader("📉 Waste Tracker")
    waste_kgs = st.number_input("Enter Kgs of food wasted", min_value=0.0, step=0.5)

    if waste_kgs > 10:
        st.error("⚠️ High waste detected! Please review portion sizes.")
    elif waste_kgs > 0:
        st.warning(f"⚠️ {waste_kgs} Kgs wasted. Let's aim for zero!")
    else:
        st.success("🎉 Amazing work! No food wasted today. You are a sustainable champion!")
