import streamlit as st

# 1. School Login Data
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

    # Ingredient Calculator (Using database ratios) 
    st.subheader("🧮 Ingredient Requirements (Grams per student)")
    num_students = st.number_input("Number of Students Present", min_value=0, value=1000, step=50)
    
    c1, c2, c3, c4 = st.columns(4)
    
    # Calculations based on provided database 
    with c1:
        st.metric("Rice (Kgs)", f"{(num_students * 0.150):.1f}") # 150g 
    with c2:
        st.metric("Beans (Kgs)", f"{(num_students * 0.090):.1f}") # 90g 
    with c3:
        st.metric("Cabbage (Kgs)", f"{(num_students * 0.080):.1f}") # 80g 
    with c4:
        st.metric("Banana (Kgs)", f"{(num_students * 0.120):.1f}") # 120g 

    st.markdown("---")

    # Waste & Savings Tracker
    st.subheader("📉 Waste & Savings Tracker")
    w1, w2 = st.columns(2)
    with w1:
        wasted = st.number_input("Food Wasted (Kgs)", min_value=0.0, step=0.5, key="w1")
    with w2:
        saved = st.number_input("Food Saved (Kgs)", min_value=0.0, step=0.5, key="w2")

    if wasted > saved:
        st.error(f"⚠️ Net Loss: {wasted - saved:.1f} Kgs. Check your portions!")
    else:
        st.success(f"🎉 Net Efficiency: You saved {saved - wasted:.1f} Kgs today!")
