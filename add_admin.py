import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

db_path = "/Users/serik08/Documents/GitHub/clothing-brand-website/instance/franchise_brand.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# новый админ
email = "srk@gmail.com"
password = "123456"   # потом сменишь
role = "admin"

hashed_password = generate_password_hash(password)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute("""
    INSERT INTO user (email, password, datetime, role)
    VALUES (?, ?, ?, ?)
""", (email, hashed_password, now, role))

conn.commit()
conn.close()

print(f"✅ Новый админ {email} добавлен!")