# # file: data/scripts/cek.py

import sys
import os

# Tambahkan path ke folder src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# import mysql.connector
# from backend.config import DB_CONFIG

# # Cek isi tabel
# conn = mysql.connector.connect(**DB_CONFIG)
# cursor = conn.cursor()

# cursor.execute("SELECT COUNT(*) FROM instagram_users;")
# users_count = cursor.fetchone()[0]
# print(f"👤 Users: {users_count}")

# cursor.execute("SELECT COUNT(*) FROM instagram_posts;")
# posts_count = cursor.fetchone()[0]
# print(f"📷 Posts: {posts_count}")

# cursor.execute("SELECT COUNT(*) FROM face_embeddings;")
# embeddings_count = cursor.fetchone()[0]
# print(f"🧠 Embeddings: {embeddings_count}")

# cursor.close()
# conn.close()




import mysql.connector
from backend.config import DB_CONFIG  # pastikan path ini sesuai

def cek_tabel():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in DB:")
    for t in tables:
        print(t[0])

    cursor.execute("DESCRIBE instagram_users")
    print("\nStructure of instagram_users:")
    for row in cursor.fetchall():
        print(row)

    # 2. Check structure of instagram_posts
    print("\nStructure of instagram_posts:")
    cursor.execute("DESCRIBE instagram_posts")
    for column in cursor.fetchall():
        print(f"Column: {column[0]} | Type: {column[1]} | Null: {column[2]} | Key: {column[3]}")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    cek_tabel()