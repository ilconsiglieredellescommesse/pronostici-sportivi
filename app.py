
import streamlit as st
import pandas as pd
import os
import json
import subprocess

st.set_page_config(page_title="Gestione Pronostici", page_icon="⚽")

FILE = "pronostici.csv"
USERS = "users.json"

def carica_pronostici():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=["Data", "Sport", "Evento", "Pronostico", "Quota", "Esito", "Note"])

def salva_pronostici(df):
    df.to_csv(FILE, index=False)

def carica_utenti():
    if os.path.exists(USERS):
        with open(USERS, "r") as f:
            return json.load(f)
    return {}

def salva_utenti(utenti):
    with open(USERS, "w") as f:
        json.dump(utenti, f)

st.markdown("### Accesso Amministratore")
azione = st.radio("Seleziona azione", ["Login", "Registrati"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")

sessione = st.session_state
if "loggato" not in sessione:
    sessione.loggato = False

utenti = carica_utenti()

def login():
    if username in utenti and utenti[username] == password:
        sessione.loggato = True
        sessione.utente = username
        st.success("Login effettuato")
    else:
        st.error("Credenziali non valide")

def registrati():
    if username in utenti:
        st.warning("Utente già registrato")
    else:
        utenti[username] = password
        salva_utenti(utenti)
        st.success("Registrazione completata")

if azione == "Login":
    if st.button("Login"):
        login()
else:
    if st.button("Registrati"):
        registrati()

if sessione.loggato:
    st.title("📊 App Pronostici - Gestione Completa")

    df = carica_pronostici()

    with st.form("inserimento"):
        col1, col2 = st.columns(2)
        data = col1.date_input("Data")
        quota = col2.number_input("Quota", min_value=1.01, step=0.01)

        col3, col4 = st.columns(2)
        sport = col3.selectbox("Sport", ["Calcio", "Basket", "Tennis"])
        evento = col4.text_input("Evento")

        pronostico = st.text_input("Pronostico")
        esito = st.selectbox("Esito", ["In attesa", "Vinto", "Perso"])
        note = st.text_input("Note (facoltative)")

        submitted = st.form_submit_button("Salva")
        if submitted:
            nuovo = {
                "Data": data,
                "Sport": sport,
                "Evento": evento,
                "Pronostico": pronostico,
                "Quota": quota,
                "Esito": esito,
                "Note": note
            }
            df = pd.concat([df, pd.DataFrame([nuovo])], ignore_index=True)
            salva_pronostici(df)
            st.success("Pronostico salvato")

    st.markdown("### Pronostici salvati")
    st.dataframe(df)

    st.markdown("### Elimina pronostico")
    riga = st.number_input("Numero riga da eliminare (inizia da 0)", min_value=0, max_value=len(df)-1 if len(df) > 0 else 0, step=1)
    if st.button("Elimina pronostico selezionato"):
        if not df.empty and riga < len(df):
            df = df.drop(riga).reset_index(drop=True)
            salva_pronostici(df)
            st.success("Pronostico eliminato")

    # NUOVO PULSANTE: Sincronizza con GitHub
if st.button("Sincronizza su GitHub"):
    result = os.system("sync_github.bat")
    if result == 0:
        st.success("Sincronizzazione avviata! Controlla il terminale.")
    else:
        st.warning("Controlla se il file .bat funziona correttamente.")

    if st.button("Logout"):
        sessione.loggato = False
        st.rerun()
