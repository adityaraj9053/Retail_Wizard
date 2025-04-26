import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("ID | Fullname | Username | Hashed Password")
print("-" * 200)
for user in users:
    print(user)

conn.close()
