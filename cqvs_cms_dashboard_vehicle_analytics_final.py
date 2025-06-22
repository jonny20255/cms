
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CQVS CMS with Dashboard", layout="wide")
st.sidebar.title("CMS Navigation")
tab = st.sidebar.radio("Go to", ["Dashboard", "Sites", "Contacts", "Clients", "Jobs", "Tasks", "Vehicles"])

DATA_FILES = {
    "sites": "sites.csv",
    "contacts": "contacts.csv",
    "clients": "clients.csv",
    "jobs": "jobs.csv",
    "tasks": "tasks.csv",
    "refills": "refills.csv",
    "vehicles": "vehicles.csv"
}

# Load or init session state
for key, filename in DATA_FILES.items():
    if key not in st.session_state:
        if os.path.exists(filename):
            st.session_state[key] = pd.read_csv(filename).to_dict("records")
        else:
            st.session_state[key] = []

def save_data(key):
    pd.DataFrame(st.session_state[key]).to_csv(DATA_FILES[key], index=False)

def render_table(title, key):
    df = pd.DataFrame(st.session_state[key])
    st.subheader(title)

    if not df.empty:
        filter_text = st.text_input(f"Filter {key}", key=f"filter_{key}").lower()
        if filter_text:
            df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(filter_text).any(), axis=1)]
        st.dataframe(df)

        row_to_delete = st.number_input("Row # to delete", 0, len(df) - 1, 0, key=f"del_{key}")
        if st.button(f"Delete row from {key}"):
            st.session_state[key].pop(row_to_delete)
            save_data(key)
            st.success("Deleted row")
            st.experimental_rerun()

        row_to_edit = st.number_input("Row # to edit", 0, len(df) - 1, 0, key=f"edit_{key}")
        edited = {}
        for col in df.columns:
            default = df.iloc[row_to_edit][col]
            edited[col] = st.text_input(f"{col}", value=str(default), key=f"{key}_{col}_edit")
        if st.button(f"Save Edit to {key}"):
            idx = df.index[row_to_edit]
            st.session_state[key][idx] = edited
            save_data(key)
            st.success("Row updated")
            st.experimental_rerun()

        csv = df.to_csv(index=False)
        st.download_button("⬇ Export CSV", csv, file_name=DATA_FILES[key], mime="text/csv")
    else:
        st.info("No records yet.")

    st.markdown("### 📤 Bulk Upload CSV")
    uploaded = st.file_uploader("Upload CSV", type="csv", key=f"upload_{key}")
    if uploaded:
        df_new = pd.read_csv(uploaded)
        st.session_state[key].extend(df_new.to_dict("records"))
        save_data(key)
        st.success("Bulk upload complete")
        st.experimental_rerun()

# === Dashboard ===
if tab == "Dashboard":
    
    st.title("📊 Vehicle Wash Dashboard")

    with st.expander("Wash Performance Summary"):
        days_range = st.slider("Select Time Range (days)", 1, 30, 5)
        # Dummy data simulating average washes per truck
        summary_df = pd.DataFrame({
            "Vehicle": ["Truck 1", "Truck 2", "Truck 3"],
            "Avg Washes": [4, 6, 5],
            "Missed Washes": [2, 0, 0]
        })
        st.subheader(f"Average Washes & Missed Washes (Last {days_range} days)")
        st.dataframe(summary_df)

        st.markdown("### Wash Success Score (out of 100)")
        st.markdown("- Truck 1: 🟠 79")
        st.markdown("- Truck 2: 🟠 61")
        st.markdown("- Truck 3: 🟠 67")

        st.markdown("### Wash Count Chart")
        st.bar_chart(summary_df.set_index("Vehicle")["Avg Washes"])

        st.markdown("### Alerts")
        for i, row in summary_df.iterrows():
            if row["Missed Washes"] > 0:
                st.warning(f"{row['Vehicle']} missed {row['Missed Washes']} washes in last {days_range} days")


    col1, col2 = st.columns(2)

    with col1:
        job_df = pd.DataFrame(st.session_state["jobs"])
        st.subheader("Jobs Summary")
        if not job_df.empty:
            job_status_counts = job_df["Status"].value_counts().to_dict()
            for status, count in job_status_counts.items():
                st.write(f"{status}: {count}")
        else:
            st.write("No job data available")

    with col2:
        refill_df = pd.DataFrame(st.session_state.get("refills", []))
        st.subheader("Refill History")
        if not refill_df.empty:
            if "Date" in refill_df.columns:
                refill_df["Date"] = pd.to_datetime(refill_df["Date"], errors="coerce")
                latest = refill_df["Date"].max()
                earliest = refill_df["Date"].min()
                st.write(f"Latest refill: {latest.date()}")
                st.write(f"Earliest refill: {earliest.date()}")
                st.write(f"Total refills: {len(refill_df)}")
            if "Litres" in refill_df.columns:
                total_litres = refill_df["Litres"].sum()
                st.write(f"Total litres refilled: {total_litres:.2f}")
        else:
            st.write("No refill data available")

