import streamlit as st
import plotly.graph_objects as go
import datetime

# --- CONFIGURATION DE L'APPARENCE ---
st.set_page_config(page_title="HYBRIDE", layout="centered", page_icon="⚡")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #1E90FF; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- CALCULATEUR ÉNERGÉTIQUE (Formule Venesson / Mifflin-St Jeor) ---
def calculer_besoins(sexe, poids, taille, age, activite, objectif):
    # s = +5 pour les hommes, -161 pour les femmes
    s = 5 if sexe == "Homme" else -161
    mb = (10 * poids) + (6.25 * taille) - (5 * age) + s
    
    # Facteurs d'activité
    facteurs = {"Sédentaire": 1.2, "Léger": 1.375, "Modéré": 1.55, "Intense": 1.725, "Extrême": 1.9}
    tdee = mb * facteurs[activite]
    
    # Ajustement objectif (Prise de masse / Maintien / Sèche)
    if objectif == "Prise de masse":
        cible = tdee + 300
    elif objectif == "Perte de gras":
        cible = tdee - 500
    else:
        cible = tdee
    return int(mb), int(cible)

# --- INITIALISATION DES DONNÉES ---
if 'conso' not in st.session_state:
    st.session_state.conso = 0
if 'prot' not in st.session_state:
    st.session_state.prot = 0

# --- BARRE LATÉRALE ---
st.sidebar.title("⚡ HYBRIDE")
menu = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🥗 Nutrition & Masse", "⏳ Jeûne & Ramadan", "🏃 Running", "⚙️ Mon Profil"])

# --- PAGE PROFIL ---
if menu == "⚙️ Mon Profil":
    st.header("⚙️ Configuration de l'Athlète")
    col1, col2 = st.columns(2)
    with col1:
        sexe = st.radio("Sexe", ["Homme", "Femme"])
        poids = st.number_input("Poids (kg)", value=75)
        taille = st.number_input("Taille (cm)", value=175)
    with col2:
        age = st.number_input("Âge", value=25)
        activite = st.selectbox("Niveau d'activité", ["Sédentaire", "Léger", "Modéré", "Intense", "Extrême"])
        obj = st.selectbox("Objectif", ["Maintien", "Prise de masse", "Perte de gras"])
    
    mb, cible = calculer_besoins(sexe, poids, taille, age, activite, obj)
    st.session_state.cible_cal = cible
    st.success(f"Métabolisme de Base : **{mb} kcal** | Cible Journalière : **{cible} kcal**")

# --- PAGE NUTRITION ---
elif menu == "🥗 Nutrition & Masse":
    st.header("🥗 Suivi Nutrition")
    cible = st.session_state.get('cible_cal', 2500)
    conso = st.session_state.conso
    
    # JAUGE STYLE YAZIO
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = conso,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, cible]},
            'bar': {'color': "#1E90FF"},
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': cible}
        }
    ))
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

    # MACROS
    c1, c2, c3 = st.columns(3)
    c1.metric("Protéines", f"{st.session_state.prot}
