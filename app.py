import streamlit as st
import json
import os

st.set_page_config(layout="wide")

# carregar dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(BASE_DIR, "dados.json")

with open(caminho, encoding="utf-8") as f:
    dados = json.load(f)

st.title("🌎 Catálogo de Solos e Vegetação")

# filtros
col1, col2, col3 = st.columns(3)

with col1:
    busca = st.text_input("Buscar")

with col2:
    tipos = sorted(set(d["tipo"] for d in dados))
    tipo = st.selectbox("Tipo", ["Todos"] + tipos)

with col3:
    # classes dependentes do tipo
    if tipo == "Todos":
        classes_filtradas = sorted(set(d["classe"] for d in dados))
    else:
        classes_filtradas = sorted(set(
            d["classe"] for d in dados if d["tipo"] == tipo
        ))

    classe = st.selectbox("Classe", ["Todas"] + classes_filtradas)

# função de filtro
def filtrar(d):
    if busca.lower() not in d["nome"].lower():
        return False
    if tipo != "Todos" and d["tipo"] != tipo:
        return False
    if classe != "Todas" and d["classe"] != classe:
        return False
    return True

filtrados = [d for d in dados if filtrar(d)]

st.write(f"Resultados: {len(filtrados)}")

# separar por tipo
solos = [d for d in filtrados if d["tipo"] == "Solo"]
vegetacao = [d for d in filtrados if d["tipo"] == "Vegetação"]

# função pra desenhar grid
def mostrar_grid(lista):
    cols = st.columns(5)
    for i, item in enumerate(lista):
        with cols[i % 5]:
            st.markdown(f"""
            <div style="
                background:{item['hex']};
                padding:20px;
                border-radius:10px;
                margin-bottom:10px;
                color:black;
                text-align:center;
            ">
                <b>{item['nome']}</b><br>
                <small>{item['hex']}</small>
            </div>
            """, unsafe_allow_html=True)

# exibição separada
if tipo in ["Todos", "Solo"] and solos:
    st.subheader("🟤 Solos")
    mostrar_grid(solos)

if tipo in ["Todos", "Vegetação"] and vegetacao:
    st.subheader("🌿 Vegetação")
    mostrar_grid(vegetacao)
