import sqlite3
import db

def add_spot(name, lat, lon, description, category, user_id):

    try:
        sql = "INSERT INTO spots (name, lat, lon, description, category, user_id) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute(sql, [name, lat, lon, description, category, user_id])
    except sqlite3.IntegrityError:
        return "VIRHE: Kohdetta ei voitu luoda"


def get_spots():
    sql = "SELECT id, name FROM spots ORDER BY id DESC"

    return db.query(sql)


def get_spot(spot_id):
    sql = """SELECT s.id,
                    s.name,
                    s.lat,
                    s.lon,
                    s.description,
                    s.category,
                    u.id user_id,
                    u.username
            FROM spots s, users u
            WHERE s.user_id = u.id AND
                  s.id = ?"""
    
    return db.query(sql, [spot_id])[0]


def find_spots(keyword):
    sql = """SELECT id, name 
             FROM spots
             WHERE name LIKE ?
             ORDER BY id DESC"""
    like = "%" + keyword + "%"
    return db.query(sql, [like])

def update_spot(spot_id, name, lat, description, lon, category):
    sql = """UPDATE spots SET name = ?,
                              lat = ?,
                              lon = ?,
                              description = ?,
                              category = ?
                          WHERE id = ?"""
    db.execute(sql, [name, lat, lon, description, category, spot_id])

def remove_spot(spot_id):
    sql = "DELETE FROM spots WHERE id = ?"
    db.execute(sql, [spot_id])