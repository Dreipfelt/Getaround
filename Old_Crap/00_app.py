import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="GetAround – Late Checkout Analysis", layout="wide")

DATA_PATH = "get_around_delay_analysis.xlsx"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel(DATA_PATH, sheet_name="rentals_data")
    df = df.dropna(subset=["delay_at_checkout_in_minutes"])
    df["delay_at_checkout_in_minutes"] = df["delay_at_checkout_in_minutes"].astype(int)
    df["is_late"] = df["delay_at_checkout_in_minutes"] > 0
    df["is_connect"] = df["checkin_type"] == "connect"
    return df

df = load_data()

total_rentals = len(df)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Parameters")

threshold = st.sidebar.slider(
    "Minimum delay between rentals (minutes)",
    min_value=0,
    max_value=60,
    step=15,
    value=45
)

connect_only = st.sidebar.checkbox("Apply to Connect cars only", value=True)

# =========================
# FILTER DATA
# =========================
analysis_df = df.copy()
if connect_only:
    analysis_df = analysis_df[analysis_df["is_connect"]]

impacted = analysis_df[
    (analysis_df["delay_at_checkout_in_minutes"] > 0) &
    (analysis_df["time_delta_with_previous_rental_in_minutes"] < threshold)
]

# =========================
# KPIs
# =========================
st.title("🚗 GetAround – Minimum Delay Impact Analysis")

col1, col2, col3 = st.columns(3)

col1.metric("Total rentals", len(analysis_df))
col2.metric("Impacted rentals", len(impacted))
col3.metric(
    "Impacted ratio",
    f"{len(impacted) / total_rentals:.2%}"
)

# =========================
# DISTRIBUTION
# =========================
st.subheader("Delay distribution (late rentals only)")

st.bar_chart(
    analysis_df.loc[
        analysis_df["is_late"],
        "delay_at_checkout_in_minutes"
    ].clip(upper=500)
)