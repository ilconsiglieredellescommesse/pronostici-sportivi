
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pronostici Follower", page_icon="📱", layout="centered")

# Parametri nascosti per admin (per futura personalizzazione)
params = st.query_params
admin_mode = params.get("admin", ["false"])[0].lower() == "true"

# Sezione grafica personalizzabile solo per te
if admin_mode:
    colore = st.color_picker("🎨 Colore Titolo", "#0F8CFF")
    titolo = st.text_input("🖋️ Titolo Personalizzato", "📋 Pronostici – Solo Visualizzazione")
else:
    colore = "#0F8CFF"
    titolo = "📋 Pronostici Sportivi"

# Stile responsivo
st.markdown(f"""
    <h1 style='text-align: center; color: {colore};'>{titolo}</h1>
   
""", unsafe_allow_html=True)

FILE = "pronostici.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    if not df.empty:
        df_vista = df[["Data", "Sport", "Evento", "Pronostico", "Quota", "Esito"]]
        st.dataframe(df_vista, hide_index=True, use_container_width=True)
    else:
        st.info("Nessun pronostico disponibile.")
else:
    st.warning("Il file pronostici.csv non è stato trovato.")
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
