import pandas as pd
import streamlit as st

# Configure the app
st.set_page_config(page_title="Smart Kitchen SaaS", layout="wide")

# --- DATABASE CONNECTION ---
SHEET_ID = "1Z59JKDFF3zbCctIgcb9u2xJkN0gYlT4VlIVYw1eCRlo"

def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

# --- LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("Smart Kitchen Login")
    user = st.text_input("School Name")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        df_logins = load_data("Logins")
        if not df_logins[(df_logins["School Name"] == user) & (df_logins["Password"] == pwd)].empty:
            st.session_state["logged_in"] = True
            st.session_state["school"] = user
            st.rerun()
        else:
            st.error("Invalid Login")
else:
    # --- APP CONTENT ---
    st.title(f"Kitchen Dashboard: {st.session_state['school']}")
    
    menus = load_data("Menus")
    client_menu = menus[menus["School Name"] == st.session_state["school"]]
    
    st.write("### Today's Menu")
    st.dataframe(client_menu)
    
    meal = st.selectbox("Select Meal", client_menu["Meal Name"].tolist())
    row = client_menu[client_menu["Meal Name"] == meal].iloc[0]
    
    students = st.number_input("Enrollment", value=1200)
    portions = students * row["Multiplier"]
    
    col1, col2 = st.columns(2)
    col1.metric("Carb (KG)", round((portions * row["Carb Grams"])/1000, 2))
    col2.metric("Protein (KG)", round((portions * row["Protein Grams"])/1000, 2))
