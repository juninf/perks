import streamlit as st
import random
import time
from pathlib import Path
from zipfile import ZipFile
import tempfile
from streamlit_lottie import st_lottie
import json

# ================== CONFIG ==================
prob_perk = {"comum":0.7, "raro":0.85, "epico":0.95, "lendario":0.9999, "mitico":1.0}
perks_por_raridade = {"comum":[1,2,3,4,5],"raro":[6,7,8,9],"epico":[10,11,12],"lendario":[13,14,15,16],"mitico":[98,99]}
prob_perks_lendario = {13:0.1,14:0.3,15:0.4,16:0.16,98:0.02,99:0.02}

def sortear_raridade():
    r=random.random()
    if r<prob_perk["comum"]: return "comum"
    elif r<prob_perk["raro"]: return "raro"
    elif r<prob_perk["epico"]: return "epico"
    elif r<prob_perk["lendario"]: return "lendario"
    else: return "mitico"

def sortear_perk_dentro_raridade(raridade):
    perks=perks_por_raridade[raridade]
    if raridade=="lendario":
        r=random.random()
        acumulado=0
        for perk,prob in prob_perks_lendario.items():
            acumulado+=prob
            if r<acumulado: return perk
        return perks[0]
    return random.choice(perks)

def sortear_perk_completo():
    return sortear_perk_dentro_raridade(sortear_raridade())

def cor_raridade(numero):
    if 1<=numero<=5: return "#D9D9D9"
    elif 6<=numero<=9: return "#ADD8E6"
    elif 10<=numero<=12: return "#E6CCFF"
    elif 13<=numero<=16: return "#FFD700"
    elif numero in [98,99]: return "#FF69B4"
    return "#FFFFFF"

# ================== CARREGAR IMAGENS ==================
pasta_imagens = Path(__file__).parent / "images"
imagens_perks = {int(img.stem): img for img in pasta_imagens.glob("*.png")}

# ================== CARREGAR ANIMAÇÃO LOTTIE ==================
with open(Path(__file__).parent / "lottie/spinning.json", "r") as f:
    lottie_spinning = json.load(f)

# ================== APP ==================
st.set_page_config(page_title="Roleta de Perks", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Roleta de Perks</h1>", unsafe_allow_html=True)

if st.button("🎲 Girar!"):
    placeholder = st.empty()

    # 1️⃣ Mostrar animação Lottie de suspense
    st_lottie(lottie_spinning, height=300, key="spin")

    time.sleep(2.5)  # duração do suspense

    # 2️⃣ Sorteio do perk final
    resultado = sortear_perk_completo()
    img_final = imagens_perks[resultado]
    cor = cor_raridade(resultado)

    # 3️⃣ Mostrar imagem final centralizada e grande
    placeholder.empty()  # remove Lottie
    st.image(img_final, width=400, use_column_width=False)
    st.markdown(
        f"<h2 style='text-align:center; color:{cor}; font-weight:bold;'>🎯 Perk {resultado}</h2>",
        unsafe_allow_html=True
    )
