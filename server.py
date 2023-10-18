"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud


app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/users', methods=['POST'])
def register_user():
    '''registers a user'''
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if user:
        flash('A user with that email already exists. Please log in or try a different email.')
    else:
        db.session.add(crud.create_user(email, password))
        db.session.commit()
        flash('Your account was created. Please log in.')

    return redirect('/')



@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if user:
        if password == user.password:
            session['user'] = user.user_id
            flash('Logged in!')
            return redirect('/')
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
    return render_template("plant_details.html", plant=plant)


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
    user_id = crud.get_user_by_id(session['user'])

    db.session.add(crud.create_garden(title, description, user_id))
    db.session.commit()

    flash('garden successfully created.')
    
    return redirect('/profile')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)



