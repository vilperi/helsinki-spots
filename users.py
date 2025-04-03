import sqlite3
import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, created_at, password_hash) VALUES (?, datetime('now', 'localtime'), ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return 


def get_user(user_id):
    sql = "SELECT id, username, created_at, wrong_coords FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_spots(user_id):
    sql = "SELECT id, name FROM spots WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def count_comments(user_id):
    sql = "SELECT COUNT(id) FROM comments WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0][0]

def wrong_coords(user_id):
    sql = "UPDATE users SET wrong_coords = wrong_coords + 1 WHERE id = ?"
    db.execute(sql, [user_id])