"""CRUD operations."""

from model import db, User, Garden, Plant, GardenPlants, NativeTo, Places, connect_to_db


# Functions start here!
def create_user(email, username, password):
    """Create and return a new user."""

    user = User(email=email, username=username, password=password)
    return user


def create_plant(name, watering, light_preference, image, thumbnail, plant_type):
    """create and return a plant"""
    plant = Plant(name=name, 
                  watering=watering,
                  light_preference=light_preference,
                  image=image,
                  thumbnail=thumbnail,
                  plant_type=plant_type)
    return plant

def get_plants():
    return Plant.query.all()

def create_place(country, region):
    """creates a place"""
    place = Places(country=country, region=region)
    return place

def get_gardens():
    return Garden.query.all()

def get_my_gardens(user_id):
    return Garden.query.filter(user_id == Garden.creator_id).all()

def all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    user = User.query.filter(User.email == email).first()
    return user

def get_garden_by_id(garden_id):
    return Garden.query.get(garden_id)

def get_plant_by_id(plant_id):
    return Plant.query.get(plant_id)

def get_place_by_id(place_id):
    return Places.query.get(place_id)

def get_garden_plant_by_id(garden_plant_id):
    return GardenPlants.query.get(garden_plant_id)

def create_garden(title, description, user_id):
    """Create and return a garden"""
    garden = Garden(title=title, description=description, creator_id=user_id)
    return garden


def create_native_to(plant_id, place_id):

    native_to = NativeTo( plant_id=plant_id, place_id=place_id)
    return native_to


def create_garden_plant(garden_id, plant_id):
    """create and return a plant in a garden"""
    
    gardenplant = GardenPlants(garden_id=garden_id, plant_id=plant_id)
    return gardenplant


def get_plant_by_name(plant_name): 
    return Plant.query.filter_by(name = plant_name).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)