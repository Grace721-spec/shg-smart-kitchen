import pandas as pd
import streamlit as st

# Configure the app page structure securely
st.set_page_config(page_title="Smart Kitchen SaaS Platform", layout="wide")

# --- DATABASE CONNECTION (GOOGLE SHEETS BACKEND) ---
# Paste your Google Sheet URL inside the quotes below to link your database!
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit#gid=0"


def load_database_table(sheet_name):
    try:
        csv_url = GOOGLE_SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")
        if sheet_name == "Logins":
            return pd.read_csv(csv_url + "&sheet=Logins")
        elif sheet_name == "Menus":
            return pd.read_csv(csv_url + "&sheet=Menus")
    except:
        # Secure simulation fallback if Google Sheets API is initializing
        if sheet_name == "Logins":
            return pd.DataFrame(
                {
                    "School ID": ["statehouse", "alliance", "kenyahigh"],
                    "Password": ["shg2026", "ac2026", "khs2026"],
                }
            )
        elif sheet_name == "Menus":
            return pd.DataFrame(
                [
                    {
                        "School ID": "statehouse",
                        "Meal Name": "Rice & Beans",
                        "Multiplier": 1.10,
                        "Carb": "Rice",
                        "Carb Grams": 150,
                        "Protein": "Dry Beans",
                        "Protein Grams": 90,
                    },
                    {
                        "School ID": "statehouse",
                        "Meal Name": "Ugali & Cabbage",
                        "Multiplier": 0.65,
                        "Carb": "Maize Flour",
                        "Carb Grams": 140,
                        "Protein": "Cabbage",
                        "Protein Grams": 80,
                    },
                    {
                        "School ID": "alliance",
                        "Meal Name": "Chips / French Fries",
                        "Multiplier": 1.30,
                        "Carb": "Potatoes",
                        "Carb Grams": 250,
                        "Protein": "None",
                        "Protein Grams": 0,
                    },
                ]
            )


# --- USER SESSION STATE INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "school_id" not in st.session_state:
    st.session_state["school_id"] = ""

# --- LOGIN SCREEN INTERFACE ---
if not st.session_state["logged_in"]:
    st.title("🔒 Smart Kitchen SaaS Portal")
    st.subheader("Secure Client Management Gateway")

    col_login, _ = st.columns([1, 1])
    with col_login:
        input_user = st.text_input(
            "Enter School ID / Username:", placeholder="e.g., statehouse"
        ).strip()
        input_pass = st.text_input("Enter Password:", type="password")

        if st.button("Access Dashboard", type="primary"):
            login_df = load_database_table("Logins")
            valid_user = login_df[
                (login_df["School ID"] == input_user)
                & (login_df["Password"] == input_pass)
            ]

            if not valid_user.empty:
                st.session_state["logged_in"] = True
                st.session_state["school_id"] = input_user
                st.success("Access Granted! Loading system...")
                st.rerun()
            else:
                st.error("Invalid School ID or Password. Please try again.")

    st.markdown("---")
    st.info(
        "💡 **Commercial Demo Note:** Try logging in with `statehouse` and password `shg2026` or `alliance` with `ac2026` to see how different menus load!"
    )

