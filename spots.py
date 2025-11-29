import sqlite3
import db

def add_spot(name, lat, lon, description, category, user_id):
    try:
        sql = """INSERT INTO spots (name, lat, lon, description, category, user_id)
                 VALUES (?, ?, ?, ?, ?, ?)"""
        db.execute(sql, [name, lat, lon, description, category, user_id])
    except sqlite3.IntegrityError:
        return "VIRHE: Kohdetta ei voitu luoda"

def add_image(image, spot_id):
    sql = "INSERT INTO images (image, spot_id) VALUES (?, ?)"
    db.execute(sql, [image, spot_id])

def get_all_spots():
    sql = """SELECT s.id AS spot_id,
                    s.name,
                    s.lat,
                    s.lon,
                    s.description,
                    s.category,
                    u.id AS user_id,
                    u.username
            FROM spots s
            LEFT JOIN users u ON s.user_id = u.id"""
    result = db.query(sql, [])
    # Always return a list (possibly empty) and use consistent keys (spot_id, user_id)
    return result

def get_spots(page, page_size):
    sql = """SELECT s.id AS spot_id,
                    s.name,
                    s.category,
                    (SELECT MIN(i.id) FROM images i WHERE i.spot_id = s.id) AS image_id,
                    u.username,
                    (SELECT COUNT(*) FROM comments c WHERE c.spot_id = s.id) AS comment_count,
                    (SELECT COUNT(*) FROM spots) AS spot_count
             FROM spots s
             LEFT JOIN users u ON s.user_id = u.id
             ORDER BY s.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

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

def get_test_spot(spot_id):
    '''Tämä funktio on seed.py testitiedostolla
    luodun kohteen hakemista varten'''
    sql = """SELECT id, name FROM spots WHERE id = ?"""
    result = db.query(sql, [spot_id])
    return result[0] if result else None

def count_rows(table: str):
    sql = f"SELECT COUNT(*) FROM {table}"
    result = db.query(sql)
    return result[0][0] if result else None

def filter_spots(category, limit, offset):
    sql = """SELECT s.id AS spot_id,
                    s.name,
                    s.category,
                    (SELECT MIN(i.id) FROM images i WHERE i.spot_id = s.id) AS image_id,
                    u.username,
                    (SELECT COUNT(*) FROM comments c WHERE c.spot_id = s.id) AS comment_count,
                    (SELECT COUNT(*) FROM spots WHERE category = ?) AS spot_count
            FROM spots s
            LEFT JOIN users u ON s.user_id = u.id
            WHERE category = ?
            ORDER BY s.id DESC
            LIMIT ? OFFSET ?"""
    return db.query(sql, [category, category, limit, offset])

def find_spots(keyword, category, page, page_size):
    limit = page_size
    offset = page_size * (page - 1)
    if not keyword:
        if category == "all":
            return get_spots(page, page_size)
        else:
            return filter_spots(category, limit, offset)
    like = "%" + keyword + "%"
    if category == "all":
        sql = """SELECT s.id AS spot_id,
                        s.name,
                        s.category,
                        (SELECT MIN(i.id) FROM images i WHERE i.spot_id = s.id) AS image_id,
                        u.username,
                        (SELECT COUNT(*) FROM comments c WHERE c.spot_id = s.id) AS comment_count,
                        (SELECT COUNT(*) FROM spots WHERE name LIKE ?) AS spot_count
                FROM spots s
                LEFT JOIN users u ON s.user_id = u.id
                WHERE name LIKE ?
                ORDER BY s.id DESC
                LIMIT ? OFFSET ?"""
        return db.query(sql, [like, like, limit, offset])
    else:
        sql = """SELECT s.id AS spot_id,
                        s.name,
                        s.category,
                        (SELECT MIN(i.id) FROM images i WHERE i.spot_id = s.id) AS image_id,
                        u.username,
                        (SELECT COUNT(*) FROM comments c WHERE c.spot_id = s.id) AS comment_count,
                        (SELECT COUNT(*) FROM spots WHERE name LIKE ? AND category = ?) AS spot_count
                FROM spots s
                LEFT JOIN users u ON s.user_id = u.id
                WHERE name LIKE ? AND category = ?
                ORDER BY s.id DESC
                LIMIT ? OFFSET ?"""
        return db.query(sql, [like, category, like, category, limit, offset])

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

def get_comments(spot_id, page, page_size):
    sql = """SELECT c.id, c.content, c.sent_at, c.user_id, u.username
            FROM comments c, users u
            WHERE c.user_id = u.id AND c.spot_id = ?
            ORDER BY c.id DESC
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [spot_id, limit, offset])

def get_comment(comment_id):
    sql = """SELECT c.id, c.content, c.sent_at, c.user_id, c.spot_id, u.username
             FROM comments c, users u
             WHERE c.user_id = u.id AND c.id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def count_comments(spot_id):
    sql = "SELECT COUNT(*) FROM comments WHERE spot_id = ?"
    result = db.query(sql, [spot_id])
    return result[0][0] if result else None

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

def remove_image(spot_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND spot_id = ?"
    db.execute(sql, [image_id, spot_id])
