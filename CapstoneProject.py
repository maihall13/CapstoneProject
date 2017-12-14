import sqlite3

from flask import Flask, render_template, request, g, redirect, url_for, session
from flask_login import login_user, logout_user, LoginManager, login_required, current_user
import Geocoding
import Weather
import datetime
import AlchemyOutlook
app = Flask(__name__)
import Database
import flask_login
@app.route('/')
def home():
    active = Database.ActiveUser()
    id = active.getActiveUser()
    if id == "None":
        logstate = False
        return render_template("home.html", logstate = logstate,  formname="home.html")
    else:
        logstate = True
        return render_template("home.html", logstate = logstate, formname="home.html")

@app.route('/about')
def about():
    active = Database.ActiveUser()
    id = active.getActiveUser()
    if id == "None":
        logstate = False
        return  render_template("about.html", logstate = logstate, formname="about.html" )
    else:
        logstate = True
        return  render_template("about.html", logstate = logstate, formname="about.html" )


@app.route('/contact')
def contact():
    active = Database.ActiveUser()
    id = active.getActiveUser()
    if id == "None":
        logstate = False
        return  render_template("contact.html", logstate = logstate, formname = "contact.html")
    else:
        logstate = True
        return  render_template("contact.html", logstate = logstate, formname = "contact.html")

@app.route('/logout')
def logout():
    active = Database.ActiveUser()
    active.removeActiveUser(active.getActiveUser())
    active.closeDatabase()
    logstate=False
    return render_template("home.html", logstate = logstate, formname="home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['pagename']
        email = request.form['email']
        user = Database.Users()
        is_email = user.checkEmail(email)
        if is_email == "None":
            user.closeDatabase()
            error = "Enter a valid email address"
            return render_template(str(name), signuperror=True, error=error)
        else:
            logstate = True
            id = user.getUserInfoEmail(user_email=email)[0][0]
            user.closeDatabase()
            active = Database.ActiveUser()
            active.setActiveUser(id)
            active.closeDatabase()
            return render_template(str(name),logstate = logstate)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route('/confirmed', methods=['GET', 'POST'])
def confirmed():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        user = Database.Users()
        user.addUser(user_email=email, user_password=password,user_name=name)
        id = user.getUserInfoEmail(user_email=email)[0][0]
        info = user.getUserInfoID(user_id=id)
        user.closeDatabase()
        active = Database.ActiveUser()
        active.setActiveUser(user_id=id)
        active.closeDatabase()


        return render_template("profile.html", info = info)

@app.route('/profile')
def profile():
    active = Database.ActiveUser()
    id = active.getActiveUser()
    active.closeDatabase()
    user = Database.Users()
    info = user.getUserInfoID(user_id=id)
    logstate = True

    return render_template("profile.html", info = info, logstate=logstate)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        active = Database.ActiveUser()
        id = active.getActiveUser()
        logstate = ""
        if id == "None":
            logstate = False
        else:
            logstate = True
        location = request.form['search']
        value = request.form['Gender']

        geocode = Geocoding.Geocoding()
        latlon = geocode.getLocation(location)
        lat = str(latlon["lat"])
        long = str(latlon["lng"])

        weather = Weather.Weather()
        weather.getAllInfo(lat, long)
        day = datetime.datetime.now().strftime("%A")
        t = datetime.datetime.now().time().strftime("%I:%M %p")
        date = str(day) + " " + str(t)
        description = weather.getDescription()  # "Mostly Cloudy"
        description_list = description.split(" ")
        new_description = ""
        for word in description_list:
            word = word[0:1].upper() + word[1:]
            new_description = new_description + word + " "
        description = new_description

        current = weather.getCurrent()
        high = weather.getHigh()  # "58 F"
        low = weather.getLow()  # "39 F"
        humidity = weather.getHumidity()  # "55%"
        wind = weather.getWind()  # "20 mph"
        icon = weather.getIcon()

        if value == "Men":
            alchemy = AlchemyOutlook.Alchemy(location, value)
            pictures = alchemy.getPictures()
            return render_template("search.html", location=location.upper(), date=date, description=description,
                               current=current, high=high, low=low, humidity=humidity, wind=wind, icon=icon, pictures=pictures, logstate=logstate)

        elif value == "Women":
            alchemy = AlchemyOutlook.Alchemy(location, value)
            pictures = alchemy.getPictures()
            return render_template("search.html", location=location.upper(), date=date, description=description,
                               current=current, high=high, low=low, humidity=humidity, wind=wind, icon=icon, pictures=pictures, logstate=logstate)

        else:
            return render_template("search.html", test=value, t=t)

if __name__ == '__main__':

   # user = Database.Users()
   # check = user.checkEmail("maiahall1396")
    #print(check)
    #print(type(check))
    #user.addUser(user_email="maiahall1396@gmail.com", user_password="123Hello",user_name="Maia")
    #print(user.getAllUsers())
    #user.deleteUser(user_id=1)
    #user.deleteUser(user_id=2)

    #print(user.getAllUsers())
    #user.addUser(user_email="maiahall1396@gmail.com", user_password="123Hello",user_name="Maia")
    #user.addUser(user_email="hall53211@gmail.com", user_password="123Hello",user_name="Maia")
    #print(user.getUserInfo(user_email="maiahall1396@gmail.com"))


    #active = Database.ActiveUser()
    #print(active.getActiveUser())
    #active.removeActiveUser(3)
    #print(active.getActiveUser())

    app.run()
