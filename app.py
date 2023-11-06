from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
import pymongo

app = Flask(__name__)
mongo_url = "mongodb+srv://admin:admin@projetoagil.3bq3al9.mongodb.net/"
client = pymongo.MongoClient(mongo_url)
db = client["App"]
collection = db['cardapio']

pedidos_collection = db['pedidos']
contador_collection = db['contador']
contador_collection.insert_one({'id': 'pedido_id', 'sequence_value': 0})

def get_next_pedido_id():
    sequence_doc = contador_collection.find_one_and_update(
        {'_id': 'pedido_id'},
        {'$inc': {'sequence_value': 1}},
        return_document=True
    )
    return sequence_doc['sequence_value']

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
    
@app.route('/cardapio', methods=['POST'])
def add_cardapio():
    try:
        data = request.json
        if not all (dado in data for dado in ("name","description","price")):
            return jsonify({"erro":"Requisição inválida"}), 400
        for dado in data.values():
            if dado in (None,''):
                return jsonify({"erro":"Requisição inválida"}), 400
        filter_ = {}
        projection_ = {}
        pratos = list(collection.find(filter_, projection_))
        for prato in pratos:
            if prato["name"] == data["name"]:
                return jsonify({"erro":"Prato já cadastrado"}), 400
        prato_id = collection.insert_one(data)
        return {"_id": str(prato_id.inserted_id)}, 201
    except Exception as e:
        return {"erro":str(e)}, 500

@app.route('/cardapio/', methods=['DELETE'])
def delete_cardapio():
    print('entrou')
    try:
        data = request.json
        collection.delete_one({"_id": ObjectId(data['_id'])})
        return jsonify({'Mensagem': 'Prato deletado com sucesso!'}), 200
    except Exception as e:
        return {"erro":str(e)}, 500
     
@app.route('/pedidos', methods=['POST'])
def inserir_pedido():
    try:
        data = request.json
        data['id'] = get_next_pedido_id()
        id_pedido = pedidos_collection.insert_one(data)
        print(id_pedido.inserted_id)
        return {"_id": str(id_pedido.inserted_id)}, 201
    except Exception as e:
        return {"erro":str(e)}, 500    


@app.route('/pedidos/<pedido_id>', methods=['GET'])
def buscar_pedido_por_id(pedido_id):
    try:
        id_pedido =  ObjectId(pedido_id)
        pedido = pedidos_collection.find_one({"_id": id_pedido},{'_id': 0} )
        if pedido:
            return jsonify({"pedido": pedido}), 200
        else:
            return jsonify({"message": "Pedido não encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/restaurante/pedidos', methods=['PUT'])
def update_pedido():
    try:
        data = request.json
        pedidos_collection.update_one({"_id": ObjectId(data['_id'])}, {"$set": {"status": data['status']}})
        return {'Mensagem': 'Pedido atualizado com sucesso!'}, 200
    except Exception as e:
        return {"erro":str(e)}, 500    

@app.route('/restaurante/pedidos', methods=['DELETE'])
def delete_pedido():
    try:
        data = request.json
        pedidos_collection.delete_one({"_id": ObjectId(data['_id'])})
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
