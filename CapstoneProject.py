from flask import Flask, render_template, request, g, redirect, url_for, session
from flask_login import login_user, logout_user, LoginManager, login_required, current_user



app = Flask(__name__)

#TODO: create a loading screen or figure out how that actually works
@app.route('/')
def home():
    logstate = False
    if session.get('logged_in') == True:
        logstate = True

    return render_template("home.html", logstate = logstate)


if __name__ == '__main__':
    app.secret_key = "what"
    app.run()
