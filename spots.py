import sqlite3
import db

def add_spot(name, lat, lon, category, user_id, comment):

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
    
    