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
    
    
def get_spots():
    sql = "SELECT id, name FROM spots ORDER BY id DESC"

    return db.query(sql)


def get_spot(spot_id):
    sql = """SELECT s.id,
                    s.name,
                    s.lat,
                    s.lon,
                    s.category,
                    u.id user_id,
                    u.username
            FROM spots s, users u
            WHERE s.user_id = u.id AND
                  s.id = ?"""
    
    return db.query(sql, [spot_id])[0]

def update_spot(spot_id, name, lat, lon, category):
    sql = """UPDATE spots SET name = ?,
                              lat = ?,
                              lon = ?,
                              category = ?
                          WHERE id = ?"""
    db.execute(sql, [name, lat, lon, category, spot_id])

def remove_spot(spot_id):
    sql = "DELETE FROM spots WHERE id = ?"
    db.execute(sql, [spot_id])