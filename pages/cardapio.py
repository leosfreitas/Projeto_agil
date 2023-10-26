import streamlit as st 
import pandas as pd
import pymongo 

mongo_url = "mongodb+srv://admin:admin@projetoagil.3bq3al9.mongodb.net/"
client = pymongo.MongoClient(mongo_url)
db = client["App"]
collection = db['cardapio']

selected_collection = db['pedidos']

st.sidebar.title('Resumo do Pedido')

st.title('Cardápio')
st.subheader('Itens disponíveis:')

itens = collection.find()

itens_selecionados = []
for item in itens:
    item_selected = st.checkbox(f"**Nome:** {item['name']}")
    st.write(f"**Descrição:** {item['description']}")
    if item_selected:
        itens_selecionados.append(item)

for item in itens_selecionados:
    st.sidebar.write(item['name'])

if st.sidebar.button('Adicionar pedido'):
    for item in itens_selecionados:

        data = {
            "nome": item['name'],
            "status": "Em preparo" 
        }

        id_pedido = selected_collection.insert_one(data)

    itens_selecionados.clear()


client.close()