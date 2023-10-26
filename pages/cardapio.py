import streamlit as st
import pymongo

mongo_url = "mongodb+srv://admin:admin@projetoagil.3bq3al9.mongodb.net/"
client = pymongo.MongoClient(mongo_url)
db = client["App"]
collection = db['cardapio']

selected_collection = db['pedidos']

pratos_selecionados = {}
st.title("Cardápio")
pratos_info = list(collection.find({}, {"_id": 0, "name": 1, "description": 1, "price": 1}))
for prato_info in pratos_info:
    nome_prato = prato_info["name"]
    quantidade_sel = st.number_input(f"{nome_prato}", min_value=0, value=0)
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
    data = {
        "nome": nomes,
        "quantidade": quantidades,
        "status": "Em preparo"
    }
    pedido_id = selected_collection.insert_one(data)
    st.write("Pedido adicionado com sucesso")

client.close()