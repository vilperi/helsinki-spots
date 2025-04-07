import sqlite3
import db

def add_spot(name, lat, lon, description, category, user_id):
    try:
        sql = "INSERT INTO spots (name, lat, lon, description, category, user_id) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute(sql, [name, lat, lon, description, category, user_id])
    except sqlite3.IntegrityError:
        return "VIRHE: Kohdetta ei voitu luoda"

def add_image(image, spot_id):
    sql = "INSERT INTO images (image, spot_id) VALUES (?, ?)"
    db.execute(sql, [image, spot_id])

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
            WHERE s.user_id = u.id AND s.id = ?"""
    result = db.query(sql, [spot_id])
    return result[0] if result else None

def filter_spots(category):
    sql = "SELECT id, name FROM spots WHERE category = ? ORDER BY id DESC"
    return db.query(sql, [category])

def find_spots(keyword, category):
    if not keyword:
        if category == "all":
            return get_spots()
        else:
            return filter_spots(category)
    like = "%" + keyword + "%"
    if category == "all":
        sql = """SELECT id, name
                FROM spots 
                WHERE name LIKE ?
                ORDER BY id DESC"""
        return db.query(sql, [like])
    else:
        sql = """SELECT id, name
                FROM spots
                WHERE name LIKE ? AND category = ?
                ORDER BY id DESC"""
        return db.query(sql, [like, category])

def update_spot(spot_id, name, lat, lon, description, category):
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

def get_comment(comment_id):
    sql = """SELECT c.id, c.content, c.sent_at, c.user_id, c.spot_id, u.username
             FROM comments c, users u
             WHERE c.user_id = u.id AND c.id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def edit_comment(comment_id, content):
    sql = """UPDATE comments 
             SET content = ?, sent_at = datetime('now', 'localtime')
             WHERE id = ?"""
    db.execute(sql, [content, comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def get_images(spot_id):
    sql = "SELECT id FROM images WHERE spot_id = ?"
    return db.query(sql, [spot_id])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None