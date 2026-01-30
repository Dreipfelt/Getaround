
st.set_page_config(page_title="Getaround Analysis", layout="wide")

@st.cache_data
def load_data():
    rentals = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx")
    pricing = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")
    pricing = pricing.drop(columns=['Unnamed: 0'], errors='ignore')
    return rentals, pricing

rentals_df, pricing_df = load_data()

# Nettoyage
rentals_df['delay_at_checkout_in_minutes'] = rentals_df['delay_at_checkout_in_minutes'].fillna(0)
rentals_df['time_delta_with_previous_rental_in_minutes'] = rentals_df['time_delta_with_previous_rental_in_minutes'].fillna(np.inf)

st.title("🚗 Getaround - Analyse des Retards")

# Métriques principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Locations totales", f"{len(rentals_df):,}")

with col2:
    late_rate = (rentals_df['delay_at_checkout_in_minutes'] > 0).mean() * 100
    st.metric("Taux de retard", f"{late_rate:.1f}%")

with col3:
    problematic = rentals_df[
        (rentals_df['delay_at_checkout_in_minutes'] > 0) &
        (rentals_df['delay_at_checkout_in_minutes'] >= rentals_df['time_delta_with_previous_rental_in_minutes'])
    ]
    st.metric("Cas problématiques", f"{len(problematic):,}")

# Analyse par seuil
st.header("📈 Impact du Seuil Minimum")
threshold = st.slider("Seuil (heures)", 0.5, 6.0, 2.0, 0.5)
scope = st.selectbox("Scope", ["all", "connect"])

def analyze_threshold(threshold_h, scope='all'):
    minutes = threshold_h * 60
    df = rentals_df[rentals_df['time_delta_with_previous_rental_in_minutes'] != np.inf]
    if scope == 'connect':
        df = df[df['checkin_type'] == 'connect']
    affected = df[df['time_delta_with_previous_rental_in_minutes'] <= minutes]
    return len(affected)

affected_count = analyze_threshold(threshold, scope)
st.write(f"**Locations bloquées** : {affected_count:,}")

# Visualisation
fig, ax = plt.subplots()
sns.histplot(rentals_df['delay_at_checkout_in_minutes'].clip(upper=300), bins=50, ax=ax)
st.pyplot(fig)
