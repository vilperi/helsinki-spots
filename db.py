import sqlite3
import os
from flask import g

def get_connection():
    """Get or create a database connection for this request context"""
    # Check if connection already exists in Flask's g object
    if 'db' not in g:
        # Verify database file exists
        db_path = "database.db"
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file {db_path} not found!")
        
        # Create new connection
        g.db = sqlite3.connect(db_path)
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_connection(exception=None):
    """Close database connection at end of request"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def execute(sql, params=[]):
    """Execute a SQL statement that modifies data"""
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid

def last_insert_id():
    """Get the last inserted row ID"""
    return g.get('last_insert_id', None)

def query(sql, params=[]):
    """Execute a SQL query that returns data"""
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    return result