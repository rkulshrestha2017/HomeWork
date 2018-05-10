from flask import Flask
from flask import render_template
from pymongo import MongoClient
from flask import jsonify
import json
from bson import json_util
from bson.json_util import dumps
from flask_cors import CORS, cross_origin

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'gtlddb'
COLLECTION_NAME1 = 'registrar'
FIELDS1 = {'registrar': True, 'total_domains': True, 'change': True, 'percent_share': True, '_id': False}

COLLECTION_NAME2 = 'total_registrar'
FIELDS2 = {'total_registrar': True, 'date': True,'_id': False}

COLLECTION_NAME3 = 'tlds'
FIELDS3 = {'tlds': True, 'count': True, 'share': True, 'url': True,'_id': False}

COLLECTION_NAME4 = 'tlds_count'
FIELDS4 = {'date': True, 'count': True, '_id': False}

COLLECTION_NAME5 = 'registries'
FIELDS5 = {'registries': True, 'count': True, 'share': True, '_id': False}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gtlddb/registrar")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def gtlddb_registrars():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME1]
    registrars = collection.find(projection=FIELDS1)
    json_registrar = []
    for registrar in registrars:
        json_registrar.append(registrar)
    # json_registrar = json.dumps(json_registrar, default=json_util.default)
    connection.close()
    return jsonify(data = json_registrar)

@app.route("/gtlddb/totalregistrar")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def gtlddb_totalregistrars():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME2]
    registrars = collection.find(projection=FIELDS2)
    json_registrar = []
    for registrar in registrars:
        json_registrar.append(registrar)
    # json_registrar = json.dumps(json_registrar, default=json_util.default)
    connection.close()
    return jsonify(data = json_registrar)

@app.route("/gtlddb/tlds")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def gtlddb_tlds():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME3]
    registrars = collection.find(projection=FIELDS3)
    json_registrar = []
    for registrar in registrars:
        json_registrar.append(registrar)
    # json_registrar = json.dumps(json_registrar, default=json_util.default)
    connection.close()
    return jsonify(data = json_registrar)

@app.route("/gtlddb/tldscount")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def gtlddb_tldscount():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME4]
    registrars = collection.find(projection=FIELDS4)
    json_registrar = []
    for registrar in registrars:
        json_registrar.append(registrar)
    # json_registrar = json.dumps(json_registrar, default=json_util.default)
    connection.close()
    return jsonify(data = json_registrar)

@app.route("/gtlddb/registries")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def gtlddb_registries():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME5]
    registrars = collection.find(projection=FIELDS5)
    json_registrar = []
    for registrar in registrars:
        json_registrar.append(registrar)
    # json_registrar = json.dumps(json_registrar, default=json_util.default)
    connection.close()
    return jsonify(data = json_registrar)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)