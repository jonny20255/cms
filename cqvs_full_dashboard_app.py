import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- Load Data ---
@st.cache_data
def load_data():
    scans = pd.read_csv("Scans data - Sheet1.csv")
    vehicles = pd.read_csv("Vehicles data - Sheet1.csv")
    refills = pd.read_csv("refills data - Sheet1.csv")
    clients = pd.read_csv("clients_contacts/SE - QLD - Sites 20d6ed160c548001939bd5fd1fe1f212.csv")
    return scans, vehicles, refills, clients

scans, vehicles, refills, clients = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("CMS Navigation")
tabs = ["Dashboard", "Vehicles", "Scans", "Refills", "Clients", "Contacts", "Tasks"]
page = st.sidebar.radio("Go to", tabs)

# --- Dashboard Tab ---
if page == "Dashboard":
    st.title("📊 Vehicle Wash Dashboard")
    st.write("This view summarises wash data trends, alerts and performance.")

    # Filters
    site_filter = st.selectbox("Filter by Site", ["All"] + sorted(scans["Site"].dropna().unique()))
    filtered_scans = scans.copy()
    if site_filter != "All":
        filtered_scans = filtered_scans[filtered_scans["Site"] == site_filter]

    st.subheader("Wash Activity - Last 7 Days")
    filtered_scans['Created'] = pd.to_datetime(filtered_scans['Created'], errors='coerce')
    recent = filtered_scans[filtered_scans['Created'] > (datetime.now() - pd.Timedelta(days=7))]
    st.write(str(len(recent)) + " washes recorded in the past 7 days.")

    st.subheader("Top Vehicles by Wash Count")
    top = recent['Vehicle Name'].value_counts().head(5)
    st.bar_chart(top)

# --- Vehicles Tab ---
elif page == "Vehicles":
    st.title("🚛 Vehicle Directory")
    st.dataframe(vehicles)

# --- Scans Tab ---
elif page == "Scans":
    st.title("🧼 Wash Scan Logs")
    st.dataframe(scans)

# --- Refills Tab ---
elif page == "Refills":
    st.title("🧪 Chemical Refills")
    st.dataframe(refills)

# --- Clients Tab ---
elif page == "Clients":
    st.title("🏢 Client Sites and Notes")
    st.dataframe(clients)

# --- Contacts Tab ---
elif page == "Contacts":
    st.title("📇 Contacts")
    st.info("Contact details pulled from client data and markdowns (to be parsed).")

# --- Tasks Tab ---
elif page == "Tasks":
    st.title("✅ Tasks")
    st.write("This tab will eventually track internal tasks.")
