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


def add_comment(content, user_id, spot_id):
    sql = """INSERT INTO comments (content, sent_at, user_id, spot_id)
             VALUES (?, datetime('now', 'localtime'), ?, ?)"""
    db.execute(sql, [content, user_id, spot_id])

def get_comments(spot_id):
    sql = """SELECT c.id, c.content, c.sent_at, c.user_id, u.username
            FROM comments c, users u
            WHERE c.user_id = u.id AND c.spot_id = ?
            ORDER BY c.id DESC"""
    return db.query(sql, [spot_id])