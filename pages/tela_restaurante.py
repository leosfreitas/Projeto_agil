import streamlit as st 
import pandas as pd
import pymongo 

mongo_url = "mongodb+srv://admin:admin@projetoagil.3bq3al9.mongodb.net/"
client = pymongo.MongoClient(mongo_url)
db = client["App"]
collection = db['pedidos']

st.header('Pedidos:')

tab1, tab2 = st.tabs(["Pedidos", "Historico"])

pedidos = collection.find()

with tab1:
    for pedido in pedidos:
        if pedido['status'] == 'Em preparo':
            st.markdown('- ' + pedido['nome'])
            st.markdown('- ' + pedido['status'])
            if st.button('**Pronto**', key=pedido['_id']):
                collection.update_one({"_id": pedido['_id']}, {"$set": {'status': 'Pronto'}})
        elif pedido['status'] == 'Pronto':
            st.markdown('- ' + pedido['nome'])
            st.markdown('- ' + pedido['status'])
            if st.button('**Retirado**', key=pedido['_id']):
                collection.update_one({"_id": pedido['_id']}, {"$set": {'status': 'Retirado'}})

pedidos = collection.find()

with tab2:
    for pedido in pedidos:
        if pedido['status'] == 'Retirado':
            st.markdown('- ' + pedido['nome'])
            st.markdown('- ' + pedido['status'])
            if st.button('**Deletar**', key=pedido['_id']):
                collection.delete_one({"_id": pedido['_id']})