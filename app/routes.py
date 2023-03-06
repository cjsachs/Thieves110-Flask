from flask import render_template, request, flash, redirect, url_for
import requests
from app.forms import LoginForm, RegisterForm, EditProfileForm
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

# ROUTES SECTION
@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')



@app.route('/students', methods=['GET'])
@login_required
def students():
    my_students = ['Student 1', 'Student 2', 'Student 3']
    return render_template('students.html', my_students=my_students)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        
        # Query user from db
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully Logged In! Welcome back, {queried_user.first_name}!', 'success')            
            return redirect(url_for('home'))
        else:
            error = 'Incorrect Email/Password!'
            flash(f'{error}', 'danger')
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)



@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'warning')
        return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our form data and storing into a dict
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }

        # Create instance of User
        new_user = User()

        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save user to database
        new_user.save_to_db()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():

        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower()
        }

        # query current user from db to change
        queried_user = User.query.filter_by(email=new_user_data['email']).first()

        # check if queried_user already exists
        if queried_user:
            flash('Email is already in use.', 'danger')
            return redirect(url_for('edit_profile'))
        else:
           # add changes to db
           current_user.from_dict(new_user_data)
           current_user.save_to_db()
           flash('Profile Updated!', 'success')
           return redirect(url_for('home'))

    return render_template('edit_profile.html', form=form)



@app.route('/ergast', methods=['GET', 'POST'])
@login_required
def ergast():
    print(request.method)
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('rnd')
        print(year, rnd)
        url = f'http://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            standings_data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            new_driver_data = []
            for driver in standings_data:
                driver_dict = {
                    'first_name': driver['Driver']['givenName'],
                    'last_name': driver['Driver']['familyName'],
                    'DOB': driver['Driver']['dateOfBirth'],
                    'wins': driver['wins'],
                    'team': driver['Constructors'][0]['name']
                }
                new_driver_data.append(driver_dict)
            return render_template('ergast.html', new_driver_data=new_driver_data)
        else:
            error = 'That year or round does not exist.'    
            return render_template('ergast.html', error=error)
    return render_template('ergast.html')