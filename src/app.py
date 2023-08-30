"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicle, Planet, Favourite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoints # Poner servidor en publico, sino no funciona mister postman

# [GET] /people Listar todos los registros de people en la base de datos✅
# [GET] /people/<int:people_id> Listar la información de una sola people
# [GET] /planets Listar los registros de planets en la base de datos ✅
# [GET] /planets/<int:planet_id> Listar la información de un solo planet
# [GET] /users Listar todos los usuarios del blog ✅
# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.

# PEOPLE
@app.route('/people', methods=['GET'])
def get_people():
    people_query = People.query.all()
    results = list(map(lambda item: item.serialize(), people_query))
    print("result people: ", results)
    response_body = { "msg": "These are the People from Star Wars",
                     "results": results}
    
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    one_people = People.query.filter_by(id=people_id).first()
    response_body = { "msg": "This is the one you are looking for",
                     "results": one_people.serialize()}
    
    return jsonify(response_body), 200


# PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planet_query = Planet.query.all()
    results = list(map(lambda item: item.serialize(), planet_query))
    print("result planet: ", results)
    response_body = { "msg": "These are the Planets from Star Wars",
                     "results": results}
    
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    one_planet = Planet.query.filter_by(id=planet_id).first()
    response_body = { "msg": "This is the one you are looking for",
                     "results": one_planet.serialize()}
    
    return jsonify(response_body), 200


# USERS
@app.route('/users', methods=['GET'])
def get_users():
    user_query = User.query.all()
    results = list(map(lambda item: item.serialize(), user_query))
    print("result user: ", results)
    response_body = { "msg": "These are the users",
                     "results": results}
    
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    one_user = User.query.filter_by(id=user_id).first()
    response_body = { "msg": "This is the one you are looking for",
                     "results": one_user.serialize()}
    
    return jsonify(response_body), 200

# FAVOURITE
@app.route('/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourite(user_id):

    print("TEST 1: ", user_id)

    # favourite_query = Favourite.query.filter_by(id=user_id).first()
    # print("TEST 2: ", favourite_query) # None

    # favourite_query_2 = Favourite.query.all()
    # print("TEST 3: ", favourite_query_2)

    # favourite_query_3 = list(map(lambda item: item.serialize(), favourite_query_2))
    # print("TEST 4: ", favourite_query_3) # hay que serializar en models
    
    # id_user es de model y user_id es el param del path
    favourite_query_4 = Favourite.query.filter_by(id_user = user_id).all() # devuelve una lista al ser .all(), hay que mapear
    print("TEST 5: ", favourite_query_4)

    #favourite_query_5 =  favourite_query_4.serialize()
    favourite_query_5 =  list(map(lambda item: item.serialize(), favourite_query_4))
    print("TEST 5: ", favourite_query_5)     

    #favourite_query = Favourite.query.filter_by(id=user_id).first()
    # favoritos = Favourite.query.filter_by(user_id=user_id).all()
    
    #print("favourite_query: ", favourite_query)
    #print("favourite_query serialize: ", favourite_query.serialize())
    # datos_favoritos = [f.serialize() for f in favoritos]
    #datos_favoritos = list(map(lambda item: item.serialize(), favourite_query))
    #print("datos_favoritos: ", datos_favoritos)

    response_body = { "msg": "These is the one you are looking for",
                     "results": favourite_query_5}
    
    return jsonify(response_body), 200

  

  




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
