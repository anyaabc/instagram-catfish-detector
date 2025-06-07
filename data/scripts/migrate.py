# file: data/scripts/alter_face_embeddings.py
import os
import sys
import json
from tqdm import tqdm
from deepface import DeepFace
import mysql.connector

# Tambahkan path ke src agar bisa import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import mysql.connector
from backend.config import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        ALTER TABLE face_embeddings
        ADD COLUMN source_type ENUM('profile', 'post') NOT NULL DEFAULT 'post';
    """)
    conn.commit()
    print("✅ Kolom `source_type` berhasil ditambahkan.")
except mysql.connector.Error as err:
    print(f"🚫 ERROR: {err}")
finally:
    cursor.close()
    conn.close()
