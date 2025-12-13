import streamlit as st
import pandas as pd
import pandas._libs

# Tenter de charger les données depuis l'URL
url = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'

try:
    df = pd.read_excel(url)
    # Afficher un aperçu des données pour vérifier
    st.write("Aperçu des données chargées :")
    st.write(df.head())  # Affiche les premières lignes du dataframe
except Exception as e:
    st.write(f"Erreur lors du chargement des données : {e}")

