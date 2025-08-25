import streamlit as st
import random
import time
from pathlib import Path
from zipfile import ZipFile
import tempfile

# ================== CONFIG ==================
prob_perk = {
    "comum": 0.70,
    "raro": 0.85,
    "epico": 0.95,
    "lendario": 0.9999,
    "mitico": 1.0
}

perks_por_raridade = {
    "comum": [1, 2, 3, 4, 5],
    "raro": [6, 7, 8, 9],
    "epico": [10, 11, 12],
    "lendario": [13, 14, 15, 16],
    "mitico": [98, 99]
}

prob_perks_lendario = {
    13: 0.1,
    14: 0.3,
    15: 0.4,
    16: 0.16,
    98: 0.02,
    99: 0.02
}

# ================== FUNÇÕES ==================
def sortear_raridade():
    r = random.random()
    if r < prob_perk["comum"]: return "comum"
    elif r < prob_perk["raro"]: return "raro"
    elif r < prob_perk["epico"]: return "epico"
    elif r < prob_perk["lendario"]: return "lendario"
    else: return "mitico"

def sortear_perk_dentro_raridade(raridade):
    perks = perks_por_raridade[raridade]
    if raridade == "lendario":
        r = random.random()
        acumulado = 0
        for perk, prob in prob_perks_lendario.items():
            acumulado += prob
            if r < acumulado:
                return perk
        return perks[0]
    return random.choice(perks)

def sortear_perk_completo():
    raridade = sortear_raridade()
    return sortear_perk_dentro_raridade(raridade)

def cor_raridade(numero):
    if 1 <= numero <= 5: return "#D9D9D9"   # comum
    elif 6 <= numero <= 9: return "#ADD8E6" # raro
    elif 10 <= numero <= 12: return "#E6CCFF" # épico
    elif 13 <= numero <= 16: return "#FFD700" # lendário
    elif numero in [98, 99]: return "#FF69B4" # mítico
    return "#FFFFFF"

# ================== CARREGAR IMAGENS DO ZIP ==================
zip_path = Path(__file__).parent / "drive-download-20250825T030157Z-1-001.zip"
temp_dir = tempfile.TemporaryDirectory()  # pasta temporária
with ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir.name)

# Mapear imagens para números de perks
imagens_perks = {}
for img_path in Path(temp_dir.name).glob("*.png"):
    try:
        numero = int(img_path.stem)
        imagens_perks[numero] = img_path
    except ValueError:
        continue

# ================== STREAMLIT APP ==================
st.set_page_config(page_title="Roleta de Perks", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Roleta de Perks</h1>", unsafe_allow_html=True)

if st.button("🎲 Girar!"):
    placeholder = st.empty()

    # Animação fake de rolagem
    for i in range(10):
        temp = random.choice(list(imagens_perks.values()))
        with placeholder.container():
            st.image(temp, width=120)
        time.sleep(0.1 + i*0.05)

    # Resultado final
    resultado = sortear_perk_completo()
    url = imagens_perks[resultado]
    cor = cor_raridade(resultado)

    with placeholder.container():
        st.markdown(
            f"""
            <div style='text-align:center;'>
                <img src='{url}' width='160' style='border: 5px solid {cor}; border-radius:20px; box-shadow:0 0 30px {cor};'>
                <p style='color:{cor}; font-size:22px; font-weight:bold;'>🎯 Perk {resultado}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
