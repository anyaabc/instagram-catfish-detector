# file: core/face_matching.py

import os
import json
import numpy as np
import mysql.connector
from deepface import DeepFace
from scipy.spatial.distance import cosine
from datetime import datetime

# Import konfigurasi database dari backend
from backend.config import DB_CONFIG

# Model yang digunakan harus konsisten dengan generate_embeddings.py
MODEL_NAMES = ["ArcFace", "Facenet512", "VGG-Face"]


def load_uploaded_image_embedding(image_path):
    """
    Ambil embedding wajah dari gambar yang diunggah user.
    """
    embeddings = {}
    for model_name in MODEL_NAMES:
        try:
            result = DeepFace.represent(
                img_path=image_path,
                model_name=model_name,
                enforce_detection=True
            )
            if result:
                embeddings[model_name] = result[0]['embedding']
        except Exception as e:
            print(f"⚠️ No face detected in uploaded image for {model_name}: {e}")
    return embeddings if embeddings else None


def bytes_to_embeddings(byte_data):
    """
    Konversi LONGBLOB (bytes) ke dict embedding.
    """
    return json.loads(byte_data.decode('utf-8'))


def cosine_similarity(vec1, vec2):
    """
    Hitung similarity antar dua embedding menggunakan 1 - cosine distance.
    """
    return 1 - cosine(vec1, vec2)


def find_potential_catfish_accounts(uploaded_image_path, similarity_threshold=0.7):
    """
    Cek kemiripan wajah antara gambar yang diupload user dengan semua gambar di DB.
    Kembalikan daftar akun yang mencurigakan.
    """
    uploaded_embeddings = load_uploaded_image_embedding(uploaded_image_path)
    if not uploaded_embeddings:
        return []

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT fe.user_id, fe.post_id, fe.embedding, fe.image_path, iu.username, ip.taken_at FROM face_embeddings fe LEFT JOIN instagram_users iu ON fe.user_id = iu.user_id LEFT JOIN instagram_posts ip ON fe.post_id = ip.post_id")
    results = cursor.fetchall()

    matches = []

    for row in results:
        db_embeddings = bytes_to_embeddings(row['embedding'])
        similarities = []

        for model in MODEL_NAMES:
            if model in uploaded_embeddings and model in db_embeddings:
                sim = cosine_similarity(uploaded_embeddings[model], db_embeddings[model])
                similarities.append(sim)

        if similarities:
            avg_similarity = np.mean(similarities)
            if avg_similarity >= similarity_threshold:
                matches.append({
                    "user_id": row['user_id'],
                    "username": row.get('username'),
                    "post_id": row.get('post_id'),
                    "image_path": row.get('image_path'),
                    "taken_at": row.get('taken_at'),
                    "similarity_score": round(avg_similarity, 3)
                })

    cursor.close()
    conn.close()

    # Urutkan hasil berdasarkan tanggal post (yang paling lama dulu)
    matches.sort(key=lambda x: datetiimport os
import json
import mysql.connector
from deepface import DeepFace
import numpy as np
from backend.config import DB_CONFIG

def cosine_similarity(vec1, vec2):
    """Hitung cosine similarity antara dua vektor."""
    vec1, vec2 = np.array(vec1), np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot_product / norm_product if norm_product else 0

def load_uploaded_image_embedding(image_path):
    """
    Ekstrak embedding dari gambar yang diunggah dengan beberapa model DeepFace.
    """
    MODEL_NAMES = ["ArcFace", "Facenet512", "VGG-Face"]
    embeddings = {}
    for model_name in MODEL_NAMES:
        try:
            result = DeepFace.represent(img_path=image_path, model_name=model_name, enforce_detection=True)
            if result:
                embeddings[model_name] = result[0]["embedding"]
        except Exception as e:
            print(f"⚠️ Face not found in uploaded image for model {model_name}: {e}")
    return embeddings if embeddings else None

def find_potential_catfish_accounts(uploaded_image_path, similarity_threshold=0.7):
    """
    Cari akun yang punya kemiripan wajah tinggi dengan gambar yang diunggah.
    """
    uploaded_embeddings = load_uploaded_image_embedding(uploaded_image_path)
    if not uploaded_embeddings:
        print("🚫 No valid face detected in uploaded image.")
        return []

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
    except mysql.connector.Error as err:
        print(f"🚫 Database connection error: {err}")
        return []

    matched_profiles = []

    try:
        cursor.execute("""
            SELECT fe.user_id, fe.post_id, fe.embedding, fe.image_path,
                   iu.username, iu.full_name, ip.caption, ip.timestamp
            FROM face_embeddings fe
            LEFT JOIN instagram_users iu ON fe.user_id = iu.user_id
            LEFT JOIN instagram_posts ip ON fe.post_id = ip.post_id
        """)
        embeddings_db = cursor.fetchall()

        for row in embeddings_db:
            try:
                db_embeddings = json.loads(row["embedding"])
            except:
                continue

            similarities = [
                cosine_similarity(uploaded_embeddings[model], db_embeddings[model])
                for model in uploaded_embeddings if model in db_embeddings
            ]
            avg_similarity = sum(similarities) / len(similarities) if similarities else 0

            if avg_similarity >= similarity_threshold:
                matched_profiles.append({
                    "user_id": row["user_id"],
                    "username": row.get("username"),
                    "image_path": row["image_path"],
                    "post_id": row.get("post_id"),
                    "full_name": row.get("full_name"),
                    "caption": row.get("caption"),
                    "timestamp": row.get("timestamp"),
                    "similarity": round(avg_similarity, 4)
                })

        # Urutkan hasil dari yang paling lama (asumsi akun original) ke terbaru
        matched_profiles.sort(key=lambda x: x.get("timestamp") or '', reverse=False)

    finally:
        cursor.close()
        conn.close()

    return matched_profiles

# # Optional CLI test
# if __name__ == "__main__":
#     test_path = "path/to/uploaded/image.jpg"
#     results = find_potential_catfish_accounts(test_path)
#     for match in results:
#         print(match)
# me.strptime(x['taken_at'], "%Y-%m-%d %H:%M:%S") if x['taken_at'] else datetime.max)

#     return matches
