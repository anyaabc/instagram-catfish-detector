import os
import sys
import json
from tqdm import tqdm
from deepface import DeepFace
import mysql.connector

# Tambahkan path ke src agar bisa import DB config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from backend.config import DB_CONFIG

# Model yang digunakan untuk ekstraksi wajah
MODEL_NAMES = ["ArcFace", "Facenet512", "VGG-Face"]

def get_face_embeddings(image_path):
    """
    Ekstrak embedding wajah dari gambar menggunakan beberapa model.
    Kembalikan dict {model_name: embedding_list} atau None jika tidak ditemukan wajah.
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
                embeddings[model_name] = result[0]["embedding"]
        except Exception as e:
            print(f"⚠️ No face in {image_path} for {model_name}: {e}")
    return embeddings if embeddings else None

def embeddings_to_bytes(embeddings: dict) -> bytes:
    """
    Ubah dict embedding menjadi JSON bytes (untuk disimpan ke LONGBLOB).
    """
    return json.dumps(embeddings).encode('utf-8')

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        total_inserted = 0

        # 1. Embedding untuk foto profil
        cursor.execute("SELECT user_id, profile_image_local FROM instagram_users")
        users = cursor.fetchall()

        for user in tqdm(users, desc="🧠 Generating embeddings (profiles)"):
            user_id = user['user_id']
            profile_img_path = user['profile_image_local']

            if profile_img_path and os.path.isfile(profile_img_path):
                embeddings = get_face_embeddings(profile_img_path)
                if embeddings:
                    emb_bytes = embeddings_to_bytes(embeddings)
                    cursor.execute("""
                        INSERT INTO face_embeddings (user_id, post_id, embedding, image_path, source_type)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user_id, None, emb_bytes, profile_img_path, 'profile'))
                    conn.commit()
                    total_inserted += 1

        # 2. Embedding untuk gambar di postingan
        cursor.execute("SELECT post_id, user_id, image_local_paths FROM instagram_posts")
        posts = cursor.fetchall()

        for post in tqdm(posts, desc="🧠 Generating embeddings (posts)"):
            post_id = post['post_id']
            user_id = post['user_id']
            try:
                image_paths = json.loads(post['image_local_paths'])
            except:
                image_paths = []

            for img_path in image_paths:
                if img_path and os.path.isfile(img_path):
                    embeddings = get_face_embeddings(img_path)
                    if embeddings:
                        emb_bytes = embeddings_to_bytes(embeddings)
                        cursor.execute("""
                            INSERT INTO face_embeddings (user_id, post_id, embedding, image_path, source_type)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (user_id, post_id, emb_bytes, img_path, 'post'))
                        conn.commit()
                        total_inserted += 1

        cursor.close()
        conn.close()

        print("\n✅ DONE: Semua embedding berhasil diproses.")
        print(f"🔢 Total embeddings inserted: {total_inserted}")

    except mysql.connector.Error as err:
        print(f"🚫 Database Error: {err}")

if __name__ == "__main__":
    main()
