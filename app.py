import streamlit as st
import pandas as pd

# Configure the app
st.set_page_config(page_title="Smart Kitchen Tool", layout="wide")

# Google Sheet ID from our agreement
SHEET_ID = "1gG2Y8lD2W2MhN0_m3aTzNl-vB2S_eC6F_wNpxfMco_w"

@st.cache_data(ttl=60)
def load_sheet_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        return pd.read_csv(url)
    except Exception:
        return None

# --- APP START: NO PASSWORD, JUST ASK SCHOOL ---
st.title("🍳 Smart Kitchen Management AI")
st.subheader("Select your school to access your custom AI calculator")

# 1. Ask which school is using the app
school_input = st.text_input("Enter School Name (e.g., State House Girls):", value="")

if school_input:
    # Standardize name for matching
    school_clean = school_input.strip().lower()
    
    if "state house" in school_clean:
        st.success("✅ State House Girls Profile Loaded!")
        st.markdown("---")
        
        # --- CUSTOM STATE HOUSE GIRLS AI ENGINE ---
        def calculate_chef_portions(base_students, attendance_pct, historical_waste_pct, menu_item):
            expected_diners = base_students * (attendance_pct / 100.0)
            menu_factor = 1.00

            if menu_item == "Githeri":
                menu_factor = 0.60  # 📉 40% slash for bun hoarding
            elif menu_item in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
                menu_factor = 0.65  # 📉 35% reduction for canteen flight risk
            elif menu_item == "Ugali, Bitterherbs & Meat":
                menu_factor = 1.00 
            elif "Pilau" in menu_item:
                menu_factor = 1.20  # ⬆️ Saturday Pilau high demand
            elif "Rice" in menu_item:
                menu_factor = 1.10  # ⬆️ General Rice popularity
                
            waste_trim = 1.0 - (historical_waste_pct / 100.0 * 0.5) if historical_waste_pct > 10 else 1.0
            return round(expected_diners * menu_factor * waste_trim)

        # Main Dashboard Layout
        st.title("🍳 State House Girls Smart Kitchen Tool")
        st.subheader("Advanced Custom Menu & Ingredient Weight Calculator")
        
        # Left Sidebar Controls
        st.sidebar.header("🏫 School Enrollment")
        student_count = st.sidebar.number_input("Total Students to Cook For:", min_value=10, max_value=3000, value=800, step=50)
        st.sidebar.markdown("---")
        st.sidebar.header("📋 Today's Menu Selection")
        
        # Pull dynamic menus from your Sheet or fall back to defaults
        menu_df = load_sheet_data("Menus")
        if menu_df is not None and not menu_df.empty:
            menu_options = menu_df.iloc[:, 0].dropna().tolist()
        else:
            menu_options = [
                "Rice & Beans", "Rice & Green Grams", "Ugali & Bitterherbs", 
                "Ugali & Cabbage", "Ugali, Bitterherbs & Meat", 
                "Saturday Pilau (with Meat/Green Grams)", "Githeri", "Githeri & Bananas"
            ]
            
        menu_choice = st.sidebar.selectbox("What is on the Menu Today?", menu_options)
        attendance = st.sidebar.slider("Expected Attendance (%)", 50, 120, 100)
        waste = st.sidebar.slider("Recent Plate Waste (%)", 0, 50, 10)

        # Calculations & Metrics
        portions = calculate_chef_portions(student_count, attendance, waste, menu_choice)
        st.write("### 📊 Chef's Daily Cooking Guide")
        st.metric(label="🔥 EXACT PORTIONS TO PREPARE", value=f"{portions} Plates")

        # Smart Alerts
        if menu_choice == "Githeri":
            st.error("⚠️ AI Alert: Portions slashed by 40%. High number of students expected to skip lunch or eat buns bought yesterday!")
        elif menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
            st.warning("⚠️ AI Alert: Portions reduced by 35%. Students heavily prefer the canteen when plain greens are served!")
        elif "Pilau" in menu_choice:
            st.success("🎉 AI Alert: Extra portions added! High turnout expected for Saturday Pilau.")
        st.markdown("---")

        # --- RAW INGREDIENT CALCULATOR ---
        st.write("### ⚖️ Raw Ingredient Weight Planner")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ing1_name = st.text_input("Ingredient 1 Name:", value="Main Carb (e.g., Rice/Ugali)")
            ing1_grams = st.number_input("Grams per plate (Ing 1):", min_value=0, max_value=1000, value=150, step=10)
            st.metric(label=f"Total {ing1_name}", value=f"{round((portions * ing1_grams) / 1000, 1)} KGs")
        with col2:
            ing2_name = st.text_input("Ingredient 2 Name:", value="Protein (e.g., Beans)")
            default_prot = 0 if menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"] else 100
            ing2_grams = st.number_input("Grams per plate (Ing 2):", min_value=0, max_value=1000, value=default_prot, step=10)
            st.metric(label=f"Total {ing2_name}", value=f"{round((portions * ing2_grams) / 1000, 1)} KGs")
        with col3:
            ing3_name = st.text_input("Ingredient 3 Name:", value="Vegetables")
            default_veg = 100 if menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"] else 50
            if menu_choice in ["Githeri", "Githeri & Bananas"]: default_veg = 0
            ing3_grams = st.number_input("Grams per plate (Ing 3):", min_value=0, max_value=1000, value=default_veg, step=10)
            st.metric(label=f"Total {ing3_name}", value=f"{round((portions * ing3_grams) / 1000, 1)} KGs")
        with col4:
            ing4_name = st.text_input("Ingredient 4 Name:", value="Extras (e.g., Bananas)")
            default_extra = 120 if menu_choice == "Githeri & Bananas" else 0
            ing4_grams = st.number_input("Grams per plate (Ing 4):", min_value=0, max_value=1000, value=default_extra, step=10)
            st.metric(label=f"Total {ing4_name}", value=f"{round((portions * ing4_grams) / 1000, 1)} KGs")

    else:
        # Standard Generic System for other schools entered
        st.info(f"ℹ️ Loaded general configuration for {school_input}. Custom menu parameters are pulled from base defaults.")
        st.markdown("---")
        st.write("### 📊 General Cooking Portion Tool")
        student_count = st.number_input("Enrollment:", value=500)
        st.write("Portion adjustment set to 100% standard baseline.")
        st.metric(label="Portions", value=f"{student_count} Plates")

st.markdown("---")
st.caption("AI engine for state house girls kitchen management created by Grace Pendo a grade 10 student in 2026")
