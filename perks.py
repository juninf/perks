import streamlit as st
import random
import time

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

imagens_perks = {
    1: "https://drive.google.com/uc?export=view&id=17kjno1X8Tfm7Mim0FtGvkc78MIvGLEyR",
    2: "https://drive.google.com/uc?export=view&id=1nwRAC94ottKdfXDKAZk_gECK2eI6diU8",
    3: "https://drive.google.com/uc?export=view&id=1W4Z-Z6lYELvq4gz3E4WgLBoYeVYZdmQX",
    4: "https://drive.google.com/uc?export=view&id=1Yjh9oWyBmvcPpIPFyvciih9qpYJSaPpO",
    5: "https://drive.google.com/uc?export=view&id=1zb1x_OUIgZhFgEo4NNgJB8GTWzRdRNSQ",
    6: "https://drive.google.com/uc?export=view&id=1setyGf74g-xwrkOR5aE8RU2LcWXu0uDF",
    7: "https://drive.google.com/uc?export=view&id=1ZYjCqAlIaRN-epAa6FSC683tIKzp3FEz",
    8: "https://drive.google.com/uc?export=view&id=1q91wjDbLIcEYHIcYZO_xT0NiW7wd7Gg5",
    9: "https://drive.google.com/uc?export=view&id=1sbPP5WQV62LWbCdVQnpzb2ZlMtx3rlmc",
    10: "https://drive.google.com/uc?export=view&id=1_vNtjhm9h9vRIF-ppFGPc3QeodRpxRo6",
    11: "https://drive.google.com/uc?export=view&id=1D_98-SsAN7qkzmhAWKgpR6KS0NtVmFp0",
    12: "https://drive.google.com/uc?export=view&id=1CJYAFjYL8S7DGewDR-PxtmllCbOa9ZoO",
    13: "https://drive.google.com/uc?export=view&id=1HOuwFmggOGNw7Ozd2_fveZd_EsheYnoK",
    14: "https://drive.google.com/uc?export=view&id=1zFMUITltLQGO24LCPKX6zSk5vIm-khia",
    15: "https://drive.google.com/uc?export=view&id=1WLjBFDKAU5x1waKSV0RXLqbsDn49mkoK",
    16: "https://drive.google.com/uc?export=view&id=1kIk3pMNbL49tAdaVRCA5MQo_ag_79L8k",
    98: "https://drive.google.com/uc?export=view&id=1bK2gEFvGy6oIFiwdmlanQICeqKLHC-yx",
    99: "https://drive.google.com/uc?export=view&id=1xguwjrzd2eyky5edDoOxf_tZe839ZmKk"
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

# ================== APP ==================
st.set_page_config(page_title="Roleta de Perks", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Roleta de Perks</h1>", unsafe_allow_html=True)

if st.button("🎲 Girar!"):
    placeholder = st.empty()

    # Animação fake de rolagem
    for i in range(10):
        temp = random.choice(list(imagens_perks.values()))
        with placeholder.container():
            st.image(temp, width=120)
        time.sleep(0.1 + i*0.05)  # aumenta o delay (efeito de desacelerar)

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
