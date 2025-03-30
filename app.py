import sqlite3

from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

import db
import config
import spots


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_spots = spots.get_spots()

    return render_template("index.html", spots=all_spots)

@app.route("/find_spot")
def find_spot():
    query = request.args.get("query")
    if query:
        results = spots.find_spots(query)
    else:
        query = ""
        results = []
    return render_template("find_spot.html", query=query, results=results)

@app.route("/spot/<int:spot_id>")
def show_spot(spot_id):
    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)
    comments = spots.get_comments(spot_id)
    return render_template("/show_spot.html", spot=spot, comments=comments)

@app.route("/add_spot")
def add_spot():
    require_login()
    return render_template("add_spot.html")

@app.route("/create_spot", methods=["POST"])
def create_spot():
    require_login()

    lat = request.form["lat"]
    lon = request.form["lon"]
    name = request.form["name"]
    description = request.form["description"]
    category = request.form["category"]
    user_id = int(session["user_id"])

    spots.add_spot(name, lat, lon, description, category, user_id)

    return redirect("/")

@app.route("/edit_spot/<int:spot_id>")
def edit_spot(spot_id):
    require_login()
    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)
    if spot["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_spot.html", spot=spot)

@app.route("/update_spot", methods=["POST"])
def update_spot():
    require_login()
    spot_id = request.form["spot_id"]
    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)
    if spot["user_id"] != session["user_id"]:
        abort(403)

    lat = request.form["lat"]
    lon = request.form["lon"]
    name = request.form["name"]
    description = request.form["description"]
    category = request.form["category"]

    spots.update_spot(spot_id, name, lat, lon, description, category)

    return redirect("/spot/" + str(spot_id))

@app.route("/remove_spot/<int:spot_id>", methods=["GET", "POST"])
def remove_spot(spot_id):
    require_login()
    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)
    if spot["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_spot.html", spot=spot)

    if request.method == "POST":
        if "remove" in request.form:
            spots.remove_spot(spot_id)
            return redirect("/")
        return redirect("/spot/" + str(spot_id))

@app.route("/add_comment", methods=["POST"])
def add_comment():
    require_login()
    spot_id = request.form["spot_id"]
    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)

    content = request.form["content"]
    user_id = session["user_id"]

    spots.add_comment(content, user_id, spot_id)


    return redirect("/spot/" + str(spot_id))

@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    require_login()

    comment = spots.get_comment(comment_id)
    if not comment:
        abort(404)
    spot_id = comment["spot_id"]
    if comment["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("edit_comment.html", comment=comment)
    if request.method == "POST":
        if "edit" in request.form:
            content = request.form["content"]
            spots.edit_comment(comment_id, content)
        return redirect("/spot/" + str(spot_id))

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment = spots.get_comment(comment_id)
    if not comment:
        abort(404)
    spot_id = comment["spot_id"]

    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)

    if request.method == "POST":
        if "remove" in request.form:
            spots.remove_comment(comment_id)
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
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")