import streamlit as st #création de la page web
import sqlalchemy #récupération de sqlalchemy


import os

CUR_DIR = os.path.dirname(__file__)

# Le st.connection de STREAMLIT gère la récupération
#  - des secrets,
#  - la configuration,
#  - la mise en cache des requêtes SQL (ici moins de 10 min)
#  - les retentatives
conn = st.connection("postgresql", type="sql", ttl="10m")

# --- Streamlit Config ---
st.set_page_config(page_title="Fromage", layout="wide")
st.title("📊 🧀CartoFromages v6 - Real-Time Live Fromage")

# Perform query.
df = conn.query('SELECT nom,id_inao FROM fromage;')



## --- Select Box ---
st.subheader("Menu déroulant")

sorted_df = df.sort_values(by='nom')

# récupération du département sélectionné
selected_fromage = st.selectbox(label='Choisissez une SIQO fromage', options= sorted_df['nom'],index=0)

## --- Texte ---
st.subheader("Texte")

## --- Graph ---
st.subheader("Graphique")

## --- Map ---
st.subheader("Carte interactive")




# -- Sources ---
st.subheader("Crédits")
st.markdown("""
<p>
<em> Sources pour les données : </em>
<ul>
<li> Fond carte OpenSreetMap © OSM Contributors - IGN ADMIN EXPRESS Départements PE </li>
<li> Données INAO SIQO Fromages 2025 - Licence ouverte ETALAB </li>
</ul>
</p>
<p> 
<em>  Sources pour la programmation : </em>
<ul>
<li> data-geek-lab / real time dashboard - MIT License - Copyright (c) 2025 Data-Geek-is-my-Name </li>
<li> How to Build choropleth map in Python | Streamlit Tutorial #3 | Data Driven Maps With Python Folium - SCIENCE AND SCIENCE ONLY - Youtube</li>
</ul>
</p>

<br>

<p>
    <img src="https://www.cartodev.net/image/20240824_NIA_FR.png"> </img>
    <br>
    Réalisé sans intelligence articielle
    <br>
    <small> source logo © 2023 by Martine Peters (license creative commons BY-NC-SA 4.0) </small>
</p>
""", unsafe_allow_html=True)
