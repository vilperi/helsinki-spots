import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM spots")
db.execute("DELETE FROM comments")

user_count = 1000
spot_count = 10**6
comment_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, spot_count + 1):
    db.execute("INSERT INTO spots (name) VALUES (?)",
               ["spot" + str(i)])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    spot_id = random.randint(1, spot_count)
    db.execute("""INSERT INTO comments (content, sent_at, user_id, spot_id)
                  VALUES (?, datetime('now'), ?, ?)""",
               ["message" + str(i), user_id, spot_id])

db.commit()
db.close()