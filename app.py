import streamlit as st
import pandas as pd

# Configure the app
st.set_page_config(page_title="Smart Kitchen Network AI", layout="wide")

# Google Sheet ID
SHEET_ID = "1gG2Y8lD2W2MhN0_m3aTzNl-vB2S_eC6F_wNpxfMco_w"

@st.cache_data(ttl=60)
def load_sheet_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        return pd.read_csv(url)
    except Exception:
        return None

# Global Shared Component: Dynamic Ingredient Planner
def render_ingredient_planner(portions, menu_choice, suffix=""):
    st.write("### ⚖️ Raw Ingredient Weight Planner")
    st.caption("Adjust the grams per plate below. The AI instantly calculates total Kilograms (KGs) needed from the store.")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ing1_name = st.text_input("Carb Ingredient Name:", value="Main Carb (Rice/Ugali/Maize)", key=f"ing1_n_{suffix}")
        ing1_grams = st.number_input("Grams per plate:", min_value=0, max_value=1000, value=150, step=10, key=f"ing1_g_{suffix}")
        st.metric(label=f"Total {ing1_name}", value=f"{round((portions * ing1_grams) / 1000, 1)} KGs")
    with col2:
        ing2_name = st.text_input("Protein Ingredient Name:", value="Protein (Beans/Beef/Ndengu)", key=f"ing2_n_{suffix}")
        default_prot = 0 if any(g in menu_choice for g in ["Bitterherbs", "Cabbage", "Greens"]) else 100
        ing2_grams = st.number_input("Grams per plate:", min_value=0, max_value=1000, value=default_prot, step=10, key=f"ing2_g_{suffix}")
        st.metric(label=f"Total {ing2_name}", value=f"{round((portions * ing2_grams) / 1000, 1)} KGs")
    with col3:
        ing3_name = st.text_input("Vegetable Ingredient Name:", value="Vegetables (Cabbage/Sukuma)", key=f"ing3_n_{suffix}")
        default_veg = 100 if any(g in menu_choice for g in ["Bitterherbs", "Cabbage", "Greens"]) else 50
        if "Githeri" in menu_choice: default_veg = 0
        ing3_grams = st.number_input("Grams per plate:", min_value=0, max_value=1000, value=default_veg, step=10, key=f"ing3_g_{suffix}")
        st.metric(label=f"Total {ing3_name}", value=f"{round((portions * ing3_grams) / 1000, 1)} KGs")
    with col4:
        ing4_name = st.text_input("Extras Ingredient Name:", value="Extras (Fruit/Cooking Oil/Onions)", key=f"ing4_n_{suffix}")
        default_extra = 120 if "Bananas" in menu_choice else 0
        ing4_grams = st.number_input("Grams per plate:", min_value=0, max_value=1000, value=default_extra, step=10, key=f"ing4_g_{suffix}")
        st.metric(label=f"Total {ing4_name}", value=f"{round((portions * ing4_grams) / 1000, 1)} KGs")

