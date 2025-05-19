import json
from datetime import datetime

# Load raw JSON data
with open('data/dataset.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Container for cleaned data
cleaned_data = []

for post in raw_data:
    cleaned_post = {
        'url': post.get('url'),
        'user_posted': post.get('user_posted'),
        'description': post.get('description', ''),
        'hashtags': post.get('hashtags') if post.get('hashtags') else [],
        'num_comments': post.get('num_comments', 0),
        'date_posted': post.get('date_posted'),
        'likes': post.get('likes', 0),
        'photos': post.get('photos', []),
        'is_verified': post.get('is_verified', False),
        'followers': post.get('followers', 0)
    }

   # Filter out posts without photos — only keep posts that include at least one image
    if cleaned_post['photos']:
        cleaned_data.append(cleaned_post)

# Save cleaned data to JSON
with open('cleaned_instagram_data2.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print("Data cleaning complete! Cleaned dataset saved as 'cleaned_instagram_data.json'")
