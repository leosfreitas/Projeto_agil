import streamlit as st
import pymongo

mongo_url = "mongodb+srv://admin:admin@projetoagil.3bq3al9.mongodb.net/"
client = pymongo.MongoClient(mongo_url)
db = client["App"]
collection = db['pedidos']

pedidos_preparo = list(db['pedidos'].find({"status": "Em preparo"}))
pedidos_pronto = list(db['pedidos'].find({"status": "Pronto"}))

st.title('Em preparo:')
for pedido in pedidos_preparo:
    st.write(pedido['id'])

st.title('Pronto:')
for pedido in pedidos_pronto:
    st.write(pedido['id'])

client.close()