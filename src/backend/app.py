# src/backend/app.py

import os
import uuid
import sys
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# === Tambahkan path agar bisa import dari src/core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.face_matching import find_potential_catfish_accounts

# === Konfigurasi Upload ===
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/uploads'))
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/match', methods=['POST'])
def upload_and_match():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        results = find_potential_catfish_accounts(filepath)
        return jsonify({'results': results}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/')
def index():
    return "✅ Flask Backend Running for Catfish Checker"

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
