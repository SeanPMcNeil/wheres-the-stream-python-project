from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/register/user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/login')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash(u"Invalid Email", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash(u"Invalid Password", "login")
        return redirect('/login')

    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash(u"You must be logged in to view the dashboard", "login")
        return redirect('/')

    if 'query' in session:
        session.pop('query')
    if 'results' in session:
        session.pop('results')
    if 'one_result' in session:
        session.pop('one_result')

    data = {
        'user_id' : session['user_id']
    }

    user = User.get_by_id(data)
    favorites = Movie.get_favorites(data)

    print(user)
    return render_template("dashboard.html", user = user, favorites = favorites)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/edituser/<int:id>")
def edit_user(id):
    data = {
        'user_id' : id
    }
    user = User.get_by_id(data)
    return render_template("edit_user.html", user = user)

@app.route("/edituser/<int:id>/processing", methods=['POST'])
def process_edit(id):
    data = {
        "user_id" : id,
        "username" : request.form['username'],
        "email" : request.form['email']
    }

    User.update_user(data)

    return redirect("/dashboard")