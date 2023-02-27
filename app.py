from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    # return '<h1>This is the Thieves-110 Home Page.</h1>'

@app.route('/students', methods=['GET'])
def students():
    my_students = ['Student 1', 'Student 2', 'Student 3']
    return render_template('students.html', my_students=my_students)

@app.route('/ergast', methods=['GET', 'POST'])
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