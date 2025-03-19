import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config


app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add")
def add():
    return render_template("add_spot.html")

@app.route("/create_user", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")


@app.route("/add_spot", methods=["POST"])
def add_spot():
    # Get coordinates as float
    lat = request.form["lat"]
    lon = request.form["lon"]

    name = request.form["name"]
    category = request.form["category"]
    comment = request.form["comment"]
    user_id = int(session["user_id"])
    
    try:
        sql = "INSERT INTO spots (name, lat, lon, category, user_id) VALUES (?, ?, ?, ?, ?)"
        db.execute(sql, [name, lat, lon, category, user_id])
    except sqlite3.IntegrityError:
        return "VIRHE: Kohdetta ei voitu luoda"
    
    try:
        spot_id = db.last_insert_id()
        sql = "INSERT INTO comments (content, sent_at, user_id, spot_id) VALUES (?, datetime('now'), ?, ?)"
        db.execute(sql, [comment, user_id, spot_id])
    except sqlite3.IntegrityError:
        return "VIRHE: Kommentin jättö ei onnistunut"

    return redirect("/")