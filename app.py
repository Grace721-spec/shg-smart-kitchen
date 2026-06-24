import streamlit as st

st.set_page_config(page_title="Smart Kitchen Manager", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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
        if password == st.secrets[school_map[school]]:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password.")
else:
    st.title("🥗 Smart Kitchen Manager")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("👥 Attendance")
    num_students = st.number_input("Number of Students Present", min_value=0, value=1000)

    st.header("📋 Select Daily Menu & Grams")
    col1, col2, col3, col4 = st.columns(4)
    
    # Updated Carb Options including Wheat Flour
    carb = col1.selectbox("Carb", ["None", "Maize Flour (Ugali)", "Rice", "Potatoes", "Maize (Dry)", "Wheat Flour (Chapati)"])
    carb_g = col1.number_input("Grams/Stud (Carb)", value=150)
    
    protein = col2.selectbox("Protein", ["None", "Beans", "Meat", "Eggs", "Lentils", "Green Grams", "Peas"])
    prot_g = col2.number_input("Grams/Stud (Prot)", value=90)
    
    veg = col3.selectbox("Veg", ["None", "Cabbage", "Spinach", "Kales"])
    veg_g = col3.number_input("Grams/Stud (Veg)", value=80)
    
    fruit = col4.selectbox("Fruit", ["None", "Mango", "Orange", "Banana"])
    fruit_g = col4.number_input("Grams/Stud (Fruit)", value=120)

    st.subheader("📊 Requirements (Calculated)")
    c1, c2, c3, c4 = st.columns(4)
    if carb != "None": c1.metric(carb, f"{(num_students * carb_g) / 1000:.1f} Kgs")
    if protein != "None": c2.metric(protein, f"{(num_students * prot_g) / 1000:.1f} Kgs")
    if veg != "None": c3.metric(veg, f"{(num_students * veg_g) / 1000:.1f} Kgs")
    if fruit != "None": c4.metric(fruit, f"{(num_students * fruit_g) / 1000:.1f} Kgs")

    st.divider()

    st.header("📊 Waste, Saved & Shortage Tracker")
    w1, w2 = st.columns(2)
    food_wasted = w1.number_input("Food Wasted (Kgs)", min_value=0.0, step=0.1)
    food_saved = w2.number_input("Food Saved (Kgs)", min_value=0.0, step=0.1)
    
    shortage_reported = st.checkbox("Did food run out? (Shortage)")
    shortage_deficit = 0.0
    if shortage_reported:
        st.subheader("⚠️ Shortage Details")
        col_s1, col_s2 = st.columns(2)
        initial_cooked = col_s1.number_input("Original Amount Cooked (Kgs)", min_value=0.0, step=0.1)
        needed_to_feed = col_s2.number_input("Amount Needed to Feed All (Kgs)", min_value=0.0, step=0.1)
        shortage_deficit = max(0.0, needed_to_feed - initial_cooked)
        st.write(f"**Calculated Shortage Deficit: {shortage_deficit:.1f} Kgs**")

    if st.button("Submit Daily Report"):
        st.success("Report submitted successfully!")
