import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# --- Embedded refill forecast data ---
refill_stats = json.loads("""[
  {
    "Site": "Beenleigh",
    "Last Refill": "2025-06-20",
    "Avg Refill Gap (days)": 30.0,
    "Next Refill Forecast": "2025-07-20",
    "Days Since Last": 2,
    "Avg Volume (L)": 500.0,
    "Avg Cost ($AUD)": 1925.0
  },
  {
    "Site": "Benowa",
    "Last Refill": "2025-07-31",
    "Avg Refill Gap (days)": 36.0,
    "Next Refill Forecast": "2025-09-05",
    "Days Since Last": -39,
    "Avg Volume (L)": 450.0,
    "Avg Cost ($AUD)": 1605.83
  },
  {
    "Site": "Browns Plains",
    "Last Refill": "2025-06-27",
    "Avg Refill Gap (days)": 15.5,
    "Next Refill Forecast": "2025-07-12",
    "Days Since Last": -5,
    "Avg Volume (L)": 400.0,
    "Avg Cost ($AUD)": 1350.0
  },
  {
    "Site": "Caloundra",
    "Last Refill": "2025-07-09",
    "Avg Refill Gap (days)": 14.0,
    "Next Refill Forecast": "2025-07-23",
    "Days Since Last": -17,
    "Avg Volume (L)": 500.5,
    "Avg Cost ($AUD)": 2325.0
  },
  {
    "Site": "Capalaba",
    "Last Refill": "2025-07-09",
    "Avg Refill Gap (days)": 11.7,
    "Next Refill Forecast": "2025-07-20",
    "Days Since Last": -17,
    "Avg Volume (L)": 356.8,
    "Avg Cost ($AUD)": 1235.81
  },
  {
    "Site": "Everton Park",
    "Last Refill": "2025-07-16",
    "Avg Refill Gap (days)": 21.7,
    "Next Refill Forecast": "2025-08-06",
    "Days Since Last": -24,
    "Avg Volume (L)": 325.2,
    "Avg Cost ($AUD)": 1205.0
  },
  {
    "Site": "Geebung",
    "Last Refill": "2025-08-04",
    "Avg Refill Gap (days)": 56.0,
    "Next Refill Forecast": "2025-09-29",
    "Days Since Last": -43,
    "Avg Volume (L)": 650.0,
    "Avg Cost ($AUD)": 2502.5
  },
  {
    "Site": "Labrador",
    "Last Refill": "2025-07-18",
    "Avg Refill Gap (days)": 19.7,
    "Next Refill Forecast": "2025-08-06",
    "Days Since Last": -26,
    "Avg Volume (L)": 237.8,
    "Avg Cost ($AUD)": 946.88
  },
  {
    "Site": "Murarrie",
    "Last Refill": "2025-06-27",
    "Avg Refill Gap (days)": 8.4,
    "Next Refill Forecast": "2025-07-05",
    "Days Since Last": -5,
    "Avg Volume (L)": 400.4,
    "Avg Cost ($AUD)": 1330.62
  },
  {
    "Site": "Narangba",
    "Last Refill": "2025-07-23",
    "Avg Refill Gap (days)": 25.7,
    "Next Refill Forecast": "2025-08-17",
    "Days Since Last": -31,
    "Avg Volume (L)": 575.2,
    "Avg Cost ($AUD)": 1945.0
  },
  {
    "Site": "Redbank",
    "Last Refill": "2025-05-21",
    "Avg Refill Gap (days)": 7.5,
    "Next Refill Forecast": "2025-05-28",
    "Days Since Last": 32,
    "Avg Volume (L)": 217.0,
    "Avg Cost ($AUD)": 729.17
  },
  {
    "Site": "Wacol",
    "Last Refill": "2025-06-27",
    "Avg Refill Gap (days)": 30.0,
    "Next Refill Forecast": "2025-07-27",
    "Days Since Last": -5,
    "Avg Volume (L)": 616.7,
    "Avg Cost ($AUD)": 2374.17
  }
]""")
df_refill_stats = pd.DataFrame(refill_stats)

st.set_page_config(page_title="CQVS CMS", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Sites", "Refill Forecast"])

# --- Dashboard ---
if page == "Dashboard":
    st.title("📊 Wash Dashboard")
    st.write("This would include wash metrics, charts, and site performance (placeholder).")

# --- Sites ---
elif page == "Sites":
    st.title("📍 Sites Overview")
    st.dataframe(df_refill_stats)

# --- Forecast Tab ---
elif page == "Refill Forecast":
    st.title("⏳ Refill Forecast & Alerts")

    st.dataframe(df_refill_stats)

    st.subheader("🔻 Low Inventory")
    for row in refill_stats:
        if row['Days Since Last'] > row['Avg Refill Gap (days)'] * 1.25:
            st.error(f"{row['Site']}: Refill overdue ({row['Days Since Last']} days since last refill)")

    st.subheader("📆 Next Refill Plan")
    for row in refill_stats:
        st.write(f"{row['Site']} → Next Refill: **{row['Next Refill Forecast']}** (avg every {row['Avg Refill Gap (days)']} days)")
