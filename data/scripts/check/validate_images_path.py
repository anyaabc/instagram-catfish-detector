import os
import mysql.connector
import json
import sys

# Tambahkan path ke folder src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
from backend.config import DB_CONFIG

# Path absolut ke data/images
BASE_IMAGE_DIR = os.path.abspath('data/images')

def validate_image_paths():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT fe.embedding, fe.image_path, iu.username
            FROM face_embeddings fe
            LEFT JOIN instagram_users iu ON fe.user_id = iu.user_id
        """)

        rows = cursor.fetchall()
        missing_files = []

        for row in rows:
            image_path = row['image_path']
            if not image_path:
                continue
            if not os.path.isfile(image_path):
                missing_files.append({
                    "username": row.get("username", "unknown"),
                    "image_path": image_path
                })

        if missing_files:
            print("⚠️ File gambar berikut TIDAK ditemukan:")
            for m in missing_files:
                print(f" - {m['username']}: {m['image_path']}")
        else:
            print("✅ Semua file image ditemukan dan valid.")

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == "__main__":
    validate_image_paths()
