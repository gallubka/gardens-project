"""Models for garden app."""

from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


class User(db.Model):
    """a user"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    email = db.Column(db.String, unique=True)

    password = db.Column(db.String)

    google_account = db.Column(db.String)

    gardens = db.relationship("Garden", back_populates="creator")
    #creator = db.relationship("User", back_populates="gardens")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Plant(db.Model):
    """a plant """
    __tablename__ = 'plants'

    plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String)

    watering = db.Column(db.String) 

    image = db.Column(db.String)

    thumbnail = db.Column(db.String)

    light_preference = db.Column(db.String)

    plant_type = db.Column(db.String)

    garden_plants = db.relationship("GardenPlants", back_populates="plant")


    places = db.relationship("Places", secondary="native_to", back_populates="plants")

    def __repr__(self):
        return f'<Plant plant_id={self.plant_id} name={self.name}>, type={self.plant_type}'


class Garden(db.Model):
    """a garden"""
    __tablename__ = 'gardens'

    garden_id = db.Column(db.Integer, autoincrement=True, primary_key=True )

    title = db.Column(db.String)

    description = db.Column(db.String)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    creator = db.relationship("User", back_populates="gardens")

    garden_plants = db.relationship("GardenPlants", back_populates="garden")

    reminders_enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Garden garden_id={self.garden_id} creator={self.creator}>'


    

class GardenPlants(db.Model):
    """a plant in a garden"""
    __tablename__ = 'gardenplants'

    garden_plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    garden_id = db.Column(db.Integer,
                    db.ForeignKey('gardens.garden_id'))
    
    plant_id = db.Column(db.Integer,
                    db.ForeignKey('plants.plant_id'))

    garden = db.relationship("Garden", back_populates="garden_plants") 

    plant = db.relationship("Plant", back_populates="garden_plants")

    def __repr__(self):
        return f'<Gardenplant garden_plant_id={self.garden_plant_id} garden={self.garden} plant={self.plant}>'
    

    
class NativeTo (db.Model):
    """where a plant is native to"""
    __tablename__ = 'native_to'

    native_to_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    plant_id = db.Column(db.Integer, db.ForeignKey("plants.plant_id"))

    place_id = db.Column(db.Integer, db.ForeignKey("places.place_id"))

#test_user = User(email='test@test.test', password='test')

class Places (db.Model):
    """places where a plant can be native to"""
    __tablename__ = "places"

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    country = db.Column(db.String)

    region = db.Column(db.String)

    plants = db.relationship("Plant", secondary="native_to", back_populates="places")


# Replace this with your code!


def connect_to_db(flask_app, db_uri="postgresql:///gardens", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
