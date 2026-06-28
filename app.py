import streamlit as st

st.set_page_config(page_title="Smart Kitchen Manager", layout="centered")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login Logic ---
if not st.session_state.logged_in:
    st.title("🔐 Smart Kitchen Login")
    school_map = {
        "Alliance Girls High School": "AGHS", "Alliance High School": "AHS",
        "Moi Girls Nairobi": "MGN", "Highridge Girls Secondary School": "HGSS",
        "Jamhuri High School": "JHS", "Kenya High School": "KHS",
        "Lenana School": "LS", "Limuru Girls' School": "LGS",
        "Mang'u High School": "MHS", "Nairobi School": "NS",
        "Pangani Girls High School": "PGHS", "St. George’s Girls’ Secondary School": "SGGS",
        "Starehe Boys' Centre": "SBC", "Starehe Girls' Centre": "SGC",
        "State House Boys High School": "SHB", "State House Girls High School": "SHG",
        "The Aga Khan High School - Nairobi": "AKHS", "Upper Hill School": "UHS"
    }
    school = st.selectbox("Select Your School", list(school_map.keys()))
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()

    # --- Signature Footer ---
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <p style="font-size: 16px;">App made by</p>
            <p style="font-family: 'Brush Script MT', cursive; font-size: 32px;">Grace Pendo</p>
            <p style="font-size: 14px;">State House Girls High School | 2026</p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    # --- Main App Content ---
    st.title("🥗 Smart Kitchen Manager")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("👥 Attendance")
    num_students = st.number_input("Number of Students Present", min_value=0, value=1000, step=100)

    st.header("📋 Select Daily Menu & Grams")
    col1, col2, col3, col4 = st.columns(4)
    
    carb_g = col1.number_input("Grams/Stud (Carb)", value=150, step=50)
    prot_g = col2.number_input("Grams/Stud (Prot)", value=100, step=50)
    veg_g = col3.number_input("Grams/Stud (Veg)", value=100, step=50)
    fruit_g = col4.number_input("Grams/Stud (Fruit)", value=100, step=50)

    st.subheader("📊 Requirements (Calculated)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Carbs", f"{(num_students * carb_g) / 1000:.1f} Kgs")
    c2.metric("Protein", f"{(num_students * prot_g) / 1000:.1f} Kgs")
    c3.metric("Veg", f"{(num_students * veg_g) / 1000:.1f} Kgs")
    c4.metric("Fruit", f"{(num_students * fruit_g) / 1000:.1f} Kgs")

    st.divider()

    st.header("📊 Waste & Shortage Tracker")
    w1, w2 = st.columns(2)
    food_wasted = w1.number_input("Food Wasted (Kgs)", min_value=0.0, step=0.5)
    shortage_reported = st.checkbox("Did food run out?")
    
    shortage_deficit = 0.0
    if shortage_reported:
        initial = st.number_input("Original Amount Cooked (Kgs)", min_value=0.0, step=1.0)
        needed = st.number_input("Amount Needed (Kgs)", min_value=0.0, step=1.0)
        shortage_deficit = max(0.0, needed - initial)
        st.write(f"**Calculated Shortage: {shortage_deficit:.1f} Kgs**")

    st.subheader("💡 Smart Kitchen Feedback")
    if shortage_reported and shortage_deficit > 0:
        st.warning(f"Oh no! We ran out. Please try adding {shortage_deficit:.1f} Kgs to your cooking for the next meal. You've got this!")
    elif food_wasted > 2.0:
        st.info(f"We noticed leftovers of {food_wasted:.1f} Kgs. Try cooking slightly less next time. Keep refining your portions!")
    else:
        st.success("Great job! You hit a perfect balance today. Continue in the same spirit!")

    if st.button("Submit Daily Report"):
        st.success("Report submitted successfully!")
