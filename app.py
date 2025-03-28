import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="IKEA Afstof Dashboard", layout="wide")

# --- Instellingen ---
DAGEN = ["Maandag / Понеділок", "Dinsdag / Вівторок", "Woensdag / Середа", "Donderdag / Четвер", "Vrijdag / П’ятниця", "Zaterdag / Субота", "Zondag / Неділя"]
BEGANE_GROND = [
    "Koken en eten / Приготування їжі", "Woontextiel / Домашній текстиль", "Bedtextiel / Постільна білизна", 
    "Badkamers / Ванні кімнати", "Opbergen / Зберігання", "Verlichting / Освітлення",
    "Vloerkleden / Килими", "Wanddecoratie / Настінний декор", "Woondecoratie / Декор для дому", 
    "Planten / Рослини", "Zelfbedieningsmagazijn / Склад самообслуговування"
]
EERSTE_ETAGE = [
    "Ingang showroom (first 5) / Вхід у шоурум (перші 5)", "Woonkamers / Вітальні", 
    "Wandmeubels / Настінні меблі", "Eetkamers / Їдальні", "Keukens / Кухні",
    "Werkplekken / Робочі місця", "Slaapkamers / Спальні", "Garderobekasten / Шафи для одягу", 
    "IKEA kinderland / Дитячий відділ IKEA"
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
st.title("🧽 IKEA Afstof Dashboard / Прибиральна панель IKEA")

col1, col2 = st.columns([1, 3])
with col1:
    dag = st.selectbox("📅 Kies de dag / Обери день:", DAGEN)
    naam = st.text_input("👤 Jouw naam / Твоє ім’я:")
    verdieping = st.radio("📍 Kies de verdieping / Обери поверх:", ["Begane grond / Перший поверх", "Eerste etage / Другий поверх"])

if verdieping.startswith("Begane grond"):
    afdelingen = BEGANE_GROND
else:
    afdelingen = EERSTE_ETAGE

geselecteerd = st.multiselect("✅ Welke afdelingen heb je afgestoft? / Які відділи ти прибрав?", afdelingen)

if st.button("✔️ Opslaan / Зберегти"):
    if naam and geselecteerd:
        nieuwe_records = pd.DataFrame({
            "Dag": [dag.split(" / ")[0]] * len(geselecteerd),
            "Naam": [naam] * len(geselecteerd),
            "Afdeling": geselecteerd,
            "Verdieping": [verdieping.split(" / ")[0]] * len(geselecteerd)
        })
        logboek = pd.concat([logboek, nieuwe_records], ignore_index=True)
        logboek.to_csv(CSV_LOGBOEK, index=False)
        st.success("Afdelingen opgeslagen! / Відділи збережено!")
    else:
        st.warning("Vul je naam in en selecteer ten minste één afdeling. / Введи ім’я та обери хоча б один відділ.")

# --- Overzicht logboek ---
st.markdown("---")
st.subheader("📖 Logboek / Журнал")
dag_filter = st.selectbox("📂 Toon logboek van dag / Показати журнал за день:", ["Alle dagen / Всі дні"] + DAGEN)
if dag_filter.startswith("Alle dagen"):
    st.dataframe(logboek)
else:
    st.dataframe(logboek[logboek["Dag"] == dag_filter.split(" / ")[0]])

# --- Overzicht nog te doen per week voor beide verdiepingen ---
st.markdown("---")
st.subheader("🕓 Wat moet nog afgestoft worden deze week? / Що ще потрібно прибрати цього тижня?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏠 Begane grond / Перший поверх")
    logboek_bg = logboek[logboek["Verdieping"] == "Begane grond"]
    afgestoft_bg = logboek_bg["Afdeling"].unique().tolist()
    nog_te_doen_bg = [a for a in BEGANE_GROND if a not in afgestoft_bg]

    if nog_te_doen_bg:
        st.write("Nog te doen / Ще потрібно зробити:")
        for afdeling in nog_te_doen_bg:
            st.markdown(f"- 🔲 {afdeling}")
    else:
        st.success("🎉 Alles is afgestoft op de begane grond! / Усе прибрано на першому поверсі!")

with col2:
    st.markdown("### 🛋️ Eerste etage (showroom) / Другий поверх (виставка)")
    logboek_etage = logboek[logboek["Verdieping"] == "Eerste etage"]
    afgestoft_etage = logboek_etage["Afdeling"].unique().tolist()
    nog_te_doen_etage = [a for a in EERSTE_ETAGE if a not in afgestoft_etage]

    if nog_te_doen_etage:
        st.write("Nog te doen / Ще потрібно зробити:")
        for afdeling in nog_te_doen_etage:
            st.markdown(f"- 🔲 {afdeling}")
    else:
        st.success("🎉 Alles is afgestoft op de eerste etage! / Усе прибрано на другому поверсі!")


