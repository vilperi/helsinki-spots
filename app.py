import secrets
import sqlite3
import markupsafe
import math
import time
from pyproj import Transformer

from flask import Flask, abort, redirect, render_template
from flask import request, session, make_response, flash, g

import db
import config
import spots
import users


app = Flask(__name__)
app.secret_key = config.secret_key

categories = [
    "Arkkitehtuuri & Rakennustaide",
    "Baarit & Klubit",
    "Historialliset kohteet",
    "Hylätyt rakennukset",
    "Kahvilat & Pienpaahtimot",
    "Katutaide & Graffiti",
    "Kirppikset",
    "Kollektiivit & Yhteisöt",
    "Paikka hyvällä näkymällä",
    "Puistot & Hengailupaikat",
    "Skeittauspaikat",
    "Muut"
]

def spot_color(category):
    mapping = {
        "Arkkitehtuuri & Rakennustaide": "#ce7d32",
        "Baarit & Klubit": "#c176ff",
        "Historialliset kohteet": "#CCC057",
        "Hylätyt rakennukset": "#ff8080",
        "Kahvilat & Pienpaahtimot": "#5e4936",
        "Katutaide & Graffiti": "#7ddaff",
        "Kirppikset": "#a3ff7e",
        "Kollektiivit & Yhteisöt": "#6B3F88",
        "Paikka hyvällä näkymällä": "#5c88ff",
        "Puistot & Hengailupaikat": "#51b83c",
        "Skeittauspaikat": "#333333",
        "Muut": "#cccccc"
    }
    return mapping.get(category, "#cccccc")

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 20
    spot_count = spots.count_rows("spots")
    page_count = math.ceil(spot_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    rows = spots.get_spots(page, page_size)
    # convert rows to dicts and attach color
    all_spots = [dict(r) for r in rows]
    for s in all_spots:
        s["color"] = spot_color(s.get("category", "Muut"))
    return render_template("index.html", page=page,
                           page_count=page_count, spots=all_spots)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    user_spots = users.get_spots(user_id)
    comment_count = users.count_comments(user_id)
    if not user:
        abort(404)

    return render_template("/show_user.html", user=user, spots=user_spots,
                           comment_count=comment_count)

@app.route("/find_spot/<int:page>")
def find_spot(page=1):
    page_size = 20
    query = request.args.get("query", "")
    category = request.args.get("category", "")
    results = spots.find_spots(query, category, page, page_size)

    if results:
        spot_count = results[0]["spot_count"]
    else:
        spot_count = 0

    page_count = math.ceil(spot_count / page_size)
    page_count = max(page_count, 1)
    print(page_count)


    found_spots = [dict(r) for r in results]
    for s in found_spots:
        s["color"] = spot_color(s.get("category", "Muut"))

    if page < 1:
        return redirect("/find_spot/1")
    if page > page_count:
        return redirect("/find_spot/" + str(page_count))

    return render_template("find_spot.html", query=query, results=found_spots, category=category,
                           categories=categories, page=page, page_size=page_size, page_count=page_count)

@app.route("/spot/<int:spot_id>/<int:page>")
def show_spot(spot_id, page=1):
    page_size = 10
    comment_count = spots.count_comments(spot_id)
    page_count = math.ceil(comment_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/spot" + "/" + str(spot_id) + "/1")
    if page > page_count:
        return redirect("/spot" + "/" + str(spot_id) + "/" + str(page_count))

    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)
    comments = spots.get_comments(spot_id, page, page_size)
    images = spots.get_images(spot_id)
    return render_template("/show_spot.html", page=page, page_count=page_count,
                           spot=spot, comments=comments, images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = spots.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

def check_coords(coord):
    try:
        coord_flt = float(coord)
        return coord_flt
    except ValueError:
        return None  # Return None if invalid

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    spot_id = request.form["spot_id"]
    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)
    if spot["user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        spots.remove_image(spot_id, image_id)

    return redirect("/edit_spot/" + str(spot_id))

@app.route("/add_spot")
def add_spot():
    require_login()
    return render_template("add_spot.html", categories=categories, errors=None)

def check_images(files, errors: dict):
    for file in files:
        if file:
            if not file.filename.endswith(".png"):
                errors["files"] = "Väärä tiedostomuoto"
            image = file.read()
            if len(image) > 500 * 1024:
                errors["files"] = "Liian iso tiedosto"
            file.seek(0)

def upload_images(files, spot_id):
    for file in files:
        if file:
            image = file.read()
            spots.add_image(image, spot_id)

@app.route("/create_spot", methods=["POST"])
def create_spot():
    require_login()
    check_csrf()

    errors = {}
    if "cancel" in request.form:
        return redirect("/")
    name = request.form["name"]
    lat, lon = request.form["coords"].split(", ")
    print(lon, "Toimiiko? Itäkoordinaatti")
    print(lat, "Toimiiko? Pohjoiskoordinaatti")
    lat = check_coords(lat)
    lon = check_coords(lon)
    description = request.form["description"]
    category = request.form["category"]
    user_id = int(session["user_id"])
    files = request.files.getlist("image")

    if not name or not lat or not lon or not category:
        abort(403)
    if not 60.05 < lat < 60.34:
        users.wrong_coords(user_id)
        errors["lat"] = "Pohjoiskoordinaatti on virheellinen"
    if not 24.55 < lon < 25.22:
        users.wrong_coords(user_id)
        errors["lon"] = "Itäkoordinaatti on virheellinen"
    if len(name) > 50 or len(description) > 1000:
        abort(403)
    if category not in categories:
        abort(403)
    check_images(files, errors)

    if errors:
        flash("Tarkista syöte", "error-message")
        return render_template(
            "add_spot.html",
            categories=categories,
            name=name,
            lat=lat,
            lon=lon,
            description=description,
            category=category,
            errors=errors,
        )

    spots.add_spot(name, lat, lon, description, category, user_id)
    spot_id = db.last_insert_id()
    upload_images(files, spot_id)
    flash("Uusi kohde luotu", "info")
    return redirect("/")

@app.route("/edit_spot/<int:spot_id>")
def edit_spot(spot_id):
    require_login()
    spot = spots.get_spot(spot_id)
    images = spots.get_images(spot_id)
    if not spot:
        abort(404)
    if spot["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_spot.html", spot=spot, categories=categories, images=images, errors=None)

@app.route("/update_spot", methods=["POST"])
def update_spot():
    require_login()
    check_csrf()

    errors = {}
    if "cancel" in request.form:
        return redirect("/")

    spot_id = request.form["spot_id"]
    spot = spots.get_spot(spot_id)
    images = spots.get_images(spot_id)
    if not spot:
        abort(404)
    if spot["user_id"] != session["user_id"]:
        abort(403)

    name = request.form["name"]
    lat, lon = request.form["coords"].split(", ")
    print(lon, "Toimiiko? Itäkoordinaatti")
    print(lat, "Toimiiko? Pohjoiskoordinaatti")
    lat = check_coords(lat)
    lon = check_coords(lon)
    description = request.form["description"]
    category = request.form["category"]
    user_id = int(session["user_id"])
    files = request.files.getlist("image")

    if not name or not lat or not lon or not category:
        abort(403)
    if not 60.05 < lat < 60.34:
        users.wrong_coords(user_id)
        errors["coords"] = "Koordinaatti on virheellinen"
    if not 24.55 < lon < 25.22:
        users.wrong_coords(user_id)
        errors["coords"] = "Koordinaatti on virheellinen"
    if len(name) > 50 or len(description) > 1000:
        abort(403)
    if category not in categories:
        abort(403)
    check_images(files, errors)

    if errors:
        flash("Tarkista syöte", "error-message")
        return render_template(
            "edit_spot.html",
            spot=spot,
            categories=categories,
            images=images,
            errors=errors
        )

    spots.update_spot(spot_id, name, lat, lon, description, category)
    upload_images(files, spot_id)
    return redirect("/spot/" + str(spot_id) + "/1")

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
        check_csrf()
        if "remove" in request.form:
            spots.remove_spot(spot_id)
            return redirect("/")
        return redirect("/spot/" + str(spot_id) + "/1")

@app.route("/add_comment", methods=["POST"])
def add_comment():
    require_login()
    check_csrf()

    spot_id = request.form["spot_id"]
    spot = spots.get_spot(spot_id)
    if not spot:
        abort(404)

    content = request.form["content"]
    if not content:
        abort(403, "Älä jätä tyhjää kommenttia!")
    user_id = session["user_id"]
    if len(content) > 500:
        abort(403)

    spots.add_comment(content, user_id, spot_id)


    return redirect("/spot/" + str(spot_id) + "/1")

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
        check_csrf()
        if "edit" in request.form:
            content = request.form["content"]
            if not content:
                abort(403, "Älä jätä tyhjää kommenttia")
            if len(content) > 500:
                abort(403)
            spots.edit_comment(comment_id, content)
        return redirect("/spot/" + str(spot_id) + "/1")

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
        check_csrf()
        if "remove" in request.form:
            spots.remove_comment(comment_id)
        return redirect("/spot/" + str(spot_id) + "/1")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not username or not password1 or not password2:
        abort(403)
    if password1 != password2:
        flash("VIRHE: Salasanat eivät ole samat", "error-message")
        return redirect("/register")
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: Tunnus on jo varattu", "error-message")
        return redirect("/register")

    flash("Tunnus luotu", "info")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            abort(403)
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: Väärä tunnus tai salasana", "error-message")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    return redirect("/")

@app.route("/map", methods=["GET"])
def map():
    rows = spots.get_all_spots()
    all_spots = []
    for row in rows:
        s = dict(row)
        s["color"] = spot_color(s.get("category", "Muut"))
        all_spots.append(s)

    # debug: print first spot keys to confirm names (remove in production)
    if all_spots:
        print("map spot sample keys:", list(all_spots[0].keys()))

    return render_template("map.html", spots=all_spots)

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

@app.teardown_appcontext
def teardown_db(exception=None):
    """Close database connection when request ends"""
    db.close_connection(exception)