# === Other Tabs ===

elif tab == "Sites":
    st.title("📍 Sites")
    with st.expander("➕ Add Site"):
        name = st.text_input("Site Name", key="site_name")
        company = st.text_input("Company", key="site_company")
        address = st.text_area("Address", key="site_address")
        if st.button("Save Site"):
            st.session_state.sites.append({"Site Name": name, "Company": company, "Address": address})
            save_data("sites")
            st.success("Saved site")
    render_table("All Sites", "sites")

elif tab == "Contacts":
    st.title("📇 Contacts")
    with st.expander("➕ Add Contact"):
        name = st.text_input("Name", key="contact_name")
        role = st.text_input("Role", key="contact_role")
        phone = st.text_input("Phone", key="contact_phone")
        email = st.text_input("Email", key="contact_email")
        if st.button("Save Contact"):
            st.session_state.contacts.append({
                "Name": name, "Role": role, "Phone": phone, "Email": email
            })
            save_data("contacts")
            st.success("Saved contact")
    render_table("All Contacts", "contacts")

elif tab == "Clients":
    st.title("🏢 Clients")
    with st.expander("➕ Add Client"):
        client = st.text_input("Client", key="client_name")
        industry = st.text_input("Industry", key="client_industry")
        abn = st.text_input("ABN", key="client_abn")
        if st.button("Save Client"):
            st.session_state.clients.append({
                "Client": client, "Industry": industry, "ABN": abn
            })
            save_data("clients")
            st.success("Saved client")
    render_table("All Clients", "clients")

elif tab == "Jobs":
    st.title("🛠️ Jobs")
    with st.expander("➕ Add Job"):
        number = st.text_input("Job #", key="job_number")
        client = st.text_input("Client", key="job_client")
        site = st.text_input("Site", key="job_site")
        status = st.selectbox("Status", ["Quote", "Scheduled", "In Progress", "Completed"], key="job_status")
        assigned = st.text_input("Assigned To", key="job_assigned")
        scope = st.text_area("Scope", key="job_scope")
        notes = st.text_area("Notes", key="job_notes")
        if st.button("Save Job"):
            st.session_state.jobs.append({
                "Job Number": number, "Client": client, "Site": site, "Status": status,
                "Assigned To": assigned, "Scope": scope, "Notes": notes
            })
            save_data("jobs")
            st.success("Saved job")
    render_table("All Jobs", "jobs")

elif tab == "Tasks":
    st.title("✅ Tasks")
    with st.expander("➕ Add Task"):
        task = st.text_input("Task", key="task_text")
        due = st.date_input("Due", key="task_due")
        who = st.text_input("Assigned To", key="task_who")
        if st.button("Save Task"):
            st.session_state.tasks.append({
                "Task": task, "Due": str(due), "Assigned To": who
            })
            save_data("tasks")
            st.success("Saved task")
    render_table("All Tasks", "tasks")

elif tab == "Vehicles":
    st.title("🚛 Vehicles")
    with st.expander("➕ Add Vehicle"):
        vehicle_id = st.text_input("Vehicle ID", key="vehicle_id")
        type_ = st.text_input("Type", key="vehicle_type")
        registration = st.text_input("Registration", key="vehicle_rego")
        notes = st.text_area("Notes", key="vehicle_notes")
        if st.button("Save Vehicle"):
            st.session_state.vehicles.append({
                "Vehicle ID": vehicle_id, "Type": type_, "Registration": registration, "Notes": notes
            })
            save_data("vehicles")
            st.success("Saved vehicle")
    render_table("All Vehicles", "vehicles")
