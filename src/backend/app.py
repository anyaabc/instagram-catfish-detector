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

# ——————————————————————————————
# Fungsi: Validasi ekstensi file
# ——————————————————————————————
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ——————————————————————————————
# Route: Serve halaman utama (index.html)
# ——————————————————————————————
@app.route('/')
def index():
    return send_file(os.path.join(FRONTEND_FOLDER, 'index.html'))

# ——————————————————————————————
# Route: Serve static assets (style.css, script.js)
# ——————————————————————————————
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)

# ——————————————————————————————
# Route: Serve image statis dari folder data/images
# ——————————————————————————————
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# ——————————————————————————————
# API: Terima upload dan lakukan face matching
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

        # Panggil fungsi face matching
        try:
            results = find_potential_catfish_accounts(filepath)
            return jsonify({'matches': results}), 200
        except Exception as e:
            return jsonify({'error': f"Face matching error: {str(e)}"}), 500
    else:
        return jsonify({'error': 'Invalid file format. Only JPG, JPEG, PNG allowed.'}), 400

# ——————————————————————————————
# Main entry
# ——————————————————————————————
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
