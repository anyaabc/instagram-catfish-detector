# SCRIPT 1 FIXXX

import os
import json
import mysql.connector
from deepface import DeepFace
import numpy as np
from datetime import datetime
import time  # ditambahkan untuk mengukur durasi proses
from src.backend.config import DB_CONFIG

MODEL_NAMES = ["ArcFace", "Facenet512", "VGG-Face"]

def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot_product / norm_product if norm_product else 0

def load_uploaded_image_embedding(image_path):
    embeddings = {}
    for model_name in MODEL_NAMES:
        try:
            result = DeepFace.represent(img_path=image_path, model_name=model_name, enforce_detection=True)
            if result:
                embeddings[model_name] = result[0]["embedding"]
        except:
            continue
    return embeddings if embeddings else None

def find_potential_catfish_accounts(uploaded_image_path, similarity_threshold=0.7):
    start_time = time.time()  # waktu mulai

    uploaded_embeddings = load_uploaded_image_embedding(uploaded_image_path)
    if not uploaded_embeddings:
        return [], 0.0  # tambahkan 0 durasi jika tidak ada embedding

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
    except mysql.connector.Error:
        return [], 0.0

    matched_profiles = []

    try:
        cursor.execute("""
            SELECT fe.user_id, fe.post_id, fe.embedding, fe.image_path, fe.source_type,
                   iu.username, ip.date_posted
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
                # Parsing date_posted jika string
                raw_date = row.get("date_posted")
                if isinstance(raw_date, str):
                    try:
                        row["date_posted"] = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                    except:
                        row["date_posted"] = None

                matched_profiles.append({
                    "user_id": row["user_id"],
                    "username": row.get("username"),
                    "image_path": row["image_path"],
                    "post_id": row.get("post_id"),
                    "date_posted": row.get("date_posted"),
                    "similarity": round(avg_similarity, 4),
                    "source_type": row.get("source_type") or "unknown"
                })

        # Sorting baru: similarity desc, lalu tanggal desc
        matched_profiles.sort(
            key=lambda x: (
                -x["similarity"],
                -(x["date_posted"].timestamp() if x.get("date_posted") else 0)
            )
        )

    finally:
        cursor.close()
        conn.close()

    end_time = time.time()  # waktu selesai
    elapsed = round(end_time - start_time, 3)  # durasi dalam detik (float dibulatkan 3 angka)

    return matched_profiles, elapsed
