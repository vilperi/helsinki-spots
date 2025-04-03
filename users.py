import sqlite3
import db


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