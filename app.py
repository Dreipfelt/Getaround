import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Getaround Delay Analysis",
    layout="wide"
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    url = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
    return pd.read_excel(url, engine="openpyxl")  # force openpyxl

df = load_data()

# -----------------------------
# Title & global info
# -----------------------------
st.title("🚗 Getaround — Late Checkout Analysis")
st.write("Nombre total de locations :", len(df))

# -----------------------------
# User controls
# -----------------------------
threshold = st.slider(
    "Seuil de retard (minutes)",
    min_value=0,
    max_value=180,
    value=30
)

# Multiselect scope
checkin_types = sorted(df["checkin_type"].dropna().unique().tolist())
scope = st.multiselect("Scope", options=checkin_types, default=checkin_types)

# -----------------------------
# Filter dataframe
# -----------------------------
if not scope:
    df_scope = df.copy()
else:
    df_scope = df[df["checkin_type"].isin(scope)].copy()

# -----------------------------
# Feature engineering
# -----------------------------
df_scope["late"] = df_scope["delay_at_checkout_in_minutes"] > threshold
df_scope["delay_capped"] = df_scope["delay_at_checkout_in_minutes"].clip(upper=180)

# -----------------------------
# KPIs
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    st.metric("Locations analysées", len(df_scope))
with col2:
    late_rate = df_scope["late"].mean() * 100
    st.metric("Locations en retard (%)", f"{late_rate:.2f}%")

# -----------------------------
# Histogramme retards
# -----------------------------
st.subheader("Distribution des retards")
fig_hist = px.histogram(
    df_scope,
    x="delay_at_checkout_in_minutes",
    nbins=50,
    labels={"delay_at_checkout_in_minutes": "Retard au checkout (minutes)"}
)
st.plotly_chart(fig_hist, use_container_width=True)

# -----------------------------
# Retard moyen vs seuil
# -----------------------------
st.subheader("Retard moyen vs seuil choisi")
thresholds = list(range(0, 181, 10))
mean_delays = [
    df_scope[df_scope["delay_at_checkout_in_minutes"] > t]["delay_at_checkout_in_minutes"].mean()
    if len(df_scope[df_scope["delay_at_checkout_in_minutes"] > t]) > 0 else 0
    for t in thresholds
]

fig_mean = px.line(
    x=thresholds,
    y=mean_delays,
    labels={"x": "Seuil (minutes)", "y": "Retard moyen (minutes)"},
    markers=True
)
st.plotly_chart(fig_mean, use_container_width=True)

# -----------------------------
# Business impact auto
# -----------------------------
affected = df_scope["late"].sum()
late_pct = (affected / len(df_scope)) * 100 if len(df_scope) > 0 else 0

st.subheader("Impact du seuil choisi")
st.write(
    f"👉 Sur {len(df_scope)} locations analysées, **{affected} ({late_pct:.1f}%)** dépassent le seuil de **{threshold} minutes**."
)

if late_pct > 20:
    st.info("⚠️ Une proportion importante de locations est en retard. À surveiller pour optimiser les opérations.")
elif late_pct > 5:
    st.success("✅ La plupart des locations respectent le délai, mais quelques améliorations sont possibles.")
else:
    st.success("🎉 Très peu de retards. L'opération semble bien gérée.")
