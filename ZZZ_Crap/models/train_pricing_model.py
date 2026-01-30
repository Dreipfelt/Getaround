import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Chargement et préparation des données
pricing_df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")
pricing_df = pricing_df.drop(columns=['Unnamed: 0'], errors='ignore')

# Entraînement du modèle
X = pricing_df.drop('rental_price_per_day', axis=1)
y = pricing_df['rental_price_per_day']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sauvegarde du modèle
joblib.dump(model, 'models/pricing_model.pkl')