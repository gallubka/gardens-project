import os
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb gardens")
os.system("createdb gardens")

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    new_user = crud.create_user(email, password)
    model.db.session.add(new_user)


for n in range(10):
    name = f'plant{n}'
    humidity_preference = n
    light_preference = n
    temperature_preference = "10-20 C"
    plant_type = "vegetable"

    new_plant = crud.create_plant(name, humidity_preference, light_preference, temperature_preference, plant_type)
    model.db.session.add(new_plant)

for n in range(10):
    country = f"France{n}"
    region = f"Northern{n}"

    new_place = crud.create_place(country, region)
    model.db.session.add(new_place)

model.db.session.commit()

#code here NativeTo
for n in range(10):
    new_native_to = crud.create_native_to(n+1, n+1)
    model.db.session.add(new_native_to)

model.db.session.commit()

#gardens

for n in range (10):
    title = f'garden title {n}'
    description = f"test garden description number {n}."
    user_id = n+1

    new_garden = crud.create_garden(title, description, user_id) 
    model.db.session.add(new_garden)


model.db.session.commit()

#gardenplants

for n in range (10):
    garden = crud.get_garden_by_id(n+1)
    plant = crud.get_plant_by_id(n+1)

    new_gareden_plant = crud.create_garden_plant(garden.garden_id, plant.plant_id)
    model.db.session.add(new_gareden_plant)
    

model.db.session.commit()

