import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données
url = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'
df = pd.read_excel(url)

st.title("Analyse des retards de restitution Getaround")

st.header("Aperçu du dataset")
st.write(df.head())

st.subheader("Statistiques descriptives")
st.write(df.describe())

st.subheader("Répartition des types de check-in")
fig_checkin = px.bar(df['checkin_type'].value_counts().reset_index(),
                     x='index', y='checkin_type',
                     labels={'index': 'Type de check-in', 'checkin_type': 'Nombre'})
st.plotly_chart(fig_checkin, use_container_width=True)

st.subheader("Répartition des états de location")
fig_state = px.bar(df['state'].value_counts().reset_index(),
                   x='index', y='state',
                   labels={'index': 'État', 'state': 'Nombre'})
st.plotly_chart(fig_state, use_container_width=True)

st.subheader("Distribution des retards à la restitution")
fig_delay = px.histogram(df, x='delay_at_checkout_in_minutes',
                         nbins=50,
                         labels={'delay_at_checkout_in_minutes': 'Retard (minutes)'},
                         title='Histogramme des retards à la restitution')
st.plotly_chart(fig_delay, use_container_width=True)

st.subheader("Retard moyen par type de check-in")
mean_delay_checkin = df.groupby('checkin_type')['delay_at_checkout_in_minutes'].mean().reset_index()
fig_mean_checkin = px.bar(mean_delay_checkin, x='checkin_type', y='delay_at_checkout_in_minutes',
                         labels={'delay_at_checkout_in_minutes': 'Retard moyen (min)', 'checkin_type': 'Type de check-in'})
st.plotly_chart(fig_mean_checkin, use_container_width=True)

st.subheader("Retard moyen selon l'état de la location")
mean_delay_state = df.groupby('state')['delay_at_checkout_in_minutes'].mean().reset_index()
fig_mean_state = px.bar(mean_delay_state, x='state', y='delay_at_checkout_in_minutes',
                        labels={'delay_at_checkout_in_minutes': 'Retard moyen (min)', 'state': 'État'})
st.plotly_chart(fig_mean_state, use_container_width=True)