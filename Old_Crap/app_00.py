import pandas as pd

# =========================
# LOAD DATA (CORRECT SHEET)
# =========================
DATA_PATH = "get_around_delay_analysis.xlsx"

df = pd.read_excel(DATA_PATH, sheet_name="rentals_data")

# =========================
# QUICK SANITY CHECK
# =========================
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)

# =========================
# CORE CLEANING
# =========================
# Drop rows where delay is missing (no checkout info)
df = df.dropna(subset=["delay_at_checkout_in_minutes"])

# Ensure numeric
df["delay_at_checkout_in_minutes"] = df["delay_at_checkout_in_minutes"].astype(int)

# Flags
df["is_late"] = df["delay_at_checkout_in_minutes"] > 0
df["is_connect"] = df["checkin_type"] == "connect"

# =========================
# CORE METRICS
# =========================
total_rentals = len(df)
late_rentals = df["is_late"].sum()
late_ratio = late_rentals / total_rentals

print("\n=== CORE METRICS ===")
print(f"Total rentals: {total_rentals}")
print(f"Late rentals: {late_rentals}")
print(f"Late ratio: {late_ratio:.2%}")

# Delay distribution (late rentals only)
delay_stats = df.loc[df["is_late"], "delay_at_checkout_in_minutes"].describe(
    percentiles=[0.5, 0.75, 0.9, 0.95]
)

print("\n=== DELAY STATS (LATE ONLY) ===")
print(delay_stats)

# =========================
# SIMULATE MINIMUM DELAYS
# =========================
THRESHOLDS = [0, 15, 30, 45, 60]

results = []

for threshold in THRESHOLDS:
    impacted = df[
        (df["delay_at_checkout_in_minutes"] > 0) &
        (df["time_delta_with_previous_rental_in_minutes"] < threshold)
    ]

    results.append({
        "threshold_min": threshold,
        "impacted_rentals": len(impacted),
        "impacted_ratio": len(impacted) / total_rentals
    })

impact_df = pd.DataFrame(results)

print("\n=== THRESHOLD IMPACT ===")
print(impact_df)
