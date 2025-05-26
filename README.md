# 🕵️‍♂️ instagram-catfish-detector

A tool to detect catfish accounts on Instagram by analyzing profile pictures and post metadata using OSINT techniques and facial recognition.

---
## 📖 Project Description

**Catfish Checker** is a cybersecurity thesis project that allows users to upload an image and check if it appears on suspicious Instagram accounts.  
The tool uses facial recognition (via DeepFace) to compare uploaded images with scraped Instagram data. It helps identify potential impersonation by checking who posted the image first.

---

The tool uses:

* 🧠 DeepFace for face matching
* 🌐 Bright Data for scraping public Instagram data
* 🐍 Flask for the backend API
* 💻 Simple frontend UI

---

## 🧱 Folder Structure

```
instagram-catfish-detector/
├── data/                 # Dataset and image storage
│   ├── scripts/          # DB and image setup
│   ├── dataset.json      # Main Instagram metadata
│   ├── cleaned/          # Optional cleaned dataset
│   └── downloads/        # Downloaded post/profile images
│
├── environment/          # Environment setup
│   ├── requirements.txt  # Python dependencies
│   └── README.md         # (This file)
│
├── src/                  # Main source code
│   ├── backend/          # Flask backend
│   ├── core/             # Face recognition logic
│   ├── frontend/         # Web frontend
│   ├── utils/            # Helper functions
│   ├── assets/           # Static assets (e.g., logo)
│   └── tests/            # Unit tests
|
├── templates/            # idk yet untuk apa
└── README.md             # Project overview
```

---

## 🚀 Setup Guide

### Step 1 – Clone the Repo

```bash
git clone https://github.com/yourname/instagram-catfish-detector.git
cd instagram-catfish-detector
```

### Step 2 – (Optional) Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### Step 3 – Install Python Dependencies

Make sure you have Python 3.10 or newer. Then run:

```bash
pip install -r environment/requirements.txt
```

---

## 📦 Dataset & DB Setup

### Step 4 – Add Dataset

Ensure the file `data/dataset.json` is present. It contains scraped Instagram metadata.

### Step 5 – Run DB & Image Setup

This will download profile/post images and populate `instagram_posts.db`:

```bash
python data/scripts/dbsetup.py
```

Output:

```
✅ Database saved at: data/instagram_posts.db
🖼️  Images downloaded to: data/downloads/
🧮 Posts inserted: XXX
```

---

## 📌 Git LFS Setup (for large files)

This repo uses Git LFS to store large files (e.g., images, models).

### Install Git LFS:

* **Windows**: [Git LFS Installer](https://git-lfs.github.com/)
* **macOS**: `brew install git-lfs`
* **Linux**: `sudo apt install git-lfs`

Then run:

```bash
git lfs install
```

---

## ✅ Summary of Commands

```bash
# Clone project
cd instagram-catfish-detector

# Virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r environment/requirements.txt

# Dataset + DB
python data/scripts/dbsetup.py

---