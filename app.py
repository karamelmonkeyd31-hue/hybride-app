import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date, datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="HYBRIDE ELITE", layout="centered", page_icon="⚡")

# --- INITIALISATION DES DONNÉES ---
if 'repas_data' not in st.session_state:
    st.session_state.repas_data = {
        'Petit-déjeuner': {'cal': 0, 'prot': 0},
        'Déjeuner': {'cal': 0, 'prot': 0},
        'Collation': {'cal': 0, 'prot': 0},
        'Dîner': {'cal': 0, 'prot': 0}
    }

# Simulation de données Strava (Distances et Allures sur 7 jours)
data_strava = {
    'Jour': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
    'Distance': [5.2, 0, 8.5, 0, 6.1, 12.0, 0],
    'Allure': [5.45, 0, 5.30, 0, 5.50, 5.20, 0] # en minutes par km
}
df = pd.DataFrame(data_strava)

# --- MENU ---
st.sidebar.title("⚡ HYBRIDE")
menu = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🥗 Nutrition", "🏃 Running & Strava", "⏳ Jeûne", "⚙️ Profil"])

# --- PAGE RUNNING (DASHBOARD COMPLET) ---
if menu == "🏃 Running & Strava":
    st.title("🏃 Dashboard Running")
    
    # Statistiques Globales
    col1, col2, col3 = st.columns(3)
    total_km = df['Distance'].sum()
    allure_moy = df[df['Allure'] > 0]['Allure'].mean()
    
    col1.metric("Distance Totale", f"{total_km} km", "+2.4km")
    col2.metric("Allure Moy.", f"{int(allure_moy)}' {int((allure_moy%1)*60)}''/km")
    col3.metric("Séances", "4 cette semaine")

    # GRAPHIQUE 1 : Volume de Distance (Bar Chart)
    fig_dist = go.Figure()
    fig_dist.add_trace(go.Bar(
        x=df['Jour'], y=df['Distance'],
        marker_color='#1E90FF',
        name='Kilomètres'
    ))
    fig_dist.update_layout(title="Volume Hebdomadaire (km)", template="plotly_white", height=300)
    st.plotly_chart(fig_dist, use_container_width=True)

    # GRAPHIQUE 2 : Évolution Allure (Line Chart)
    # On filtre les jours sans course pour le graphique de ligne
    df_filtered = df[df['Allure'] > 0]
    fig_pace = go.Figure()
    fig_pace.add_trace(go.Scatter(
        x=df_filtered['Jour'], y=df_filtered['Allure'],
        mode='lines+markers', line=dict(color='#FF4B4B', width=3),
        name='Allure'
    ))
    fig_pace.update_layout(title="Analyse de l'Allure (min/km)", yaxis=dict(autorange="reversed"), template="plotly_white", height=300)
    st.plotly_chart(fig_pace, use_container_width=True)

    # COACH IA
    st.info("🤖 **Coach IA :** Ta sortie longue de samedi (12km) était excellente. Pour ta prise de masse, n'oublie pas de doubler ta portion de glucides ce soir pour recharger le glycogène.")

# --- PAGE NUTRITION (TON YAZIO) ---
elif menu == "🥗 Nutrition":
    st.title("🥗 Nutrition & Masse")
    # (On garde ici le code de la jauge que tu as déjà)
    cible_cal = st.session_state.get('cible_cal', 2500)
    total_cal = sum(item['cal'] for item in st.session_state.repas_data.values())
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = total_cal,
        gauge = {'axis': {'range': [None, cible_cal]}, 'bar': {'color': "#1E90FF"}},
        title = {'text': "Calories"}
    ))
    st.plotly_chart(fig_gauge)

    # Gestion des 4 repas
    for repas in st.session_state.repas_data.keys():
        with st.expander(f"➕ {repas}"):
            c1, c2 = st.columns(2)
            cal = c1.number_input("Kcal", key=f"c_{repas}", step=50)
            prot = c2.number_input("Prot (g)", key=f"p_{repas}", step=5)
            if st.button(f"Enregistrer {repas}"):
                st.session_state.repas_data[repas]['cal'] += cal
                st.session_state.repas_data[repas]['prot'] += prot
                st.rerun()

# --- AUTRES PAGES ---
else:
    st.write("Navigue vers Running ou Nutrition pour voir tes graphes.")
