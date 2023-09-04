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

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

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
# MULTI COMANDO PARA PRENDER EL SERVER >>> pipenv run migrate && pipenv run upgrade && pipenv run start

# [GET] /people Listar todos los registros de people en la base de datos✅
# [GET] /people/<int:people_id> Listar la información de una sola people ✅
# [GET] /planets Listar los registros de planets en la base de datos ✅
# [GET] /planets/<int:planet_id> Listar la información de un solo planet ✅
# [GET] /users Listar todos los usuarios del blog ✅
# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual. ✅

# ALL PEOPLE 👨‍👩‍👧‍👦
@app.route('/people', methods=['GET'])
def get_people():
    people_query = People.query.all()
    results = list(map(lambda item: item.serialize(), people_query))
    print("result people: ", results)
    response_body = { "msg": "These are the People from Star Wars",
                     "results": results}
    
    return jsonify(response_body), 200

# ONE PEOPLE 👨‍💼
@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    one_people = People.query.filter_by(id=people_id).first()

    if not one_people:
        return jsonify({"msg": "People not found"}), 404

    response_body = { "msg": "This is the one you are looking for",
                     "results": one_people.serialize()}
    
    return jsonify(response_body), 200


# ALL PLANETS 🪐🪐🪐
@app.route('/planets', methods=['GET'])
def get_planets():
    planet_query = Planet.query.all()
    results = list(map(lambda item: item.serialize(), planet_query))
    print("result planet: ", results)
    response_body = { "msg": "These are the Planets from Star Wars",
                     "results": results}
    
    return jsonify(response_body), 200

# ONE PLANET 🪐
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    one_planet = Planet.query.filter_by(id=planet_id).first()

    if not one_planet:
        return jsonify({"msg": "Planet not found"}), 404
    
    response_body = { "msg": "This is the one you are looking for",
                     "results": one_planet.serialize()}
    
    return jsonify(response_body), 200


# ALL USERS 👥
@app.route('/users', methods=['GET'])
def get_users():
    user_query = User.query.all()
    results = list(map(lambda item: item.serialize(), user_query))
    print("result user: ", results)
    response_body = { "msg": "These are the users",
                     "results": results}
    
    return jsonify(response_body), 200

# ONE USER 👤
@app.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    one_user = User.query.filter_by(id=user_id).first()

    if not one_user:
        return jsonify({"msg": "User not found"}), 404
    
    response_body = { "msg": "This is the one you are looking for",
                     "results": one_user.serialize()}
    
    return jsonify(response_body), 200

# USER FAVOURITE 🎇🎇🎇
@app.route('/users/<int:user_id>/favourites', methods=['GET'])
@jwt_required()
def get_user_favourite(user_id):
    # .all() obtiene todos
    # .first() obtiene el primero

    # forma .get para obtener user
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    # tomamos el id del token generado y lo comparamos con el user_id que viene
    current_user_id = get_jwt_identity()

    # Verifica si el usuario actual coincide con el usuario solicitado
    if current_user_id != user.id:
        return jsonify({"msg": "You don't have user favorites permission"}), 403

    favourites_list = Favourite.query.filter_by(id_user=user_id).all() # lista de objetos con los id de los fav
    print("TEST favourite user list: ",favourites_list)
    serialized_favourites = []

    if not favourites_list:
        return jsonify({"msg": "User not found"}), 204 # 204 para no contenido, si esta vacia

    # iteramos la lista de favoritos para obtener los objetos serializados de cada entidad, si es que tiene
    for fav in favourites_list:
        serialized_fav = fav.serialize()   
        print(serialized_fav)
        if fav.id_peoples:
            serialized_fav["people"] = fav.people.serialize()
        if fav.id_planets:
            serialized_fav["planet"] = fav.planet.serialize()
        if fav.id_vehicles:
            serialized_fav["vehicle"] = fav.vehicle.serialize()
        
        serialized_favourites.append(serialized_fav)

    response_body = {
        "msg": f"Favourites de usario: {user_id}",
        "results": serialized_favourites
    }
              
    return jsonify(response_body), 200

# [POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el planet id = planet_id.✅
# [POST] /favorite/people/<int:people_id> Añade una nueva people favorita al usuario actual con el people.id = people_id.✅
# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id`.✅
# [DELETE] /favorite/people/<int:people_id> Elimina una people favorita con el id = people_id.✅

# ADD FAVOURITE PLANET 🎇🪐
@app.route('/users/<int:user_id>/favourites/planet/<int:planet_id>', methods=['POST'])
def add_user_favourite_planet(user_id, planet_id):
    # user exist ?
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # planet exist ?
    planet = Planet.query.get(planet_id)
    if planet:
        # planet exist in user-favourite?
        existing_favourite = Favourite.query.filter_by(id_user=user_id, id_planets=planet_id).first()
        if existing_favourite:
            return jsonify({"msg": "Planet already in user's favourites"}), 400
            # Agrega el nuevo favorito a la base de datos
        else:
            new_favourite_planet = Favourite(name="Nombre del favorito", 
                                    id_user=user_id, 
                                    id_peoples=None, 
                                    id_planets=planet_id, 
                                    id_vehicles=None
                                    )
            
            db.session.add(new_favourite_planet)
            db.session.commit()

            return jsonify({"msg": f"Planeta {planet_id} se agrego a favoritos del usuario {user_id} "}), 201

    return jsonify({"msg": "No se pudo agregar nada"}), 404

