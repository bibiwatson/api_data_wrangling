# coding=utf-8
import os

from flask import Flask, jsonify, request
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

print(os.environ.get('mongo_url_con'))
# conexión a la bd
client  = MongoClient(os.environ.get('mongo_url_con'))
db      = client['onepiece']

# collections
collSets    = db['sets']
collCards   = db['cards']

@app.route('/')
def root():
    return 'hola :)'

@app.route('/hola_mundo')
def holaMundo():
    return 'hola mundo'

@app.route('/sets')
def get_sets():
    try:
        # Consulta a la bd - nos trae todos los registros de la colección sets
        results = collSets.find({}, {'_id': False})

        # variable para guardar los resultados
        data = []

        for result in results:
            data.append(result)

        response = jsonify({
            'success'   : True,
            'entries'   : len(data),
            'data'      : data
        })
    except Exception as e:
        print(e)
        response = jsonify({
            'success': False,
            'msg' : 'Ocurrió un error al obtener la información'
        })

        response.status_code = 500

    return response

@app.route('/set/<id_set>')
def get_cards_by_set(id_set):

    # validamos que el parámetro recibido sea de tipo entero, en caso de que no sea así se devuelve mensaje de error
    try:
        int(id_set)
    except ValueError:
        response =  jsonify({
            'success'   : False,
            'msg'       : 'Parámetro no válido'
        })

        response.status_code = 400
        return response

    # Consulta a la base de datos para obtener los datos del set (expansión)
    resultSet = collSets.find_one({'id': int(id_set)}) 

    # Consulta a la base de datos para obtener todas las cartas que pertenecen a la expansión
    results = collCards.find({'set_id' : int(id_set)}, {'_id': False})

    # variable para guardar los resultados
    data = []

    for result in results:
        data.append(result)

    response = jsonify({
        'success'   : True,
        'entries'   : len(data),
        'data'      : data,
        'set_id'    : id_set,
        'set_name'  : resultSet['name']
    })

    return response


@app.route('/cards')    
def get_cards():
    try:
        qstring     = request.args.get('qstring', type = str)
        rarity      = request.args.get('rarity', type = str)
        card_type   = request.args.get('card_type', type = str)

        # si no se recibió ningún filtro se envía mensaje de error
        if(not qstring and not rarity and not card_type):
            return jsonify({
                'success'   : False,
                'msg'       : 'Por lo menos un parámetro es requerido: qstring, rarity o card_type'
            }), 400


        # variables para los filtros
        qparams = {}
        qparams_and = []

        # llenar los parámetros de búsqueda
        if(qstring):
            search_name_effect_trigger = [
                {'name'     : {'$regex' : qstring, '$options' : 'i'}},
                {'effect'   : {'$regex' : qstring, '$options' : 'i'}},
                {'trigger'  : {'$regex' : qstring, '$options' : 'i'}},
            ]
            qparams['$or'] = search_name_effect_trigger

        if(rarity):
            qparams_and.append({'rarity' : rarity})

        if(card_type):
            qparams_and.append({'card_type' : card_type})

        if(len(qparams_and) > 0):
            qparams['$and'] = qparams_and

        print(qparams)

        # Realizar la consulta a la bd
        results = collCards.find(qparams, {'_id': False})

        # variable para guardar nuestros datos
        data = []

        for result in results:
            data.append(result)

        return jsonify({
            'success'   : True,
            'data'      : data,
            'entries'   : len(data)
        })
    except Exception as e:
        print(e)
        return jsonify({
            'success'   : False,
            'msg'       : 'Ocurrió un error interno al consultar la Info'
        }), 500


if os.environ.get('ENV') == 'dev' :
    app.run(debug = True, host = os.environ.get('HOST'), port = os.environ.get('PORT'))
else:
    app.run()