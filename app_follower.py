import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pronostici Sportivi", page_icon="📋")

st.title("📋 Pronostici Sportivi")

@st.cache_data(ttl=60)
def carica_pronostici():
    url = "https://raw.githubusercontent.com/ilconsiglieredellescommesse/pronostici-sportivi/master/pronostici.csv"
    return pd.read_csv(url)

try:
    df = carica_pronostici()
    st.dataframe(df)
except:
    st.error("Errore nel caricamento dei pronostici da GitHub.")
