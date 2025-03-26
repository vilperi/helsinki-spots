import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import spots


app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_spots = spots.get_spots()

    return render_template("index.html", spots=all_spots)

@app.route("/spot/<int:spot_id>")
def show_spot(spot_id):
    spot = spots.get_spot(spot_id)
    return render_template("/show_spot.html", spot=spot)

@app.route("/add")
def add():
    return render_template("add_spot.html")

@app.route("/add_spot", methods=["POST"])
def add_spot():
    # Get coordinates as float
    lat = request.form["lat"]
    lon = request.form["lon"]

    name = request.form["name"]
    category = request.form["category"]
    comment = request.form["comment"]
    user_id = int(session["user_id"])

    spots.add_spot(name, lat, lon, category, user_id, comment)

    return redirect("/")

@app.route("/edit_spot/<int:spot_id>")
def edit_spot(spot_id):
    spot = spots.get_spot(spot_id)
    return render_template("edit_spot.html", spot=spot)

@app.route("/update_spot", methods=["POST"])
def update_spot():
    # Get coordinates as float
    lat = request.form["lat"]
    lon = request.form["lon"]

    name = request.form["name"]
    category = request.form["category"]
    spot_id = request.form["spot_id"]

    spots.update_spot(spot_id, name, lat, lon, category)

    return redirect("/spot/" + str(spot_id))

@app.route("/remove_spot/<int:spot_id>", methods=["GET", "POST"])
def remove_spot(spot_id):
    if request.method == "GET":
        spot = spots.get_spot(spot_id)
        return render_template("remove_spot.html", spot=spot)

    if request.method == "POST":
        if "remove" in request.form:
            spots.remove_spot(spot_id)
            return redirect("/")
        return redirect("/spot/" + str(spot_id))

@app.route("/register")
def register():
    return render_template("register.html")

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