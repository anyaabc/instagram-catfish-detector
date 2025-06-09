## 📖 Project Description

🕵️‍♂️ **instagram-catfish-detector** is a cybersecurity thesis project that enables users to upload a photo and check whether the same face appears on suspicious Instagram accounts. 

This tool helps detect potential impersonation (catfishing) by checking who posted a similar image first using facial recognition.

---

The system uses:

* 🧠 **DeepFace** for facial recognition
* 🌐 **Bright Data** to scrape public Instagram metadata
* 🐍 **Flask** as the backend REST API
* 💻 A clean web frontend (HTML + JS + CSS)
* 🛢️ **MariaDB** as the main database

---

## 🧱 Folder Structure

```
instagram-catfish-detector/
├── data/
│   ├── images/                  # Stored Instagram post/profile images
│   ├── uploads/                 # Uploaded images from users
│   └── scripts/
│       ├── check/              # Script to check DB tables/debug image dates
│       ├── db_setup.py         # Create DB schema and insert records
│       ├── download_images.py  # Download image files from metadata
│       └── generate_embeddings.py  # Generate embeddings for each image
│
├── environment/
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Optional env doc
│
├── src/
│   ├── backend/
│   │   ├── app.py              # Flask app
│   │   └── config.py           # Config file for DB credentials
│   ├── core/
│   │   └── face_matching.py    # Face matching logic
│   └── frontend/
│       ├── index.html          # Web UI
│       ├── style.css           # Styling
│       └── script.js           # Client-side logic
│
├── test/
│   └── test_face_matching.py   # Unit test for matching
├── .gitignore
├── config.env
├── LICENSE
└── README.md
```

---

## 🚀 Setup Guide

### Step 1 – Clone the Repo

```bash
git clone https://github.com/yourname/instagram-catfish-detector.git
cd instagram-catfish-detector
```

### Step 2 – Install Python and MariaDB

- ✅ Make sure Python version is **3.10.0**
- ✅ Download MariaDB Server version **11.4.7**:
  [Download Link](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.4.7&os=windows&cpu=x86_64&pkg=msi&mirror=heru)
  ### 🛠️ [Optional] Add MariaDB `bin` Folder to System PATH (Windows Only)

If you want to use `mysql` or `mysqldump` commands directly from your terminal (without navigating to the installation folder every time), you should add MariaDB’s `bin` folder to your system `PATH`.

#### 📌 Steps:

1. **Locate MariaDB `bin` Folder**

   Usually found at:
   ```
   C:\Program Files\MariaDB 11.7\bin
   ```
   *(Adjust based on your installation directory)*

2. **Open Environment Variables Settings**
   - Press `Windows + S`
   - Type **Environment Variables**
   - Click on **Edit the system environment variables**
   - In the **System Properties** window, click the **Environment Variables...** button

3. **Edit the `Path` Variable**
   - Under **User variables** or **System variables**, find a variable named `Path`
   - Select it and click **Edit...**
   - Click **New**, then paste the path to your `bin` folder, for example:
     ```
     C:\Program Files\MariaDB 11.7\bin
     ```

4. **Click OK** to close all dialogs and save changes

5. **Restart Terminal**
   - Close all open terminals (CMD, PowerShell, VSCode)
   - Open them again so the new PATH takes effect

### 🔐 Important: Remember Your MariaDB Root Username and Password

After installing MariaDB:

- You’ll be asked to **set a root password**
- **Keep it safe!** You’ll need this when creating your database and connecting from your application

> ✅ By default, you can use:
> - **Username**: `root`
> - **Password**: (whatever you set during installation)

You’ll enter this info later in the `config.env` file to connect your Python app to the database.

### Step 3 – (Optional) Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
```

### Step 4 – Install All Python Requirements

```bash
pip install -r environment/requirements.txt
```

### Step 5 – Ensure Dataset is Present

Ensure the file `data/dataset.json` is available. This contains Instagram metadata.

### Step 6 – Run DB Setup

```bash
python data/scripts/db_setup.py
```

### Step 7 – Download Instagram Images

```bash
python data/scripts/download_images.py
```

### Step 8 – Generate Face Embeddings

```bash
python data/scripts/generate_embeddings.py
```

### Step 9 – (Optional) Debug / Check Tables

```bash
# Check embeddings or DB table existence:
python data/scripts/check/cek_table_embeddings.py
```

### Step 10 – Setup DB Credentials (Environment File)

Create a file named `config.env` in the project root based on `.env_example`:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_db_password
DB_NAME=instagram_db

```

Ensure MariaDB/MySQL service is running.

### Step 11 – (Optional) Run Unit Test for Matching

```bash
python test/test_face_matching.py
```

### Step 12 – Run the Flask App

```bash
python src/backend/app.py
```

---

## 🌐 Using the Web Interface

**Don't use Live Server** to open `index.html`. Access via Flask instead:

1. Open browser to `http://127.0.0.1:5000/`
2. Upload image (JPG/PNG only, max 5MB)
3. Preview image shown before submitting
4. System processes image and returns results
5. Results include face matches + metadata + original post info

---

## 🧰 Requirements (environment/requirements.txt)

```
Flask==3.1.0
Flask-Cors==5.0.1
requests==2.32.3
deepface==0.0.93
tensorflow==2.19.0
tf-keras==2.19.0
Pillow==11.2.1
numpy==2.1.3
pandas==2.2.3
matplotlib==3.10.3
opencv-python==4.11.0.86
tqdm==4.67.1
scikit-learn==1.6.1
mysql-connector-python==9.3.0
python-dotenv==1.1.0
```

---

## ✅ Summary of Commands

```bash
# Clone project
cd instagram-catfish-detector

# Virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r environment/requirements.txt

# Dataset setup
python data/scripts/db_setup.py
python data/scripts/download_images.py
python data/scripts/generate_embeddings.py

# Optional checks
python data/scripts/check/cek_table_embeddings.py

# Start Flask App
python src/backend/app.py

# Access frontend
http://127.0.0.1:5000/
```

---

## 📸 Fitur Tambahan

- ✅ Validasi ukuran dan format file (JPG/PNG, max 5MB)
- ✅ Preview gambar sebelum dikirim
- ✅ Spinner loading saat pengecekan
- ✅ Hasil match disertai gambar dan metadata pengguna asli
- ✅ UI responsif dan siap untuk laptop/desktop

---


