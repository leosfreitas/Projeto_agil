from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
import pymongo

app = Flask(__name__)
mongo_url = "mongodb+srv://admin:admin@projetoagil.3bq3al9.mongodb.net/"
client = pymongo.MongoClient(mongo_url)
db = client["App"]
collection = db['cardapio']

pedidos_collection = db['pedidos']

@app.route('/cardapio', methods=['GET'])
def get_cardapio():
    try:
        filter_ = {}
        projection_ = {}
        cardapio = list(collection.find(filter_, projection_))
        for prato in cardapio:
            prato["_id"] = str(prato["_id"])
        return {"cardapio": cardapio}, 200
    except Exception as e:
        return {"erro":str(e)}, 500
        
@app.route('/pedidos', methods=['POST'])
def inserir_pedido():
    try:
        data = request.json
        id_pedido = pedidos_collection.insert_one(data)
        print(id_pedido.inserted_id)
        return {"_id": str(id_pedido.inserted_id)}, 201
    except Exception as e:
        return {"erro":str(e)}, 500    

@app.route('/restaurante/pedidos', methods=['POST'])
def update_pedido():
    try:
        data = request.json
        pedidos_collection.update_one({"_id": data['_id']}, {"$set": {'status': data['status']}})
        return {'Mensagem': 'Pedido atualizado com sucesso!'}, 200
    except Exception as e:
        return {"erro":str(e)}, 500    

@app.route('restaurante/pedidos', methods=['DELETE'])
def delete_pedido():
    try:
        data = request.json
        pedidos_collection.delete_one({"_id": data['_id']})
        return {'Mensagem': 'Pedido deletado com sucesso!'}, 200
    except Exception as e:
        return {"erro":str(e)}, 500

@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    try:
        filter_ = {}
        projection_ = {}
        pedidos = list(pedidos_collection.find(filter_, projection_))
        for pedido in pedidos:
            pedido["_id"] = str(pedido["_id"])
        return {"pedidos": pedidos}, 200
    except Exception as e:
        return {"erro":str(e)}, 500
        

if __name__ == "__main__":
    app.run(debug=True)
