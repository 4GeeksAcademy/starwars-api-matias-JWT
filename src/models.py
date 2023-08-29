from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # Relationships 1 a 1 con Favourite
    favourites = db.relationship('Favourite', backref='user', lazy=True) # NO ES 1 a 1

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    # Relationships 1 a 1 con User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='favorite', uselist=False) # de rodrigo, sino me queda de 1 user a n favourite

    # Relationship 1 a n con People, Planet, Vehicle, Starship
    id_peoples = db.relationship('People', backref='favourite', lazy=True)
    id_planets = db.relationship('Planet', backref='favourite', lazy=True)
    id_vehicles = db.relationship('Vehicle', backref='favourite', lazy=True)
    # id_starships = db.relationship('Starship', backref='favourite', lazy=True) # TODO 
    
    def __repr__(self):
        return '<Favourite %r>' % self.id
    
    def serialize(self):
        return {
            "name": self.name
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

    # Relationships n a 1 con Favourite
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourite.id'),nullable=True)
    #user = db.relationship('User') # forma Rodri

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "height": self.name,
            "mass": self.name,
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

    # Relationships n a 1 con Favourite
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourite.id'),nullable=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        return {
            "name" : self.name,
            "model" : self.model,
            "manufacturer" : self.manufacturer,
            "cost_in_credits" : self.cost_in_credits,
            "length" : self.length,
            "speed" : self.speed,
            "crew" : self.crew,
            "cargo_capacity" : self.namcargo_capacitye,
            "consumables" : self.consumables,
            "vehicle_class" : self.vehicle_class
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.Float(50), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)

    # Relationships n a 1 con Favourite
    favourite_id = db.Column(db.Integer, db.ForeignKey('favourite.id'),nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "name" : self.name,
            "rotation_period" : self.rotation_period,
            "orbital_period" : self.orbital_period,
            "diameter" : self.diameter,
            "climate" : self.climate,
            "gravity" : self.gravity,
            "terrain" : self.terrain,
            "surface_water" : self.surface_water,
            "population" : self.population
        }