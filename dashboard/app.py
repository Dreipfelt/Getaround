import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page config
st.set_page_config(
    page_title="Getaround Delay Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 Getaround Delay Analysis Dashboard")
st.markdown("Delay analysis and minimum buffer simulation between rentals")

# ---------- Data loading ----------

@st.cache_data
def load_data():
    """Load and preprocess delay data."""
    delay_url = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
    df = pd.read_excel(delay_url)

    # Keep only ended rentals
    df_ended = df[df["state"] == "ended"].copy()
    df_ended["is_late_checkout"] = df_ended["delay_at_checkout_in_minutes"] > 0

    # Rentals with a previous rental
    df_following = df_ended[df_ended["time_delta_with_previous_rental_in_minutes"].notna()].copy()
    df_following["is_late_checkout"] = df_following["delay_at_checkout_in_minutes"] > 0
    df_following["is_problematic_for_next"] = (
        df_following["delay_at_checkout_in_minutes"]
        > df_following["time_delta_with_previous_rental_in_minutes"]
    )
    return df_ended, df_following


df_ended, df_following = load_data()


@st.cache_data
def load_buffer_sim():
    """Load precomputed buffer simulation from CSV."""
    try:
        return pd.read_csv("../data/buffer_simulation_summary.csv")
    except FileNotFoundError:
        return None


buffer_df = load_buffer_sim()

# ---------- Sidebar filters ----------

st.sidebar.header("🎛️ Interactive filters")
scope = st.sidebar.selectbox(
    "Scope (cars)",
    ["All", "Connect only", "Mobile only"],
    index=0
)

buffer_minutes = st.sidebar.slider(
    "Minimum buffer (minutes)",
    min_value=0,
    max_value=120,
    value=30,
    step=10
)

# ---------- Top KPIs ----------

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    late_rate = df_ended["is_late_checkout"].mean()
    st.metric(
        "Checkout delay rate",
        f"{late_rate:.1%}",
        delta=f"{df_ended['is_late_checkout'].sum():,} rentals"
    )

with col2:
    total_problematic = df_following["is_problematic_for_next"].sum()
    st.metric(
        "Current problematic cases",
        f"{total_problematic:,}",
        delta="impact the next driver"
    )

with col3:
    if buffer_df is not None:
        blocked = buffer_df.loc[
            buffer_df["buffer_minutes"] == buffer_minutes, "n_blocked_rentals"
        ].iloc[0]
        pct_blocked = blocked / len(df_following) * 100
        st.metric(
            "Blocked rentals",
            f"{blocked:,}",
            f"{pct_blocked:.1f}% of follow‑up rentals"
        )
    else:
        st.metric("Blocked rentals", "N/A")

with col4:
    if buffer_df is not None:
        solved = buffer_df.loc[
            buffer_df["buffer_minutes"] == buffer_minutes, "n_problematic_solved"
        ].iloc[0]
        current_prob = buffer_df["n_problematic_current"].iloc[0]
        solve_rate = solved / current_prob * 100 if current_prob > 0 else 0
        st.metric(
            "Issues solved",
            f"{solved:,}",
            f"{solve_rate:.1f}% resolved"
        )
    else:
        st.metric("Issues solved", "N/A")

# ---------- Row 1: Distributions ----------

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribution of checkout delays")
    fig1 = px.histogram(
        df_following,
        x="delay_at_checkout_in_minutes",
        nbins=50,
        title="Distribution of delays (minutes)",
        labels={"delay_at_checkout_in_minutes": "Delay at checkout (minutes)"}
    )
    fig1.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Scheduled time"
    )
    fig1.add_vline(
        x=buffer_minutes,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"Buffer {buffer_minutes} min"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📈 Delays by check‑in type")
    fig2 = px.box(
        df_following,
        x="checkin_type",
        y="delay_at_checkout_in_minutes",
        title="Boxplot of delays by check‑in type",
        color="checkin_type"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------- Row 2: Scope filter + buffer trade‑off ----------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔄 Rates by check‑in type")

    # Late checkout rate for all ended rentals
    late_rate_table = pd.crosstab(
        df_ended["checkin_type"],
        df_ended["is_late_checkout"],
        normalize="index"
    ) * 100

    # Apply scope filter for problematic cases
    if scope == "Connect only":
        df_filtered = df_following[df_following["checkin_type"].str.lower() == "connect"]
    elif scope == "Mobile only":
        df_filtered = df_following[df_following["checkin_type"].str.lower() == "mobile"]
    else:
        df_filtered = df_following

    prob_rate_table = pd.crosstab(
        df_filtered["checkin_type"],
        df_filtered["is_problematic_for_next"],
        normalize="index"
    ) * 100

    # Build a small summary table for plotting
    late_reset = late_rate_table.reset_index()
    late_reset = late_reset.rename(columns={True: "Late (%)"})
    prob_reset = prob_rate_table.reset_index()
    prob_reset = prob_reset.rename(columns={True: "Problematic for next (%)"})

    summary = pd.merge(
        late_reset[["checkin_type", "Late (%)"]],
        prob_reset[["checkin_type", "Problematic for next (%)"]],
        on="checkin_type",
        how="inner"
    )

    fig3 = px.bar(
        summary.melt(id_vars="checkin_type", value_vars=["Late (%)", "Problematic for next (%)"]),
        x="checkin_type",
        y="value",
        color="variable",
        barmode="group",
        title="Late vs problematic rate by check‑in type (%)",
        labels={"value": "Rate (%)", "checkin_type": "Check‑in type", "variable": "Metric"}
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("⚖️ Buffer trade‑off")

    if buffer_df is not None:
        fig4 = px.line(
            buffer_df,
            x="buffer_minutes",
            y=["n_blocked_rentals", "n_problematic_solved"],
            title="Blocked rentals vs solved issues",
            labels={"value": "Number of cases", "variable": "Metric"}
        )
        fig4.add_vline(
            x=buffer_minutes,
            line_dash="dash",
            line_color="orange"
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Summary for selected buffer
        current_row = buffer_df[buffer_df["buffer_minutes"] == buffer_minutes].iloc[0]
        st.dataframe(
            {
                "Metric": [
                    "Buffer (min)",
                    "Blocked rentals",
                    "Current problematic cases",
                    "Solved cases",
                    "Solved rate"
                ],
                "Value": [
                    f"{int(current_row['buffer_minutes'])} min",
                    f"{current_row['n_blocked_rentals']:,}",
                    f"{current_row['n_problematic_current']:,}",
                    f"{current_row['n_problematic_solved']:,}",
                    f"{current_row['n_problematic_solved'] / current_row['n_problematic_current'] * 100:.1f}%"
                    if current_row["n_problematic_current"] > 0 else "0.0%"
                ]
            },
            use_container_width=True
        )
    else:
        st.info("💡 Run the EDA notebook to generate data/buffer_simulation_summary.csv")

# ---------- Footer ----------

st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666;'>
  <p><strong>🎯 Getaround Dashboard – CDSD Certification</strong></p>
  <p>Simulate the impact of a minimum buffer between rentals.</p>
</div>
""",
    unsafe_allow_html=True,
)