# ADD FAVOURITE PEOPLE 🎇👨‍💼
@app.route('/users/<int:user_id>/favourites/people/<int:people_id>', methods=['POST'])
def add_user_favourite_people(user_id, people_id):
    # user exist ?
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # people exist ?
    people = People.query.get(people_id)
    if people:
        # people exist in user-favourite?
        existing_favourite = Favourite.query.filter_by(id_user=user_id, id_peoples=people_id).first()
        if existing_favourite:
            return jsonify({"msg": "People already in user's favourites"}), 400
            # Agrega el nuevo favorito a la base de datos
        else:
            new_favourite_people = Favourite(name="Nombre del favorito", 
                                    id_user=user_id, 
                                    id_peoples=people_id, 
                                    id_planets=None, 
                                    id_vehicles=None
                                    )
            
            db.session.add(new_favourite_people)
            db.session.commit()

            return jsonify({"msg": f"People {people_id} se agrego a favoritos del usuario {user_id} "}), 201

    return jsonify({"msg": "No se pudo agregar nada"}), 404

# DELETE FAVORITE PEOPLE FROM USER ❌🎇👨‍💼
@app.route('/users/<int:user_id>/favourites/people/<int:people_id>', methods=['DELETE'])
def delete_user_favourite_people(user_id, people_id):
    # user exist ?
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # people exist ?
    people = People.query.get(people_id)
    if people:
        # people exist in user-favourite?
        existing_favourite = Favourite.query.filter_by(id_user=user_id, id_peoples=people_id).first()
        if existing_favourite:
            db.session.delete(existing_favourite)
            db.session.commit()
            return jsonify({"msg": f"People {people_id} removed from user's favorites {user_id}"}), 200
        else:
            return jsonify({"msg": "People no exist in user's favourites"}), 400

    return jsonify({"msg": "No se pudo eliminar nada"}), 404

# DELETE FAVORITE PLANET FROM USER ❌🎇🪐
@app.route('/users/<int:user_id>/favourites/planet/<int:planet_id>', methods=['DELETE'])
def delete_user_favourite_planet(user_id, planet_id):
    # user exist ?
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # planet exist ?
    planet = Planet.query.get(planet_id)
    if planet:
        # planet exist in user-favourite?
        existing_favourite = Favourite.query.filter_by(id_user=user_id, id_planets=planet_id).first() # id_planet de la entidad, planet_id de los que nos llega
        if existing_favourite:
            db.session.delete(existing_favourite)
            db.session.commit()
            return jsonify({"msg": f"Planet {planet_id} removed from user's favorites {user_id}"}), 200
        else:
            return jsonify({"msg": "Planet no exist in user's favourites"}), 400

    return jsonify({"msg": "No se pudo eliminar nada"}), 404

# /signup	<Signup>	Renderizar formulario de registro ✅
# /login	<Login>	Renderizar formulario de Inicio de sesión ✅
# /private	<Private>	Validar que solo ingresen usuarios autenticados y renderizar este componente EN FAV ✅

# SIGNUP NEW USER ✔ TODO >> verificar si ya existe mail
@app.route('/signup', methods=['POST'])
def signup():
    request_body = request.get_json(force=True)
     
    new_user = User(username=request_body["username"],
                    email = request_body["email"], 
                    password = request_body["password"],
                    is_active = request_body["is_active"]
                    )

    db.session.add(new_user)
    db.session.commit()
   
    return { "msg": "Usuario creado con éxito",
            "response": new_user.serialize(),
            }

# LOGIN  ✔
@app.route('/login', methods=['POST'])
def login():

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    login_user = User.query.filter_by(email=email).first()
    # user email exist ?
    if not login_user:
        return jsonify({"msg": "User not found"}), 404
    
    if email != login_user.email or password != login_user.password:
        return jsonify({"msg": "Incorrect login"})
    
    # pasamos el id para poder usarlo en >>>  get_jwt_identity()
    access_token = create_access_token(identity=login_user.id) 

    response_body = { "access_token": access_token,
                    "user": login_user.serialize()
                    }
    
    return jsonify(response_body)


@app.route("/valid-token", methods=["GET"])
@jwt_required
def valid_token():
    current_user = get_jwt_identity()
    return jsonify({"is_logged":True}), 200

# TEST 
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# TEST ADD FAVOURITE PLANET 🎇🪐  WITH THE FRONT ID PLANET
@app.route('/users/<int:user_id>/favouritesfront/planet/<int:planet_id>', methods=['POST'])
def add_user_favourite_planet_with_front_id(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

   
    existing_favourite = Favourite.query.filter_by(id_user=user_id, id_planets=planet_id).first()
    
    if existing_favourite:
        return jsonify({"msg": "Planet already in user's favourites"}), 400
            # Agrega el nuevo favorito a la base de datos
    else:
        new_favourite_planet = Favourite(name="Nombre del favorito", 
                                    id_user=user_id, 
                                    id_peoples=None, 
                                    id_planets=planet_id, 
                                    id_vehicles=None
                                    )
            
        db.session.add(new_favourite_planet)
        db.session.commit()

        return jsonify({"msg": f"Planeta {planet_id} se agrego a favoritos del usuario {user_id} "}), 201

    






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
