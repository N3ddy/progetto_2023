from flask import render_template, url_for, redirect, flash, session
from flaskr.forms import RegistrationForm, LoginForm
from flaskr.models import User
from flaskr import db, bcrypt
from flaskr import app, socketio
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import join_room, send, rooms


active_rooms = {}


# controllo dell evento nel socket
@socketio.on('change_color')
def test(color):
    print(rooms(), flush=True)
    send(color, to=active_rooms[current_user.username])


@socketio.on('join')
def on_join(data):
    username = current_user.username
    room = username + "_" + data['room']
    active_rooms[username] = room
    join_room(room)
    print("created room " + room, flush=True)
    send(username + ' has entered the room: ' + room, to=room)
    socketio.emit("load_avaiable_rooms", active_rooms, broadcast=True)


@socketio.on('enter_existing_room')
def on_enter_existing_room(data):
    username = current_user.username
    room = active_rooms[data["username"]]
    join_room(room)
    
    active_rooms[username] = room #to revise it
    print("entered room " + room, flush=True)
    
    send(username + ' has entered the room: ' + room, to=room)
    socketio.emit("load_avaiable_rooms", active_rooms, broadcast=True)

#send the avaiable room when a new user enter the page
@socketio.on("startInfo")
def connect():
    socketio.emit("setup", active_rooms)




# route per la home page e la pagina "About"
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

# route per la pagina dell'account
@app.route("/logout/")
@login_required
def log_out_user():
    logout_user()
    return render_template("home.html", title="Home Page")


# route per la pagina game
@app.route("/game/")
@login_required
def coming_soon():
    return render_template("game.html", title="Coming Soon!", username=current_user.username)
