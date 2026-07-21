import streamlit as st
import plotly.express as px
import pandas as pd

from monday_client import load_all_data
from data_cleaner import clean_dataframe
from ai_agent import ask_ai


st.set_page_config(
    page_title="Monday Business Intelligence Agent",
    page_icon="🤖",
    layout="wide"
)
col1, col2 = st.columns([8,2])

with col2:
    st.success("🟢 Live")
st.markdown("""
<style>

/* Main App */
.stApp{
    background: linear-gradient(180deg,#071A2C 0%,#0B2239 100%);
}

/* Main container */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#061421;
}

/* KPI Cards */
div[data-testid="metric-container"]{
    background: linear-gradient(135deg,#12395A,#0D2C47);
    border:1px solid #1F4E79;
    border-radius:18px;
    padding:18px;
    box-shadow:0 6px 18px rgba(0,0,0,0.35);
}

/* Buttons */
.stButton>button{
    background:#00B4D8;
    color:white;
    border-radius:12px;
    border:none;
    font-weight:bold;
}

.stButton>button:hover{
    background:#0096C7;
}

/* Chat input */
.stChatInput{
    border-radius:12px;
}

/* Charts */
.js-plotly-plot{
    border-radius:16px;
}

/* Headers */
h1,h2,h3{
    color:#F8FAFC;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# LOAD DATA
# -----------------------------

if "deals" not in st.session_state:

    deals, work = load_all_data()

    st.session_state.deals = clean_dataframe(deals)
    st.session_state.work = clean_dataframe(work)

if "messages" not in st.session_state:
    st.session_state.messages = []

deals = st.session_state.deals
work = st.session_state.work

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.title("🤖 Monday BI Agent")

    st.success("Connected to Monday.com")

    if st.button("🔄 Refresh Data"):
        deals, work = load_all_data()
        st.session_state.deals = clean_dataframe(deals)
        st.session_state.work = clean_dataframe(work)
        st.rerun()

    st.divider()

    st.subheader("Try asking")

    st.write("• How many deals do we have?")
    st.write("• How is the pipeline looking?")
    st.write("• Which sectors are present?")
    st.write("• Prepare a leadership update")
    st.write("• Total billed value")
    st.write("• Which sector has highest activity?")

# -----------------------------
# HEADER
# -----------------------------

st.title("📊 Monday Business Intelligence Dashboard")

st.caption(
    "AI-powered Business Intelligence Agent for Deals and Work Orders"
)

# -----------------------------
# KPI CARDS
# -----------------------------


total_deals = len(deals)

total_work_orders = len(work)

sector_count = 0

if "Sector" in work.columns:
    sector_count = work["Sector"].dropna().nunique()

elif "Sector/Service" in deals.columns:
    sector_count = deals["Sector/Service"].dropna().nunique()

missing_values = (
    deals.isna().sum().sum() +
    work.isna().sum().sum()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Deals", total_deals)

c2.metric("Work Orders", total_work_orders)

c3.metric("Sectors", sector_count)

c4.metric("Missing Values", int(missing_values))

st.divider()

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Deals Preview")
    st.dataframe(
        deals.head(10),
        use_container_width=True,
        height=300
    )

with col2:
    st.subheader("🛠 Work Orders Preview")
    st.dataframe(
        work.head(10),
        use_container_width=True,
        height=300
    )

# -----------------------------
# CHARTS
# -----------------------------

st.divider()

left, right = st.columns(2)

# -----------------------------
# Deal Stage Chart
# -----------------------------
with left:

    st.subheader("📈 Deal Stage Distribution")

    if "Deal Stage" in deals.columns:

        deal_stage = (
            deals["Deal Stage"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        deal_stage.columns = ["Deal Stage", "Count"]

        fig = px.pie(
            deal_stage,
            values="Count",
            names="Deal Stage",
            hole=0.45,
            title="Deal Pipeline"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            legend_title="Deal Stage"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Deal Stage column not found.")

# -----------------------------
# Sector Chart
# -----------------------------
with right:

    st.subheader("🏭 Work Orders by Sector")

    if "Sector" in work.columns:

        sector_df = (
            work["Sector"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        sector_df.columns = ["Sector", "Count"]

        fig = px.bar(
            sector_df,
            x="Sector",
            y="Count",
            text="Count",
            title="Sector Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            xaxis_title="Sector",
            yaxis_title="Work Orders"
        )

        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Sector column not found.")
# -----------------------------
# CHATBOT
# -----------------------------

st.subheader("💬 Ask the AI")

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a business question...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Analyzing business data..."):

        answer = ask_ai(
            question,
            deals,
            work
        )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )