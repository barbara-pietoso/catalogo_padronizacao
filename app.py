import streamlit as st
import json
import os

st.set_page_config(layout="wide")

# carregar dados (forma segura pro Streamlit Cloud)
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

# filtro aplicado
filtrados = []
for d in dados:
    if busca.lower() not in d["nome"].lower():
        continue
    if tipo != "Todos" and d["tipo"] != tipo:
        continue
    if classe != "Todas" and d["classe"] != classe:
        continue
    filtrados.append(d)

st.write(f"Resultados: {len(filtrados)}")

# layout em grade
cols = st.columns(5)

for i, item in enumerate(filtrados):
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
