import os
import json
import mysql.connector
from deepface import DeepFace
import numpy as np
from backend.config import DB_CONFIG

MODEL_NAMES = ["ArcFace", "Facenet512", "VGG-Face"]

def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    dot = np.dot(vec1, vec2)
    norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot / norm if norm else 0

def load_uploaded_image_embedding(image_path):
    embeddings = {}
    for model in MODEL_NAMES:
        try:
            result = DeepFace.represent(img_path=image_path, model_name=model, enforce_detection=True)
            if result:
                embeddings[model] = result[0]["embedding"]
        except Exception as e:
            print(f"⚠️ No face in uploaded image for {model}: {e}")
    return embeddings if embeddings else None

def match_against_embeddings(uploaded_embeddings, source_type, threshold):
    matches = []
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = f"""
            SELECT fe.user_id, fe.post_id, fe.embedding, fe.image_path, fe.source_type,
                   iu.username, ip.date_posted
            FROM face_embeddings fe
            LEFT JOIN instagram_users iu ON fe.user_id = iu.user_id
            LEFT JOIN instagram_posts ip ON fe.post_id = ip.post_id
            WHERE fe.source_type = %s
        """
        cursor.execute(query, (source_type,))
        rows = cursor.fetchall()

        for row in rows:
            try:
                db_embeddings = json.loads(row["embedding"])
            except:
                continue

            sims = [
                cosine_similarity(uploaded_embeddings[model], db_embeddings[model])
                for model in uploaded_embeddings if model in db_embeddings
            ]
            avg_sim = sum(sims) / len(sims) if sims else 0

            if avg_sim >= threshold:
                matches.append({
                    "user_id": row["user_id"],
                    "username": row.get("username") or "Unknown",
                    "image_path": row["image_path"],
                    "post_id": row.get("post_id"),
                    "date_posted": row.get("date_posted"),
                    "similarity": round(avg_sim, 4),
                    "source_type": row["source_type"]  # 'profile' or 'post'
                })

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"🚫 DB Error: {err}")

    return matches

def find_potential_catfish_accounts(uploaded_image_path):
    uploaded_embeddings = load_uploaded_image_embedding(uploaded_image_path)
    if not uploaded_embeddings:
        print("🚫 Tidak ditemukan wajah yang valid di gambar yang diunggah.")
        return []

    # Step 1: Cek foto profil
    profile_matches = match_against_embeddings(uploaded_embeddings, source_type='profile', threshold=0.75)

    if profile_matches:
        print(f"Ditemukan {len(profile_matches)} potensi akun catfishing (berdasarkan foto profil):")
        for match in sorted(profile_matches, key=lambda x: x.get("date_posted") or ''):
            print(f"- {match['username']} | Score: {match['similarity']} | Source: dari foto profil | Date: {match['date_posted'] or 'N/A'}")
        return profile_matches

    # Step 2: Kalau tidak ada di profile, lanjut ke post
    post_matches = match_against_embeddings(uploaded_embeddings, source_type='post', threshold=0.65)
    if post_matches:
        print(f"Ditemukan {len(post_matches)} potensi akun catfishing (berdasarkan postingan):")
        for match in sorted(post_matches, key=lambda x: x.get("date_posted") or ''):
            print(f"- {match['username']} | Score: {match['similarity']} | Source: dari postingan | Date: {match['date_posted'] or 'N/A'}")
        return post_matches

    print("❌ Tidak ditemukan potensi akun catfishing yang cocok.")
    return []

# Optional: CLI test
if __name__ == "__main__":
    test_path = "path/to/uploaded/image.jpg"
    find_potential_catfish_accounts(test_path)
