import streamlit as st

# Configure the app page structure securely
st.set_page_config(page_title="State House Girls Kitchen AI", layout="wide")


# --- CUSTOM STATE HOUSE GIRLS AI ENGINE ---
def calculate_chef_portions(base_students, attendance_pct, menu_item):
    expected_diners = base_students * (attendance_pct / 100.0)

    # Custom Menu Demands & Real Student Behaviors
    menu_factor = 1.00
    if menu_item == "Githeri":
        menu_factor = 0.60  # 📉 High bun-hoarding / lunch-skipping day
    elif menu_item in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
        menu_factor = 0.65  # 📉 High canteen flight risk
    elif menu_item == "Ugali, Bitterherbs & Meat":
        menu_factor = 1.00
    elif "Pilau" in menu_item:
        menu_factor = 1.20  # ⬆️ High demand on Saturdays
    elif "Rice" in menu_item:
        menu_factor = 1.10  # ⬆️ Rice is highly popular

    return round(expected_diners * menu_factor)


# --- UI DISPLAY SETUP ---
st.title("🍳 State House Girls Smart Kitchen Tool")
st.subheader("Advanced Custom Menu & Ingredient Weight Calculator")
st.markdown("---")

# Left Sidebar Controls for Kitchen Staff
st.sidebar.header("🏫 School Enrollment")
student_count = st.sidebar.number_input(
    "Total Students to Cook For:",
    min_value=10,
    max_value=3000,
    value=800,
    step=50,
)

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
        "Githeri & Bananas",
    ],
)

attendance = st.sidebar.slider("Expected Attendance (%)", 50, 120, 100)

# Run target metrics calculation
portions = calculate_chef_portions(student_count, attendance, menu_choice)

st.write("### 📊 Chef's Daily Cooking Guide")
st.metric(label="🔥 BASE PORTIONS TO PREPARE", value=f"{portions} Plates")

# Dynamic smart alerts for the kitchen staff
if menu_choice == "Githeri":
    st.error(
        "⚠️ **AI Alert:** Portions slashed by 40%. High number of students expected to skip lunch or eat buns!"
    )
elif menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
    st.warning(
        "⚠️ **AI Alert:** Portions reduced by 35%. Students heavily prefer the canteen today!"
    )
elif menu_choice == "Ugali, Bitterherbs & Meat":
    st.info(
        "💡 **AI Alert:** Budgeting for meat and ugali only. Students typically skip the bitterherbs today."
    )
elif "Pilau" in menu_choice:
    st.success(
        "🎉 **AI Alert:** Extra portions added! High turnout expected for Saturday Pilau."
    )

st.markdown("---")

# --- WASTE LEDGER & AI ADJUSTMENT ---
st.write("### 📉 Yesterday's Waste Tracker")
st.write(
    "Enter how much food was thrown away yesterday. The AI will automatically subtract this from today's store harvest to prevent over-cooking."
)

col_waste1, col_waste2 = st.columns(2)
with col_waste1:
    yesterday_waste_kgs = st.number_input(
        "Yesterday's Thrown Away Food (in KGs):",
        min_value=0.0,
        max_value=500.0,
        value=0.0,
        step=1.0,
    )


# --- INGREDIENT WEIGHT PLANNER ---
st.write("### ⚖️ Raw Ingredient Weight Planner")
st.write(
    "Adjust how many grams of each raw ingredient go onto a single plate. The AI calculates the total KGs, minus the waste."
)


# Helper calculation function that applies the smart waste reduction drop
def calculate_net_kgs(total_portions, grams_per_plate, waste_reduction_kgs):
    base_kgs = (total_portions * grams_per_plate) / 1000
    net_kgs = max(0.0, base_kgs - waste_reduction_kgs)
    return round(net_kgs, 1), round(base_kgs, 1)


# Creating a clean layout structure
col1, col2, col3, col4 = st.columns(4)

with col1:
    ing1_name = st.text_input(
        "Ingredient 1 Name:", value="Main Carb (e.g., Rice/Ugali)"
    )
    ing1_grams = st.number_input(
        "Grams per plate (Ing 1):", min_value=0, max_value=1000, value=150, step=10
    )
    ing1_kgs, ing1_base = calculate_net_kgs(
        portions, ing1_grams, yesterday_waste_kgs
    )
    st.metric(
        label=f"Total {ing1_name} Needed",
        value=f"{ing1_kgs} KGs",
        delta=(
            f"-{yesterday_waste_kgs} KG Waste Trim"
            if yesterday_waste_kgs > 0
            else None
        ),
    )

with col2:
    ing2_name = st.text_input(
        "Ingredient 2 Name:", value="Protein/Legume (e.g., Beans)"
    )
    default_prot = (
        100
        if menu_choice not in ["Ugali & Bitterherbs", "Ugali & Cabbage"]
        else 0
    )
    ing2_grams = st.number_input(
        "Grams per plate (Ing 2):", min_value=0, max_value=1000, value=default_prot, step=10
    )
    ing2_kgs, ing2_base = calculate_net_kgs(
        portions, ing2_grams, yesterday_waste_kgs * 0.5
    )
    st.metric(label=f"Total {ing2_name} Needed", value=f"{ing2_kgs} KGs")

with col3:
    ing3_name = st.text_input(
        "Ingredient 3 Name:", value="Vegetable (e.g., Cabbage)"
    )
    if menu_choice in [
        "Ugali, Bitterherbs & Meat",
        "Githeri",
        "Githeri & Bananas",
    ]:
        default_veg = 0
    elif menu_choice in ["Ugali & Bitterherbs", "Ugali & Cabbage"]:
        default_veg = 100
    else:
        default_veg = 50
    ing3_grams = st.number_input(
        "Grams per plate (Ing 3):", min_value=0, max_value=1000, value=default_veg, step=10
    )
    ing3_kgs, _ = calculate_net_kgs(portions, ing3_grams, 0)
    st.metric(label=f"Total {ing3_name} Needed", value=f"{ing3_kgs} KGs")

with col4:
    ing4_name = st.text_input("Ingredient 4 Name:", value="Extras (e.g., Bananas)")
    default_extra = 120 if menu_choice == "Githeri & Bananas" else 0
    ing4_grams = st.number_input(
        "Grams per plate (Ing 4):", min_value=0, max_value=1000, value=default_extra, step=10
    )
    ing4_kgs, _ = calculate_net_kgs(portions, ing4_grams, 0)
    st.metric(label=f"Total {ing4_name} Needed", value=f"{ing4_kgs} KGs")
