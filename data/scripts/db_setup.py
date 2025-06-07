# file: data/scripts/db_setup.py

import sys
import os

# Tambahkan path ke folder src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import mysql.connector
from mysql.connector import errorcode
from backend.config import DB_CONFIG

def create_tables():
    TABLES = {}

    # Tabel users
    TABLES['instagram_users'] = (
        """
        CREATE TABLE IF NOT EXISTS instagram_users (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            user_id VARCHAR(100) NOT NULL UNIQUE,
            username VARCHAR(100) NOT NULL,
            profile_url VARCHAR(255),
            profile_image_url VARCHAR(255),
            profile_image_local VARCHAR(255),
            followers INT,
            posts_count INT,
            is_verified BOOLEAN,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    # Tabel posts
    TABLES['instagram_posts'] = (
        """
        CREATE TABLE IF NOT EXISTS instagram_posts (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            post_id VARCHAR(100) NOT NULL UNIQUE,
            user_id VARCHAR(100) NOT NULL,
            shortcode VARCHAR(100),
            post_url VARCHAR(255),
            content_type VARCHAR(50),
            date_posted DATETIME,
            num_comments INT,
            likes INT,
            image_local_paths TEXT,
            FOREIGN KEY (user_id) REFERENCES instagram_users(user_id) ON DELETE CASCADE
        );
        """
    )

    # Tabel embeddings 
    TABLES['face_embeddings'] = (
        """
        CREATE TABLE IF NOT EXISTS face_embeddings (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            user_id VARCHAR(100) NOT NULL,
            post_id VARCHAR(100) NULL,
            embedding LONGBLOB NOT NULL,
            image_path TEXT,
            source_type ENUM('profile', 'post') NOT NULL DEFAULT 'post',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES instagram_users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES instagram_posts(post_id) ON DELETE CASCADE
        );
        """
    )

    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()

        for table_name, ddl in TABLES.items():
            print(f"Creating table `{table_name}`...", end='')
            cursor.execute(ddl)
            print("OK")

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("🚫 Error: Invalid DB credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("🚫 Error: Database does not exist")
        else:
            print(err)

if __name__ == "__main__":
    create_tables()
