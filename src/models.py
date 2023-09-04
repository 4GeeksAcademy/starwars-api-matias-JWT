from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ROSINI:
# favoritos n planetas 1
# usuario 1 favoritos n

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # Relationships 1 a n con Favourite
    favourites = db.relationship('Favourite', backref='user', lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)

    # Relationships 1 a n con User, people, planet, vehicle, starship
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    id_peoples = db.Column(db.Integer, db.ForeignKey('people.id'),nullable=True)
    id_planets = db.Column(db.Integer, db.ForeignKey('planet.id'),nullable=True)
    id_vehicles = db.Column(db.Integer, db.ForeignKey('vehicle.id'),nullable=True)
    

    def __repr__(self):
        return '<Favourite %r>' % self.id
    
    def serialize(self):
        return {
            "name": self.name,
            "id_peoples": self.id_peoples,
            "id_planets": self.id_planets,
            "id_vehicles": self.id_vehicles,
        }
      
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer, unique=True, nullable=False)
    mass = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(120), unique=True, nullable=False)
    skin_color = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=True, nullable=False)

    # Relationships 1 a n con Favourite
    favourites = db.relationship('Favourite', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color" : self.hair_color,
            "skin_color" : self.skin_color,
            "eye_color" : self.eye_color,
            "birth_year" : self.birth_year,
            "gender" : self.gender,
            # do not serialize the password, its a security breach
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Float(50), nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    consumables = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250), nullable=False)

    # Relationships 1 a n con Favourite
    favourites = db.relationship('Favourite', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "model" : self.model,
            "manufacturer" : self.manufacturer,
            "cost_in_credits" : self.cost_in_credits,
            "length" : self.length,
            "speed" : self.speed,
            "crew" : self.crew,
            "cargo_capacity" : self.cargo_capacity,
            "consumables" : self.consumables,
            "vehicle_class" : self.vehicle_class,
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODOS EN nulleable=True, PARA PODER GUARDAR TODOS LOS ID QUE VIENEN DEL FRONT DE LA OTRA API.
    name = db.Column(db.String(250), nullable=True) 
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    gravity = db.Column(db.Float(50), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)

    # Relationships 1 a n con Favourite
    favourites = db.relationship('Favourite', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "rotation_period" : self.rotation_period,
            "orbital_period" : self.orbital_period,
            "diameter" : self.diameter,
            "climate" : self.climate,
            "gravity" : self.gravity,
            "terrain" : self.terrain,
            "surface_water" : self.surface_water,
            "population" : self.population,
        }