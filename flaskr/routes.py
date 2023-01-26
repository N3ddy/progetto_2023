# Preparazione Lezione 5
from flask import render_template, url_for, redirect, flash
from flaskr import app, db, bcrypt
#from myflaskblog.forms import RegistrationForm, LoginForm
#from myflaskblog.models import User
from flask_login import login_user, logout_user, current_user, login_required

# indirizzo per la home page
@app.route("/")
@app.route("/home")
def home():
    # Reindirizzamento del template home.html con il titolo "Home Page" e i post
    return render_template("home.html", title="Home Page")
