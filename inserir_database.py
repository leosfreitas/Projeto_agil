from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:admin@projetoagil.3bq3al9.mongodb.net/App"
mongo = PyMongo(app)

@app.route('/cardapio', methods=['POST'])
def inserir_prato():
    try:
        data = request.json
        id_item = mongo.db.cardapio.insert_one(data)
        print(id_item.inserted_id)
        return {"_id": str(id_item.inserted_id)}, 201
    except Exception as e:
        return {"erro":str(e)}, 500
    
if __name__ == "__main__":
    app.run(debug=True)
