import os
from random import choice, randint
from datetime import datetime

import requests
import crud
import model
import server

os.system("dropdb gardens")
os.system("createdb gardens")

model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()

for n in range(10):
    email = f'user{n}@test.com'  
    username = f'user{n}'
    password = 'test'

    new_user = crud.create_user(email, username, password)
    model.db.session.add(new_user)

response = requests.get("https://perenual.com/api/species-list?key=sk-HbCe6538426d9ecb42677")
thirty_plants = response.json()

for plant in thirty_plants['data']:
    plant_name = plant['common_name']
    watering = plant['watering']
    sunlight = plant['sunlight'][0]
    cycle = plant['cycle']
    if plant['default_image']:
        image = plant['default_image'].get('original_url', 'https://easydrawingguides.com/wp-content/uploads/2020/11/Potted-Plant-Step-10.png')
        thumbnail = plant['default_image'].get('thumbnail', 'https://easydrawingguides.com/wp-content/uploads/2020/11/Potted-Plant-Step-10.png')
    else:
        image = 'https://easydrawingguides.com/wp-content/uploads/2020/11/Potted-Plant-Step-10.png'
        thumbnail = 'https://easydrawingguides.com/wp-content/uploads/2020/11/Potted-Plant-Step-10.png'

    new_plant = crud.create_plant(plant_name, watering, sunlight, image, thumbnail, cycle)
    model.db.session.add(new_plant)

model.db.session.commit()



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

