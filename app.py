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

# Perform query.
df = conn.query('SELECT nom,id_inao FROM fromage;')


## --- Tableau ---
st.text(df)


## --- Select Box ---
st.subheader("Menu déroulant")

sorted_df = df.sort_values(by='nom')

# récupération du département sélectionné
selected_fromage = st.selectbox(label='Choisissez une SIQO fromage', options= sorted_df['nom'],index=0)






# Print results.
##for row in df.itertuples():
##    st.write(f" nom : {row : nom} ")





# conn = st.connection("sql")
#df = conn.query("SELECT * FROM fromage")
# st.dataframe(df)

