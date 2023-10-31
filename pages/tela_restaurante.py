import streamlit as st 
import pandas as pd
import pymongo 
import requests

BASE_URL = 'http://127.0.0.1:5000/'

st.header('Pedidos:')

tab1, tab2 = st.tabs(["Pedidos", "Historico"])

pedidos = requests.get(f'{BASE_URL}pedidos').json()["pedidos"]

with tab1:
    for pedido in pedidos:
        if pedido['status'] == 'Em preparo':
            st.write(pedido['id'])
            for i in range(len(pedido['nome'])):
                st.markdown('- ' + pedido['nome'][i])
                st.markdown('- ' + 'Quantidade: ' + str(pedido['quantidade'][i]))
            st.markdown('- ' + pedido['status'])
            if st.button('**Pronto**', key=pedido['_id']):
                atualizar_pedido = requests.put(f'{BASE_URL}restaurante/pedidos', json={"_id": pedido['_id'], 'status': 'Pronto'})
        elif pedido['status'] == 'Pronto':
            st.write(pedido['id'])
            for i in range(len(pedido['nome'])):
                st.markdown('- ' + pedido['nome'][i])
                st.markdown('- ' + 'Quantidade: ' + str(pedido['quantidade'][i]))
            st.markdown('- ' + pedido['status'])
            if st.button('**Retirado**', key=pedido['_id']):
                atualizar_pedido = requests.put(f'{BASE_URL}restaurante/pedidos', json={"_id": pedido['_id'], 'status': 'Retirado'})

pedidos = requests.get(f'{BASE_URL}pedidos').json()['pedidos']

with tab2:
    for pedido in pedidos:
        if pedido['status'] == 'Retirado':
            st.write(pedido['id'])
            for i in range(len(pedido['nome'])):
                st.markdown('- ' + pedido['nome'][i])
                st.markdown('- ' + 'Quantidade: ' + str(pedido['quantidade'][i]))
            st.markdown('- ' + pedido['status'])
            if st.button('**Deletar**', key=pedido['_id']):
                deletar_pedido = requests.delete(f'{BASE_URL}restaurante/pedidos', json={"_id": pedido['_id']})