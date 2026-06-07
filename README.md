# shg-smart-kitchen 
import streamlit as st

st.set_page_config(page_title="State House Girls Kitchen AI", layout="wide")

# --- CUSTOM STATE HOUSE GIRLS AI ENGINE ---
def calculate_chef_portions(base_students, attendance_pct, historical_waste_pct, menu_item):
    expected_diners = base_students * (attendance_pct / 100.0)
    
    # Custom Menu Demands & Real Student Behaviors
    menu_factor = 1.00
    
    if menu_item == "Githeri":
        # 📉 High bun-hoarding and lunch-skipping day! Slash portions by 40%
        menu_factor = 0.60  
    elif menu_item in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
        # 📉 High canteen flight risk! Reduce portions by 35%
        menu_factor = 0.65  
    elif menu_item == "Ugali, Bitterherbs & Meat":
        # Students prefer to have Ugali and Meat only, skipping the greens
        menu_factor = 1.00 
    elif "Pilau" in menu_item:
        menu_factor = 1.20  # ⬆️ High demand on Saturdays!
    elif "Rice" in menu_item:
        menu_factor = 1.10  # ⬆️ Rice is highly popular
        
    # Plate waste trim
    waste_trim = 1.0 - (historical_waste_pct / 100.0 * 0.5) if historical_waste_pct > 10 else 1.0
    
    return round(expected_diners * menu_factor * waste_trim)

st.title("🍳 State House Girls Smart Kitchen Tool")
st.subheader("Advanced Custom Menu & Ingredient Weight Calculator")
st.markdown("---")

# Left Sidebar Controls
st.sidebar.header("🏫 School Enrollment")
student_count = st.sidebar.number_input("Total Students to Cook For:", min_value=10, max_value=3000, value=800, step=50)

st.sidebar.markdown("---")
st.sidebar.header("📋 Today's Menu Selection")
menu_choice = st.sidebar.selectbox(
    "What is on the Menu Today?", 
    [
        "Rice & Beans", 
        "Rice & Green Grams", 
        "Ugali & Bitterherbs", 
        "Ugali & Cabbage", 
        "Ugali, Bitterherbs & Meat", 
        "Saturday Pilau (with Meat/Green Grams)", 
        "Githeri", 
        "Githeri & Bananas"
    ]
)

attendance = st.sidebar.slider("Expected Attendance (%)", 50, 120, 100)
waste = st.sidebar.slider("Recent Plate Waste (%)", 0, 50, 10)

# Run portion calculation
portions = calculate_chef_portions(student_count, attendance, waste, menu_choice)

st.write("### 📊 Chef's Daily Cooking Guide")
st.metric(label="🔥 EXACT PORTIONS TO PREPARE", value=f"{portions} Plates")

# Dynamic smart alerts for the kitchen staff
if menu_choice == "Githeri":
    st.error("⚠️ **AI Alert:** Portions slashed by 40%. High number of students expected to skip lunch or eat buns bought yesterday!")
elif menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
    st.warning("⚠️ **AI Alert:** Portions reduced by 35%. Students heavily prefer the canteen when plain greens are served!")
elif menu_choice == "Ugali, Bitterherbs & Meat":
    st.info("💡 **AI Alert:** Budgeting for meat and ugali only. Students typically skip the bitterherbs today.")
elif "Pilau" in menu_choice:
    st.success("🎉 **AI Alert:** Extra portions added! High turnout expected for Saturday Pilau.")

st.markdown("---")

# --- FREE WILL INGREDIENT CALCULATOR ---
st.write("### ⚖️ Raw Ingredient Weight Planner")
st.write("Chefs can type or adjust how many grams of each raw ingredient go onto a single plate. The AI will instantly calculate the total Kilograms (KGs) to harvest from the store.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ing1_name = st.text_input("Ingredient 1 Name:", value="Main Carb (e.g., Rice/Ugali/Maize)")
    ing1_grams = st.number_input("Grams per plate (Ing 1):", min_value=0, max_value=1000, value=150, step=10)
    ing1_kgs = round((portions * ing1_grams) / 1000, 1)
    st.metric(label=f"Total {ing1_name} Needed", value=f"{ing1_kgs} KGs")

with col2:
    ing2_name = st.text_input("Ingredient 2 Name:", value="Protein/Legume (e.g., Beans/Beans in Githeri)")
    default_prot = 100
    if menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
        default_prot = 0
    ing2_grams = st.number_input("Grams per plate (Ing 2):", min_value=0, max_value=1000, value=default_prot, step=10)
    ing2_kgs = round((portions * ing2_grams) / 1000, 1)
    st.metric(label=f"Total {ing2_name} Needed", value=f"{ing2_kgs} KGs")

with col3:
    ing3_name = st.text_input("Ingredient 3 Name:", value="Vegetable (e.g., Cabbage)")
    if menu_choice in ["Ugali, Bitterherbs & Meat", "Githeri", "Githeri & Bananas"]:
        default_veg = 0 
    elif menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
        default_veg = 100 
    else:
        default_veg = 50
    ing3_grams = st.number_input("Grams per plate (Ing 3):", min_value=0, max_value=1000, value=default_veg, step=10)
    ing3_kgs = round((portions * ing3_grams) / 1000, 1)
    st.metric(label=f"Total {ing3_name} Needed", value=f"{ing3_kgs} KGs")

with col4:
    ing4_name = st.text_input("Ingredient 4 Name:", value="Extras (e.g., Bananas)")
    default_extra = 120 if menu_choice == "Githeri & Bananas" else 0
    ing4_grams = st.number_input("Grams per plate (Ing 4):", min_value=0, max_value=1000, value=default_extra, step=10)
    ing4_kgs = round((portions * ing4_grams) / 1000, 1)
    st.metric(label=f"Total {ing4_name} Needed", value=f"{ing4_kgs} KGs")
