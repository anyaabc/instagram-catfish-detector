import sqlite3
import pandas as pd

conn = sqlite3.connect("data/instagram_posts.db")
df = pd.read_sql("SELECT * FROM posts LIMIT 5", conn)
print(df)