# Global Shared Component: Wastage & Emergency Shortage Tracker (with Actionable AI Solutions)
def render_waste_shortage_tracker(planned_portions, suffix=""):
    st.markdown("---")
    st.write("### 📉 Waste, Shortage, & Emergency Cooking Tracker")
    st.caption("Log kitchen performance data below to receive real-time AI solutions and smart optimizations.")
    
    w_col1, w_col2 = st.columns(2)
    
    with w_col1:
        st.markdown("#### 🗑️ Food Wastage Audit")
        leftover_plates = st.number_input("Plates worth of food thrown away / left in giant pots:", min_value=0, value=0, step=5, key=f"left_p_{suffix}")
        
        if planned_portions > 0:
            waste_pct = round((leftover_plates / planned_portions) * 100, 1)
            st.metric(label="Actual Food Waste Rate", value=f"{waste_pct}%", delta=f"{leftover_plates} Plates Lost", delta_color="inverse")
            
            if leftover_plates > 0:
                st.markdown("##### 💡 AI Recommendation for Next Time:")
                if waste_pct > 15:
                    st.error(f"👉 **Action Item:** Reduce your baseline 'Expected Attendance Buffer' slider by **{round(waste_pct - 5)}%** for this meal next week. Students are heavily bypassing this menu for the canteen or hoarding snacks.")
                elif waste_pct > 5:
                    st.warning(f"👉 **Action Item:** Trim your portions slightly. Drop your baseline target by **{leftover_plates} plates** next time to hit a zero-waste balance.")
                else:
                    st.success("✨ **Excellent Efficiency:** Waste is under 5%. Keep your cooking baseline exactly where it is!")

    with w_col2:
        st.markdown("#### ⚠️ Emergency Shortages & Extra Cooking")
        shortage_occurred = st.checkbox("Did food run short before all students finished eating?", key=f"short_cb_{suffix}")
        
        if shortage_occurred:
            extra_cooked = st.number_input("Emergency extra plates chefs had to prepare on the fly:", min_value=1, value=10, step=5, key=f"extra_p_{suffix}")
            st.metric(label="Total Meals Served (Planned + Emergency)", value=f"{planned_portions + extra_cooked} Plates")
            
            st.markdown("##### 💡 AI Recommendation for Next Time:")
            st.error(f"👉 **Action Item:** The kitchen was under-prepared today. Next time this menu is served, manually increase your 'Expected Attendance' slider by **15%** or pre-budget an extra **{extra_cooked} plates** into the store harvest weights to avoid emergency cooking pressures.")
        else:
            if leftover_plates == 0:
                st.success("✨ **Perfect Balance achieved today!** Food was perfectly sufficient for all lines, and no emergency secondary cooking was required.")

# --- MAIN APP ROUTING ---
st.title("🎛️ National School Smart Kitchen Network")
st.subheader("Select your school to access your custom AI calculator profile")

school_choice = st.selectbox(
    "Choose School Profile:",
    [
        "Select a school...",
        "State House Girls' High School",
        "Alliance High School",
        "St. George's Girls' Secondary School",
        "Lenana School",
        "Nairobi School"
    ]
)

st.markdown("---")

if school_choice != "Select a school...":
    
    # 1. Menu Modification Controller
    st.sidebar.header("📋 Menu Management")
    menu_mode = st.sidebar.radio("Menu Selection Mode:", ["Use Default Preset Lists", "Type Custom Menu Manually"])
    
    # Configuration profiles map
    if "State House" in school_choice:
        school_id, def_enroll, def_menus = "shg", 800, ["Rice & Beans", "Rice & Green Grams", "Ugali & Bitterherbs", "Ugali & Cabbage", "Ugali, Bitterherbs & Meat", "Saturday Pilau (with Meat/Green Grams)", "Githeri", "Githeri & Bananas"]
    elif "Alliance" in school_choice:
        school_id, def_enroll, def_menus = "ahs", 1200, ["Ugali & Beef Stew", "Rice & Beans", "Githeri", "Murram (Maize & Beans Extra)", "Rice & Beef Veg Stew"]
    elif "St. George" in school_choice:
        school_id, def_enroll, def_menus = "stg", 1000, ["Rice & Yellow Beans", "Chapati & Ndengu (Green Grams)", "Ugali & Sukuma Wiki", "Githeri Special"]
    elif "Lenana" in school_choice:
        school_id, def_enroll, def_menus = "len", 1100, ["Ugali & Sukuma with Meat", "Rice & Njahi (Black Beans)", "Githeri Mixed", "Rice & Beans Premium"]
    else:
        school_id, def_enroll, def_menus = "nch", 1300, ["Rice & Beans Classic", "Ugali & Cabbage Mixed", "Patch Special Githeri", "Rice & Chicken/Meat Stew"]

    # Handle dynamic typewriter menus
    if menu_
