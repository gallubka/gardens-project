import requests
import model
import crud


response = requests.get("https://perenual.com/api/species-list?key=sk-HbCe6538426d9ecb42677")

#print(response.status_code)
thirty_plants = response.json()

#print(thirty_plants['data'])

#for plant in thirty_plants['data']:
    #print(plant)

one_plant = {'id': 1, 
             'common_name': 'European Silver Fir', 
             'scientific_name': ['Abies alba'], 
             'other_name': ['Common Silver Fir'], 
             'cycle': 'Perennial', 
             'watering': 'Frequent', 
             'sunlight': ['full sun'], 
             'default_image': {'license': 45, 
                               'license_name': 'Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)', 
                               'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/deed.en', 
                               'original_url': 'https://perenual.com/storage/species_image/1_abies_alba/og/1536px-Abies_alba_SkalitC3A9.jpg', 
                               'regular_url': 'https://perenual.com/storage/species_image/1_abies_alba/regular/1536px-Abies_alba_SkalitC3A9.jpg', 
                               'medium_url': 'https://perenual.com/storage/species_image/1_abies_alba/medium/1536px-Abies_alba_SkalitC3A9.jpg', 
                               'small_url': 'https://perenual.com/storage/species_image/1_abies_alba/small/1536px-Abies_alba_SkalitC3A9.jpg', 
                               'thumbnail': 'https://perenual.com/storage/species_image/1_abies_alba/thumbnail/1536px-Abies_alba_SkalitC3A9.jpg'}}
#print(one_plant)


#def create_plant(name, watering, light_preference, image, thumbnail, plant_type):

new_plant = crud.create_plant(one_plant['common_name'], one_plant['watering'], one_plant['sunlight'][0], one_plant['default_image']['original_url'], one_plant['default_image']['thumbnail'], one_plant['cycle'])

new_plants = []

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
    new_plants.append(new_plant)

#print(new_plants)



base_url = 'https://perenual.com/api/species-list?key=sk-HbCe6538426d9ecb42677'

search_term = 'onstera'

response2 = requests.get(base_url + f'&q={search_term}')
plant_results = response2.json()

for plant in plant_results['data']:
    print(plant['common_name'])

#print(plant_results['data'][0]['common_name'])

#print(plant_results.keys())

# >>> payload = {'term': 'wow very long',
# ...            'filter': 'very long',
# ...            'user': 'whoa dudette'}

# >>> req = requests.get('https://fakeapi.code/search', params=payload)
# >>> print(req.url)

# payload = {}
# headers = {}

#response = requests.request("", url, headers=headers, data=payload)

#print(response.text)


#if search term is empty, dont call api
#else call api with url+search term

#checkbox for filter, if checked append to url 