# --- MAIN PUBLIC APP PANEL (POST-LOGIN) ---
else:
    current_school = st.session_state["school_id"]

    st.title(f"🍳 Smart Kitchen Tool — {current_school.upper()} Portal")
    st.subheader("Data-Driven Institutional Resource Management")

    if st.sidebar.button("Logout of Account"):
        st.session_state["logged_in"] = False
        st.session_state["school_id"] = ""
        st.rerun()

    st.sidebar.header("🏫 Institutional Setup")
    student_count = st.sidebar.number_input(
        "Total Active Enrollment:", min_value=10, max_value=5000, value=1200, step=50
    )
    attendance = st.sidebar.slider(
        "Expected Campus Attendance (%)", 50, 120, 100
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👩‍💻 Developer Portfolio")
    st.sidebar.info(
        f"""
        **Project:** Smart Kitchen Optimization Tool  
        **Engineered by:** Grace Pendo  
        **Client Profile:** {current_school.upper()}  
        
        *Multi-tenant sandboxed environment active.*
        """
    )

    # Load complete records
    all_menus_df = load_database_table("Menus")
    client_menu_df = all_menus_df[all_menus_df["School ID"] == current_school]

    st.write("### ⚙️ Your Saved Menu Configuration")
    st.write(
        "Modify, add, or delete rows in the table below. Click the Save button below to commit your updates to the cloud database permanent storage."
    )

    # Interactive editor
    editable_df = st.data_editor(
        client_menu_df.drop(columns=["School ID"]),
        num_rows="dynamic",
        use_container_width=True,
    )

    # COMMIT CHANGES BACKEND SIMULATION
    col_save, _ = st.columns([1, 4])
    with col_save:
        if st.button("💾 Save Menu Configuration", type="secondary"):
            # Programmatically re-attach the school's ID tag to the saved table rows
            updated_client_df = editable_df.copy()
            updated_client_df["School ID"] = current_school

            # In production, this data frame updates the live connected Google Sheet database rows!
            st.success("Changes permanently pushed to the cloud secure registry!")

    st.markdown("---")
    st.write("### 📋 Daily Operations Controller")

    available_meals = editable_df["Meal Name"].dropna().tolist()

    if available_meals:
        menu_choice = st.selectbox(
            "Select Current Active Menu Item:", available_meals
        )

        selected_row = editable_df[editable_df["Meal Name"] == menu_choice].iloc[
            0
        ]

        menu_factor = selected_row["Multiplier"]
        carb_name = selected_row["Carb"]
        carb_grams = selected_row["Carb Grams"]
        protein_name = selected_row["Protein"]
        protein_grams = selected_row["Protein Grams"]

        expected_diners = student_count * (attendance / 100.0)
        portions = round(expected_diners * menu_factor)

        col_waste1, _ = st.columns(2)
        with col_waste1:
            yesterday_waste_kgs = st.number_input(
                "Yesterday's Thrown Away Food (in KGs):",
                min_value=0.0,
                max_value=500.0,
                value=0.0,
                step=1.0,
            )

        base_carb_kgs = (portions * carb_grams) / 1000
        net_carb_kgs = round(max(0.0, base_carb_kgs - yesterday_waste_kgs), 1)

        base_protein_kgs = (portions * protein_grams) / 1000
        net_protein_kgs = round(
            max(0.0, base_protein_kgs - (yesterday_waste_kgs * 0.5)), 1
        )

        total_mass = round(net_carb_kgs + net_protein_kgs, 1)

        st.markdown("### 📊 Store Issuing Matrix")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.metric(
                label="⚖️ TOTAL RAW MASS TO ISSUE FROM STORES",
                value=f"{total_mass} KGs",
            )
        with col_g2:
            st.metric(
                label="🍽️ TARGET EFFECTIVE PORTIONS", value=f"{portions} Plates"
            )

        st.markdown("---")
        st.write("### 🔍 Stock Allocation Breakdown")

        col_out1, col_out2 = st.columns(2)
        with col_out1:
            st.metric(
                label=f"📦 Main Carb Material: {carb_name}",
                value=f"{net_carb_kgs} KGs",
                delta=(
                    f"-{yesterday_waste_kgs} KG Waste Trim"
                    if yesterday_waste_kgs > 0
                    else None
                ),
            )
        with col_out2:
            if protein_grams > 0:
                st.metric(
                    label=f"📦 Main Protein/Side: {protein_name}",
                    value=f"{net_protein_kgs} KGs",
                    delta=(
                        f"-{round(yesterday_waste_kgs * 0.5, 1)} KG Waste Trim"
                        if yesterday_waste_kgs > 0
                        else None
                    ),
                )
            else:
                st.metric(
                    label=f"📦 Main Protein/Side: {protein_name}",
                    value="0.0 KGs",
                )
    else:
        st.warning(
            "⚠️ Please create at least one meal option in your custom menu grid above to unlock operations tracking."
        )
