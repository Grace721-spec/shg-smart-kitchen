import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Smart Kitchen App", layout="centered")

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login System ---
if not st.session_state.logged_in:
    st.title("🔐 Smart Kitchen Login")
    school = st.selectbox("Select Your School", ["Alliance Girls High School", "State House Girls High School", "Other"])
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        # Replace 'admin123' with your actual secure password
        if password == "admin123": 
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password.")
else:
    # --- Main Application (After Login) ---
    st.title("🥗 Smart Kitchen Manager")
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- Attendance & Calculator Module ---
    st.header("👥 Attendance")
    num_students = st.number_input("Number of Students Present", min_value=0, value=1000, step=1)

    st.header("📋 Select Daily Menu & Grams")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        carb = st.selectbox("Carb", ["Maize Flour (Ugali)", "Rice", "Potatoes"])
        carb_g = st.number_input("Grams/Stud (Carb)", value=150)
    with col2:
        protein = st.selectbox("Protein", ["Beans", "Meat", "Eggs"])
        prot_g = st.number_input("Grams/Stud (Prot)", value=90)
    with col3:
        veg = st.selectbox("Veg", ["Cabbage", "Spinach", "Kales"])
        veg_g = st.number_input("Grams/Stud (Veg)", value=80)
    with col4:
        fruit = st.selectbox("Fruit", ["Mango", "Orange", "Banana"])
        fruit_g = st.number_input("Grams/Stud (Fruit)", value=120)

    st.subheader("📊 Requirements (Calculated)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(carb, f"{(num_students * carb_g) / 1000:.1f} Kgs")
    c2.metric(protein, f"{(num_students * prot_g) / 1000:.1f} Kgs")
    c3.metric(veg, f"{(num_students * veg_g) / 1000:.1f} Kgs")
    c4.metric(fruit, f"{(num_students * fruit_g) / 1000:.1f} Kgs")

    st.divider()

    # --- Waste & Shortage Tracker Module ---
    st.header("📊 Waste & Shortage Tracker")
    w1, w2, w3 = st.columns(3)

    with w1:
        food_wasted = st.number_input("Food Wasted (Kgs)", min_value=0.0, step=0.1)
    with w2:
        food_saved = st.number_input("Food Saved (Kgs)", min_value=0.0, step=0.1)
    with w3:
        shortage_reported = st.checkbox("Did food run out? (Shortage)")

    if st.button("Submit Daily Report"):
        st.success("Report submitted successfully!")
        
        # Feedback logic
        if shortage_reported:
            st.warning("⚠️ Shortage detected: Please increase portion estimates for the next batch.")
        elif food_wasted > 5.0:
            st.info("📉 High waste detected: Consider slightly reducing portions to save resources.")
        else:
            st.write("✅ Consumption is balanced. Keep up the efficiency!")
