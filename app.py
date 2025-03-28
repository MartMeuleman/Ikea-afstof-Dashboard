import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="IKEA Afstof Dashboard", layout="wide")

# --- Instellingen ---
DAGEN = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
BEGANE_GROND = [
    "Koken en eten", "Woontextiel", "Bedtextiel", "Badkamers", "Opbergen", "Verlichting",
    "Vloerkleden", "Wanddecoratie", "Woondecoratie", "Planten", "Zelfbedieningsmagazijn"
]
EERSTE_ETAGE = [
    "Ingang showroom (first 5)", "Woonkamers", "Wandmeubels", "Eetkamers", "Keukens",
    "Werkplekken", "Slaapkamers", "Garderobekasten", "IKEA kinderland"
]

CSV_LOGBOEK = "afstof_logboek.csv"

# --- Laad of maak logboek ---
if os.path.exists(CSV_LOGBOEK):
    logboek = pd.read_csv(CSV_LOGBOEK)
else:
    logboek = pd.DataFrame(columns=["Dag", "Naam", "Afdeling", "Verdieping"])

# --- Reset automatisch op maandag ---
vandaag = datetime.today().strftime("%A")
if vandaag == "Monday" and not logboek.empty:
    logboek = pd.DataFrame(columns=["Dag", "Naam", "Afdeling", "Verdieping"])
    logboek.to_csv(CSV_LOGBOEK, index=False)

# --- Interface ---
st.title("🧽 IKEA Afstof Dashboard")

col1, col2 = st.columns([1, 3])
with col1:
    dag = st.selectbox("📅 Kies de dag:", DAGEN)
    naam = st.text_input("👤 Jouw naam:")
    verdieping = st.radio("📍 Kies de verdieping:", ["Begane grond", "Eerste etage"])

if verdieping == "Begane grond":
    afdelingen = BEGANE_GROND
else:
    afdelingen = EERSTE_ETAGE

geselecteerd = st.multiselect("✅ Welke afdelingen heb je afgestoft?", afdelingen)

if st.button("✔️ Opslaan"):
    if naam and geselecteerd:
        nieuwe_records = pd.DataFrame({
            "Dag": [dag] * len(geselecteerd),
            "Naam": [naam] * len(geselecteerd),
            "Afdeling": geselecteerd,
            "Verdieping": [verdieping] * len(geselecteerd)
        })
        logboek = pd.concat([logboek, nieuwe_records], ignore_index=True)
        logboek.to_csv(CSV_LOGBOEK, index=False)
        st.success("Afdelingen opgeslagen!")
    else:
        st.warning("Vul je naam in en selecteer ten minste één afdeling.")

# --- Overzicht logboek ---
st.markdown("---")
st.subheader("📖 Logboek")
dag_filter = st.selectbox("📂 Toon logboek van dag:", ["Alle dagen"] + DAGEN)
if dag_filter == "Alle dagen":
    st.dataframe(logboek)
else:
    st.dataframe(logboek[logboek["Dag"] == dag_filter])
