import pandas as pd
import streamlit as st

# Configure the app page structure
st.set_page_config(page_title="Smart Kitchen SaaS Platform", layout="wide")

# --- DATABASE CONNECTION ---
SHEET_ID = "1Z59JKDFF3zbCctIgcb9u2xJkN0gYlT4VlIVYw1eCRlo"

def load_database_table(sheet_name):
    # Using the standard Google Sheets CSV export format
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        # Clean column names by removing any accidental leading/trailing spaces
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "school_name" not in st.session_state:
    st.session_state["school_name"] = ""

# --- LOGIN SCREEN ---
if not st.session_state["logged_in"]:
    st.title("🔒 Smart Kitchen SaaS Portal")
    st.subheader("Secure Client Management Gateway")

    input_user = st.text_input("Enter School Name:", placeholder="e.g., statehouse").strip()
    input_pass = st.text_input("Enter Password:", type="password")

    if st.button("Access Dashboard", type="primary"):
        login_df = load_database_table("Logins")
        # Ensure we check the column name matches your sheet exactly
        valid_user = login_df[
            (login_df["School Name"].astype(str).str.strip() == input_user) & 
            (login_df["Password"].astype(str).str.strip() == input_pass)
        ]

        if not valid_user.empty:
            st.session_state["logged_in"] = True
            st.session_state["school_name"] = input_user
            st.rerun()
        else:
            st.error("Invalid credentials. Please check your spelling.")

# --- MAIN APP PANEL ---
else:
    current_school = st.session_state["school_name"]
    st.title(f"🍳 Smart Kitchen — {current_school.upper()}")

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    # Load data
    all_menus_df = load_database_table("Menus")
    
    # Filter for the specific school
    client_menu_df = all_menus_df[all_menus_df["School Name"].astype(str).str.strip() == current_school]

    st.write("### ⚙️ Your Saved Menu Configuration")
    # Display the editor
    editable_df = st.data_editor(client_menu_df.drop(columns=["School Name"]), num_rows="dynamic")

    # Operations Controller
    st.markdown("### 📋 Daily Operations Controller")
    available_meals = editable_df["Meal Name"].dropna().tolist()
    
    if available_meals:
        menu_choice = st.selectbox("Select Active Menu Item:", available_meals)
        selected_row = editable_df[editable_df["Meal Name"] == menu_choice].iloc[0]

        # Use 1200 as a default enrollment or pull from slider
        student_count = st.sidebar.number_input("Total Enrollment:", min_value=10, value=1200)
        attendance = st.sidebar.slider("Attendance %", 50, 100, 100)
        
        # Calculate portions
        portions = (student_count * (attendance/100)) * selected_row["Multiplier"]
        
        # Display Results
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(f"{selected_row['Carb']}", f"{round((portions * selected_row['Carb Grams'])/1000, 1)} KG")
        col2.metric(f"{selected_row['Protein']}", f"{round((portions * selected_row['Protein Grams'])/1000, 1)} KG")
        col3.metric(f"{selected_row['Vegetable']}", f"{round((portions * selected_row['Veg Grams'])/1000, 1)} KG")
        col4.metric(f"{selected_row['Fruit']}", f"{round((portions * selected_row['Fruit Grams'])/1000, 1)} KG")
    else:
        st.warning("No menu items found. Please check your Google Sheet 'Menus' tab.")
