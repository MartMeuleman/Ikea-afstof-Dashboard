import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="IKEA Afstof Dashboard", layout="wide")

# --- Instellingen ---
DAGEN = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
BEGANE_GROND = [
    "Koken en eten", "Woontextiel", "Bedtextiel", "Badkamers", "Opbergen", "Verlichting",
    "Vloerkleden", "Wanddecoratie", "Woondecoratie", "Planten", "Zelfbedieningsmagazijn",
    "Ingang", "Kassalijn", "SFM (kassa swedish market)"
]
EERSTE_ETAGE = [
    "First 5", "Woonkamers", "Wandmeubels", "Eetkamers", "Keukens",
    "Werkplekken", "Slaapkamers", "Garderobekasten", "IKEA kinderland"
]

CSV_LOGBOEK = "afstof_logboek.csv"

# --- Laad of maak logboek ---
if os.path.exists(CSV_LOGBOEK):
    logboek = pd.read_csv(CSV_LOGBOEK)
else:
    logboek = pd.DataFrame(columns=["Dag", "Naam", "Afdeling", "Verdieping", "Notitie"])

# --- Reset automatisch op maandag ---
vandaag = datetime.today().strftime("%A")
if vandaag == "Monday" and not logboek.empty:
    logboek = pd.DataFrame(columns=["Dag", "Naam", "Afdeling", "Verdieping", "Notitie"])
    logboek.to_csv(CSV_LOGBOEK, index=False)

# --- Interface ---
st.title("🧽 IKEA Afstof Dashboard")

col1, col2 = st.columns([1, 3])
with col1:
    dag = st.selectbox("📅 Kies de dag:", DAGEN)
    naam = st.text_input("👤 Jouw naam:")
    verdieping = st.radio("📍 Kies de verdieping:", ["Begane grond", "Eerste etage"])
    notitie = st.text_area("📝 Notitie (optioneel):", placeholder="Bijv. alleen rechterkant gedaan, tot helft gekomen...")

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
            "Verdieping": [verdieping] * len(geselecteerd),
            "Notitie": [notitie] * len(geselecteerd)
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

# --- Overzicht nog te doen per dag voor beide verdiepingen ---
st.markdown("---")
st.subheader(f"🕓 Wat moet nog afgestoft worden op {dag}?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏠 Begane grond")
    logboek_bg = logboek[logboek["Verdieping"] == "Begane grond"]
    afgestoft_bg = logboek_bg["Afdeling"].unique().tolist()
    nog_te_doen_bg = [a for a in BEGANE_GROND if a not in afgestoft_bg]

    if nog_te_doen_bg:
        st.write("Nog te doen:")
        for afdeling in nog_te_doen_bg:
            st.markdown(f"- 🔲 {afdeling}")
    else:
        st.success("🎉 Alles is afgestoft op de begane grond!")

with col2:
    st.markdown("### 🛋️ Eerste etage (showroom)")
    logboek_etage_dag = logboek[(logboek["Verdieping"] == "Eerste etage") & (logboek["Dag"] == dag)]
    logboek_etage_week = logboek[logboek["Verdieping"] == "Eerste etage"]
    afgestoft_etage = logboek_etage_week["Afdeling"].unique().tolist()

    # 'First 5' moet dagelijks gebeuren, andere 1x per week
    nog_te_doen_etage = []
    for afdeling in EERSTE_ETAGE:
        if afdeling == "First 5":
            if afdeling not in logboek_etage_dag["Afdeling"].unique().tolist():
                nog_te_doen_etage.append(afdeling)
        else:
            if afdeling not in afgestoft_etage:
                nog_te_doen_etage.append(afdeling)

    if nog_te_doen_etage:
        st.write("Nog te doen:")
        for afdeling in nog_te_doen_etage:
            st.markdown(f"- 🔲 {afdeling}")
    else:
        st.success("🎉 Alles is afgestoft op de eerste etage!")


