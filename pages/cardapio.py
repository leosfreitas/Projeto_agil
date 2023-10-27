import streamlit as st
import pymongo
import requests

pratos_selecionados = {}
st.title("Cardápio")

pratos_info = requests.get('http://localhost:5000/cardapio').json()['cardapio']
for prato_info in pratos_info:
    nome_prato = prato_info["name"]
    quantidade_sel = st.number_input(f"{nome_prato}", min_value=0, max_value=4, value=0)
    if quantidade_sel > 0:
        pratos_selecionados[nome_prato] = {
            "quantidade": quantidade_sel,
        }

st.title('Resumo do pedido')
for nome, dados in pratos_selecionados.items():
    quantidade = dados["quantidade"]
    st.write(f"**{nome}:** {quantidade}")

if st.button('Adcionar pedido'):
    nomes = []
    quantidades = []
    for nome, dados in pratos_selecionados.items():
        quantidade = dados['quantidade']
        nomes.append(nome)
        quantidades.append(quantidade)
    inserir_prato = requests.post('http://localhost:5000/pedidos', json={"id": 0, "nome": nomes, "quantidade": quantidades, "status": "Em preparo"})
    st.write("Pedido adicionado com sucesso")
    pratos_selecionados.clear()
