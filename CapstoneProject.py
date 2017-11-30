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

    return render_template("home.html", logstate = logstate)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form['search']
        test = "\\udc4c \\ud83d \\udeab \\u2714 \\ufe0f"

        return render_template("search.html", location=location, test = test)

if __name__ == '__main__':
    app.secret_key = "what"
    app.run()
