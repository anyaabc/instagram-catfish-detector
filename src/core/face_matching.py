import os
import json
import numpy as np
import sqlite3
from deepface import DeepFace
from tqdm import tqdm

# --- DATABASE CONFIG ---
DB_PATH = 'data/instagram_posts.db'

# --- SELECTED MODELS FOR SPEED & ACCURACY ---
MODEL_NAMES = ["ArcFace", "Facenet512", "VGG-Face"]
DISTANCE_METRIC = "cosine"

# --- DISTANCE THRESHOLDS PER MODEL ---
THRESHOLDS = {
    "ArcFace": 0.68,
    "Facenet512": 0.30,
    "VGG-Face": 0.30
}


def extract_face_embeddings(image_path):
    """
    Extract embeddings from an image using multiple DeepFace models.
    Returns a dict {model_name: embedding_vector}
    """
    embeddings = {}

    for model_name in MODEL_NAMES:
        try:
            representation = DeepFace.represent(
                img_path=image_path,
                model_name=model_name,
                enforce_detection=True,
                detector_backend='opencv',
                normalize=True
            )

            if isinstance(representation, list) and len(representation) > 0:
                embeddings[model_name] = representation[0]["embedding"]
        except Exception as e:
            print(f"❌ Failed to extract embedding with {model_name}: {e}")

    return embeddings


def cosine_distance(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 1
    return 1 - np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def match_embeddings(input_embeddings, top_k=5):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT post_id, username, image_type, image_path, date_posted, embedding FROM face_embeddings")
        candidates = cur.fetchall()

    results = []

    for post_id, username, image_type, image_path, date_posted, embed_json in tqdm(candidates, desc="🔍 Matching faces", ncols=80):
        db_embeddings = json.loads(embed_json)
        total_score = 0
        models_used = 0

        for model_name in MODEL_NAMES:
            if model_name in input_embeddings and model_name in db_embeddings:
                dist = cosine_distance(input_embeddings[model_name], db_embeddings[model_name])
                if dist <= THRESHOLDS[model_name]:
                    total_score += (1 - dist)
                    models_used += 1

        if models_used > 0:
            avg_score = total_score / models_used
            results.append({
                "username": username,
                "image_type": image_type,
                "image_path": image_path,
                "date_posted": date_posted,
                "match_score": round(avg_score, 4)
            })

    results = sorted(results, key=lambda x: x["match_score"], reverse=True)
    return results[:top_k]


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    uploaded_image_path = "path_to_uploaded_image.jpg"  # Replace with actual path

    if not os.path.exists(uploaded_image_path):
        print(f"🚫 File not found: {uploaded_image_path}")
        exit(1)

    input_embeddings = extract_face_embeddings(uploaded_image_path)

    if not input_embeddings:
        print("🚫 No faces detected or embeddings could not be extracted.")
    else:
        matches = match_embeddings(input_embeddings)
        print("\n🎯 Top Matches:")
        for match in matches:
            print(match)
