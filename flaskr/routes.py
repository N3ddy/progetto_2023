# Preparazione Lezione 5
from flask import render_template, url_for, redirect, flash
#from myflaskblog.forms import RegistrationForm, LoginForm
#from myflaskblog.models import User
from flask_login import login_user, logout_user, current_user, login_required

"""# route per la home page e la pagina "About"
@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html", title="Home Page")

@app.route("/info/")
def about():
    return render_template("info.html", title="Info Page")

# route per la pagina di login
@app.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        candidate = form.password.data
        if user and bcrypt.check_password_hash(user.password, candidate):
            login_user(user, remember=form.remember_me.data)
            flash('Benvenuto', category='success')
            return redirect('/home/')

        else:
            flash('Email o password sbagliate', category='danger')
            return redirect('/login/')
    else:
        return render_template("login.html", title="Login Page", form=form)
# route per la pagina di registrazione
@app.route("/register/", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=form.username.data,
                    password=pw_hash,
                    email=form.email.data)
        with app.app_context():

            db.session.add(user)
            db.session.commit()

        flash(
            f"Il tuo account e' stato creato {form.username.data}", category="success")
        return redirect('/login/')

    return render_template("register.html", title="Pagina di Registrazione", form=form)
# route per la pagina dell'account
@app.route("/account/")
@login_required
def account():
    return render_template("account.html", title="Pagina dell'Account", p_bucks=current_user.p_bucks)

# route per la pagina game
@app.route("/game/")
def coming_soon():
    return render_template("game.html", title="Coming Soon!")"""

