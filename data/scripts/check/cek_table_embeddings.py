# file: data/scripts/verify_embeddings.py
import os
import sys
import json
from tqdm import tqdm
from deepface import DeepFace
import mysql.connector

# Tambahkan path ke src agar bisa import DB config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
from backend.config import DB_CONFIG

def verify_face_embeddings():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as total FROM face_embeddings")
        total = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as profiles FROM face_embeddings WHERE source_type = 'profile'")
        profiles = cursor.fetchone()['profiles']

        cursor.execute("SELECT COUNT(*) as posts FROM face_embeddings WHERE source_type = 'post'")
        posts = cursor.fetchone()['posts']

        print(f"🔎 Total embeddings: {total}")
        print(f"👤 Profile embeddings: {profiles}")
        print(f"🖼️ Post embeddings: {posts}")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"🚫 Error: {err}")

if __name__ == "__main__":
    verify_face_embeddings()
