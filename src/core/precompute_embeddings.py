import os
import json
import sqlite3
from tqdm import tqdm
from deepface import DeepFace

# --- CONFIGURATIONS ---
DB_PATH = "data/instagram_posts.db"
MODEL_NAME = "Facenet"  # You can change this to VGG-Face, ArcFace, Dlib, etc.

# --- CONNECT TO DB ---
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- CREATE TABLE FOR FACE EMBEDDINGS ---
cur.execute('''
CREATE TABLE IF NOT EXISTS face_embeddings (
    embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    image_type TEXT,  -- 'profile' or 'post'
    image_path TEXT,
    embedding TEXT     -- store as JSON string
)
''')
conn.commit()

# --- FACE EMBEDDING FUNCTION ---
def get_face_embedding(image_path):
    try:
        # Use DeepFace to extract embedding
        embedding_result = DeepFace.represent(
            img_path=image_path,
            model_name=MODEL_NAME,
            enforce_detection=True
        )
        if embedding_result:
            return embedding_result[0]["embedding"]
    except Exception as e:
        print(f"⚠️ Face not detected in {image_path}: {e}")
    return None

# --- PROCESS POSTS FROM DB ---
cur.execute("SELECT username, profile_image_local, image_local_paths FROM posts")
rows = cur.fetchall()

count_inserted = 0
for username, profile_img_path, image_paths_json in tqdm(rows, desc="🔍 Extracting face embeddings"):

    # --- PROFILE IMAGE ---
    if profile_img_path and os.path.exists(profile_img_path):
        embedding = get_face_embedding(profile_img_path)
        if embedding:
            cur.execute('''
                INSERT INTO face_embeddings (username, image_type, image_path, embedding)
                VALUES (?, ?, ?, ?)
            ''', (username, 'profile', profile_img_path, json.dumps(embedding)))
            conn.commit()
            count_inserted += 1

    # --- POST IMAGES ---
    try:
        image_paths = json.loads(image_paths_json)
    except:
        image_paths = []

    for post_img_path in image_paths:
        if post_img_path and os.path.exists(post_img_path):
            embedding = get_face_embedding(post_img_path)
            if embedding:
                cur.execute('''
                    INSERT INTO face_embeddings (username, image_type, image_path, embedding)
                    VALUES (?, ?, ?, ?)
                ''', (username, 'post', post_img_path, json.dumps(embedding)))
                conn.commit()
                count_inserted += 1

# --- DONE ---
conn.close()
print("\n✅ All embeddings processed and stored.")
print(f"🧠 Total embeddings inserted: {count_inserted}")
