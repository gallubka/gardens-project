"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud
import requests


app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    if 'user' not in session:
        session['logged_in'] = False
    print(f'homepage, THIS IS SESSION LOGGED IN : {session["logged_in"]}')
    return render_template('homepage.html')

@app.route('/users', methods=['POST'])
def register_user():
    '''registers a user'''
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if user:
        flash('A user with that email already exists. Please log in or try a different email.')
    elif email and password:
        db.session.add(crud.create_user(email, username, password))
        db.session.commit()
        flash('Your account was created. Please log in.')
    else: 
        flash('Please enter an email and a password to create an account.')

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if user:
        if password == user.password:
            session['user'] = user.user_id
            session['logged_in'] = True
            print(f'login, THIS IS SESSION LOGGED IN : {session["logged_in"]}')
            flash('Logged in!')
            return redirect('/profile')
        else: 
            flash('Wrong password. Please try again.')
            return redirect('/')
    else:
        flash('There is no user with this email. Please try again or register.')
        return redirect('/')
    
    
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Successffully loggedd out.')
    return redirect('/')
    

@app.route('/profile')
def profile():
    if 'user' in session:
        user = crud.get_user_by_id(session['user'])
        return render_template('profile.html', user=user)
    else:
        flash('Please log in first.')
        return redirect('/')



@app.route('/plants')
def plants():
    """view all plants"""

    plants = crud.get_plants()

    return render_template('plants.html', plants=plants) 


@app.route('/plants/<plant_id>')
def plant_details(plant_id):
    """Show details of a plant."""
    plant = crud.get_plant_by_id(plant_id)
    gardens = crud.get_my_gardens(session['user'])

    return render_template("plant_details.html", plant=plant, gardens=gardens)


@app.route('/add-plant-to-garden', methods=['POST'])
def add_plant_to_garden():
    plant_id = request.form.get('plant_id')
    garden = request.form.get('which-garden')
   
    db.session.add(crud.create_garden_plant(garden, plant_id))
    db.session.commit()

    flash('Plant added to garden.')
    return redirect(f'/plants/{plant_id}')
    #save plant to database


@app.route('/gardens')
def gardens():
    """view all gardens"""
    gardens = crud.get_gardens()

    return render_template('gardens.html', gardens=gardens)


@app.route('/gardens/<garden_id>')
def garden_details(garden_id):
    """show details of a garden"""
    garden = crud.get_garden_by_id(garden_id)

    return render_template("garden_details.html", garden=garden)


@app.route('/new-garden', methods=['POST'])
def create_new_garden():
    title = request.form.get('garden_title')
    description = request.form.get('garden_description')


    db.session.add(crud.create_garden(title, description, session['user']))
    db.session.commit()

    flash('garden successfully created.')
    
    return redirect('/profile')

@app.route('/remove-plant-from-garden', methods=['POST'])
def remove_plant_from_garden():
    garden_id = request.form.get('garden_to_remove_from')
    garden_plant_id = request.form.get('remove-plant')
    garden_plant = crud.get_garden_plant_by_id(garden_plant_id)

    db.session.delete(garden_plant)
    db.session.commit()

    return redirect(f'/gardens/{garden_id}')


@app.route('/remove-garden', methods=['POST'])
def remove_garden():
    garden_id = request.form.get('garden_to_remove')
    garden = crud.get_garden_by_id(garden_id)

    db.session.delete(garden)
    db.session.commit()

    flash('Garden successfully deleted!')
    return redirect('/profile')


@app.route('/search_plants', methods=['GET'])
def search_plants():
    search_param = request.args.get('search_plant')
    base_url = 'https://perenual.com/api/species-list?key=sk-HbCe6538426d9ecb42677'
    response2 = requests.get(base_url + f'&q={search_param}')
    plants_result = response2.json()

    our_plants = []

    for plant in plants_result['data']:
        plant_in_database =  crud.get_plant_by_name(plant['common_name'])
        if plant_in_database is not None:
            our_plants.append(plant_in_database)
        else:
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
            db.session.add(new_plant)
            db.session.commit()
            our_plants.append(new_plant)

    set_plants = set(our_plants)
    list_our_plants = list(set_plants)
    
    return render_template('search-results.html', our_plants=list_our_plants)


@app.route('/filter', methods=['GET'])
def filter_plants():
    base_url = 'https://perenual.com/api/species-list?key=sk-HbCe6538426d9ecb42677'
    search_param = ''

    #watering
    if request.form.get("frequent") == True:
        search_param = search_param + '&watering=frequent'
    elif request.form.get("average") == True:
        search_param = search_param + '&watering=average'
    elif request.form.get("minimum") == True:
        search_param = search_param + '&watering=minimum'
    elif request.form.get("none") == True:
        search_param = search_param + '&sunlight=none'
    #sunlight
    elif request.form.get("full_shade") == True:
        search_param = search_param + '&sunlight=full_shade'
    elif request.form.get("part_shade") == True:
        search_param = search_param + '&sunlight=part_shade'
    elif request.form.get("sun-part_shade") == True:
        search_param = search_param + '&sunlight=sun-part_shade'
    elif request.form.get("full_sun") == True:
        search_param = search_param + '&sunlight=full_sun'
    #cycle
    elif request.form.get("perennial") == True:
        search_param = search_param + '&cycle=perennial'
    elif request.form.get("annual") == True:
        search_param = search_param + '&cycle=annual'
    elif request.form.get("biennial") == True:
        search_param = search_param + '&cycle=biennial'
    elif request.form.get("biannual") == True:
        search_param = search_param + '&cycle=biannual'

    response = requests.get(base_url + f'{search_param}')
    plants_result = response.json()
    
    our_plants = []

    for plant in plants_result['data']:
        plant_in_database =  crud.get_plant_by_name(plant['common_name'])
        if plant_in_database is not None:
            our_plants.append(plant_in_database)
        else:
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
            db.session.add(new_plant)
            db.session.commit()
            our_plants.append(new_plant)

    set_plants = set(our_plants)
    list_our_plants = list(set_plants)
    
    return render_template('search-results.html', our_plants=list_our_plants)

    



@app.route('/change_username', methods=['POST'])
def change_username():
    new_username = request.json.get('new_username')
    user_id = request.json.get('user_id')
   
    user = crud.get_user_by_id(int(user_id))

    user.username = new_username
    
    db.session.commit()
   
    return jsonify({'msg': 'Successfully changed!', 'newname': new_username})



if __name__ == '__main__':
    connect_to_db(app)
    app.app_context().push()
    app.run(host='0.0.0.0', debug=True)



