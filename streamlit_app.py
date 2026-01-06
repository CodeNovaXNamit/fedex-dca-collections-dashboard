import streamlit as st
import pandas as pd
import requests

API_BASE = "http://127.0.0.1:5000/api"

st.set_page_config(
    page_title="FedEx DCA Collections Dashboard",
    layout="wide"
)

st.title("📦 FedEx DCA — Collections Dashboard with AI Prioritizer")

# -------------------------
# Fetch data
# -------------------------
@st.cache_data(ttl=10)
def load_accounts():
    response = requests.get(f"{API_BASE}/accounts")
    return pd.DataFrame(response.json())

df = load_accounts()

# -------------------------
# KPIs
# -------------------------
total_amount = df["amount_due"].sum()
open_accounts = df[df["status"] == "open"].shape[0]
avg_days = df["days_overdue"].mean()
high_priority = df[df["predicted_score"] > 0.7].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Overdue Amount", f"{total_amount:,.2f}")
col2.metric("📂 Open Accounts", open_accounts)
col3.metric("⏱ Avg Days Overdue", f"{avg_days:.1f}")
col4.metric("🔥 High Priority Accounts", high_priority)

st.divider()

# -------------------------
# Accounts Table
# -------------------------
st.subheader("📋 Overdue Accounts (Sorted by AI Priority)")

df_sorted = df.sort_values(by="predicted_score", ascending=False)

st.dataframe(
    df_sorted[[
        "customer_name",
        "amount_due",
        "days_overdue",
        "predicted_score",
        "agency_assigned",
        "status"
    ]],
    use_container_width=True
)

st.divider()

# -------------------------
# Assign account
# -------------------------
st.subheader("🏷 Assign Account to Agency")

account_ids = df_sorted["id"].tolist()

selected_id = st.selectbox("Select Account ID", account_ids)
selected_agency = st.selectbox(
    "Select Agency",
    ["AgencyX", "AgencyY", "AgencyZ"]
)

if st.button("Assign"):
    requests.put(
        f"{API_BASE}/accounts/{selected_id}/assign",
        json={"agency": selected_agency}
    )
    st.success("Account assigned successfully")
    st.cache_data.clear()

st.divider()

# -------------------------
# Aging Bucket Chart
# -------------------------
st.subheader("📊 Aging Buckets")

bins = [0, 30, 60, 90, 1000]
labels = ["0–30", "31–60", "61–90", "90+"]

df["aging_bucket"] = pd.cut(df["days_overdue"], bins=bins, labels=labels)

aging_counts = df["aging_bucket"].value_counts().sort_index()

st.bar_chart(aging_counts)
