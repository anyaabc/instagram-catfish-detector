# src/backend/app.py

import os
import uuid
import sys
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename

# Tambahkan path agar bisa import dari src/core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.face_matching import find_potential_catfish_accounts

# ——————————————————————————————
# Konfigurasi
# ——————————————————————————————
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/uploads'))
IMAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/images'))
FRONTEND_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ——————————————————————————————
# Route: Serve halaman frontend
# ——————————————————————————————
@app.route('/')
def index():
    return send_file(os.path.join(FRONTEND_FOLDER, 'index.html'))

# ——————————————————————————————
# Route: Serve static image dari data/images/
# ——————————————————————————————
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# ——————————————————————————————
# API: Terima upload + match
# ——————————————————————————————
@app.route('/api/match', methods=['POST'])
def upload_and_match():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Panggil face_matching
        results = find_potential_catfish_accounts(filepath)
        return jsonify({'matches': results}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

# ——————————————————————————————
# Jika dijalankan langsung
# ——————————————————————————————
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
