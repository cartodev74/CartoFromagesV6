import streamlit as st
import plotly.express as px #affichage des graphiques
import folium #gestion affichage
import geopandas
from sqlalchemy import create_engine

from utils.recherche import recherche_vue
from utils.format import separateur_millier

import os
import pickle



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

# filtre et récupération dans le dataframe de la ligne avec le nom du fromage choisi
filtered_data = df[df['nom']==selected_fromage]

# dans la ligne, on récupère le numéro SIQO id_inao
numero_SIQO = filtered_data['id_inao']

# dans la cellule choisie, on prend la valeur
SIQO_id = numero_SIQO.values[0]

fichier_photo = "0" + str(SIQO_id) + ".jpg"





## --- Texte ---
st.subheader("Texte")
st.text(rf"Le fromage choisi a le numéro SIQO* {SIQO_id} de l'INAO ")
st.text(rf"*SIQO = Signe officiel d'Identification de la Qualité et de l'Origine")

## calcul surface
vue_selectionnee = recherche_vue(int(SIQO_id))

df_surface_SIQO = conn.query(f"SELECT st_area(st_union(wkb_geometry))/1000000 as surf_km from {vue_selectionnee}")
surface_SIQO_selectionne = df_surface_SIQO.values[0,0]

st.text(f"La surface totale de cette SIQO : {separateur_millier(surface_SIQO_selectionne)} km²")

st.image(f"https://fel.alwaysdata.net/images/{fichier_photo}", caption=None, width=400)

## --- Graph ---

st.subheader("Graphique")



df_effectif_dept_SIQO = conn.query(f"""select dept.nom_dept_min, mv.code_dept,count(mv.id_insee)
from {vue_selectionnee} as mv,departement_geofla_2010 as dept
where mv.code_dept = dept.code_dept
group by mv.code_dept, dept.nom_dept_min""")

df_effectif_dept_SIQO_sorted = df_effectif_dept_SIQO.sort_values(by='count',  ascending=False)


df_liste_categorie = df_effectif_dept_SIQO_sorted[['nom_dept_min']]

liste_categorie =[]
for i in df_liste_categorie.index:
    liste_categorie.append (df_liste_categorie["nom_dept_min"][i])

df_liste_effectif = df_effectif_dept_SIQO_sorted[['count']]

liste_effectif = []
for i in df_liste_effectif.index:
    liste_effectif.append(df_liste_effectif["count"][i])

fig = px.bar(liste_categorie, y = liste_effectif, x=liste_categorie, color= liste_categorie,
             title="Nombres de communes labelisées par département")

st.plotly_chart(fig,width=400)



## --- Map ---
st.subheader("Carte interactive")




# -- Sources ---
st.subheader("Crédits")
st.markdown("""
<p>
<em> Contribution(s) : </em>
<ul>
<small>
    <li> Merci à Pascaline pour sa relecture attentive et le classement des SIQO </li>
</small>
</ul>
</p>
<p>
<em> Sources pour les données : </em>
<ul>
<small>
    <li> Fond carte OpenSreetMap © OSM Contributors - IGN ADMIN EXPRESS Départements PE </li>
    <li> Données INAO SIQO Fromages 2025 - Licence ouverte ETALAB </li>
</small>
</ul>
</p>
<p> 
<em>  Sources pour la programmation : </em>
<ul>
<small>
    <li> data-geek-lab / real time dashboard - MIT License - Copyright (c) 2025 Data-Geek-is-my-Name </li>
    <li> How to Build choropleth map in Python | Streamlit Tutorial #3 | Data Driven Maps With Python Folium - SCIENCE AND SCIENCE ONLY - Youtube</li>
</ul>
</small>
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
