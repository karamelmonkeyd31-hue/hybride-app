import streamlit as st
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="HYBRIDE", layout="centered", page_icon="⚡")

# --- INITIALISATION DES DONNÉES ---
if 'conso' not in st.session_state:
    st.session_state.conso = 0
if 'prot_consommees' not in st.session_state:
    st.session_state.prot_consommees = 0

# --- CALCULATEUR ÉNERGÉTIQUE (Venesson / Mifflin-St Jeor) ---
def calculer_besoins(sexe, poids, taille, age, activite, objectif):
    s = 5 if sexe == "Homme" else -161
    mb = (10 * poids) + (6.25 * taille) - (5 * age) + s
    f = {"Sédentaire": 1.2, "Léger": 1.375, "Modéré": 1.55, "Intense": 1.725, "Extrême": 1.9}
    tdee = mb * f[activite]
    
    if objectif == "Prise de masse":
        cible = tdee + 300
    elif objectif == "Perte de gras":
        cible = tdee - 500
    else:
        cible = tdee
    return int(mb), int(cible)

# --- NAVIGATION ---
st.sidebar.title("⚡ HYBRIDE")
menu = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🥗 Nutrition & Masse", "⏳ Jeûne & Ramadan", "⚙️ Mon Profil"])

# --- PAGE PROFIL ---
if menu == "⚙️ Mon Profil":
    st.header("⚙️ Ton Profil")
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
    st.session_state.poids_actuel = poids
    st.success(f"Cible Journalière : **{cible} kcal**")

# --- PAGE NUTRITION ---
elif menu == "🥗 Nutrition & Masse":
    st.header("🥗 Suivi Nutrition")
    
    # Récupération des objectifs
    poids = st.session_state.get('poids_actuel', 75)
    cible_cal = st.session_state.get('cible_cal', 2500)
    cible_prot = int(poids * 2) # Formule : 2g par kg de poids
    
    conso_cal = st.session_state.conso
    conso_prot = st.session_state.prot_consommees
    
    # JAUGE CALORIES
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = conso_cal,
        gauge = {
            'axis': {'range': [None, cible_cal]},
            'bar': {'color': "#1E90FF"},
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': cible_cal}
        },
        title = {'text': "Calories Journalières"}
    ))
    st.plotly_chart(fig, use_container_width=True)

    # MACROS
    c1, c2 = st.columns(2)
    c1.metric("Protéines", f"{conso_prot}g / {cible_prot}g")
    c2.metric("Reste à manger", f"{cible_cal - conso_cal} kcal")

    # AJOUT REPAS
    with st.expander("➕ Ajouter un repas"):
        cal = st.number_input("Calories", value=0)
        p = st.number_input("Protéines (g)", value=0)
        if st.button("Enregistrer"):
            st.session_state.conso += cal
            st.session_state.prot_consommees += p
            st.rerun()

# --- PAGE JEÛNE & RAMADAN ---
elif menu == "⏳ Jeûne & Ramadan":
    st.header("⏳ Jeûne")
    mode = st.toggle("Mode Ramadan 🌙")
    
    if mode:
        st.subheader("Planning Ramadan")
        st.info("Imsak (Fajr) : 06:15 | Iftar (Maghrib) : 18:45")
    else:
        niv = st.select_slider("Protocole", ["Poussin (14:10)", "Loup (16:8)", "Guerrier (20:4)"])
        st.write(f"Mode actuel : **{niv}**")

else:
    st.title("🏠 Dashboard")
    st.write("Bienvenue sur Hybride. Utilise le menu pour naviguer.")
