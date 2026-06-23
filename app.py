import streamlit as st

# School Data
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

    # 4-Column Ingredient Calculator
    st.subheader("🧮 Ingredient Requirements")
    num_students = st.number_input("Number of Students Present", min_value=0, value=1000, step=50)
    
    # We use 4 columns for the 4 key ingredients
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.write("**Carbohydrates**")
        carb_name = st.text_input("Item 1", "Ugali Flour")
        st.metric(f"{carb_name} (Kgs)", f"{num_students * 0.25:.1f}")
        
    with c2:
        st.write("**Proteins**")
        prot_name = st.text_input("Item 2", "Beans")
        st.metric(f"{prot_name} (Kgs)", f"{num_students * 0.15:.1f}")
        
    with c3:
        st.write("**Vegetables**")
        veg_name = st.text_input("Item 3", "Cabbage")
        st.metric(f"{veg_name} (Kgs)", f"{num_students * 0.10:.1f}")
        
    with c4:
        st.write("**Other (Oil/Salt)**")
        other_name = st.text_input("Item 4", "Cooking Oil")
        st.metric(f"{other_name} (Liters/Kgs)", f"{num_students * 0.02:.1f}")

    st.markdown("---")

    # Waste & Savings
    st.subheader("📉 Waste & Savings Tracker")
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        wasted = st.number_input("Food Wasted (Kgs)", min_value=0.0, step=0.5)
    with w_col2:
        saved = st.number_input("Food Saved (Kgs)", min_value=0.0, step=0.5)

    if wasted > saved:
        st.error(f"⚠️ Net Loss: {wasted - saved:.1f} Kgs. Let's look for ways to reduce prep waste!")
    else:
        st.success(f"🎉 Net Efficiency: You successfully managed or saved {saved - wasted:.1f} Kgs today!")
