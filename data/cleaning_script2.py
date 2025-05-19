import json
import pandas as pd

# Load your raw JSON data
with open('data/dataset.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Container for cleaned data
cleaned_data = []

for post in raw_data:
    # Extract only the fields you need
    cleaned_post = {
        'url': post.get('url'),
        'user_posted': post.get('user_posted'),
        'description': post.get('description', ''),
        'hashtags': post.get('hashtags') if post.get('hashtags') else [],
        'num_comments': post.get('num_comments', 0),
        'date_posted': post.get('date_posted'),
        'likes': post.get('likes', 0),
        'photos': post.get('photos', []),
        'is_verified': post.get('is_verified', False),  # Add is_verified parameter
        'followers': post.get('followers', 0)  # Add followers count
    }
    
    # Filter out posts without photos — only keep posts that include at least one image
    if cleaned_post['photos']:
        cleaned_data.append(cleaned_post)

# Convert to DataFrame for easier use
df = pd.DataFrame(cleaned_data)

# Optional: convert date_posted to datetime type (better for sorting/filtering later)
df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')

# Save cleaned data to CSV for later use, simpan clean data set dalam bentuk csv
df.to_csv('cleaned_instagram_data.csv', index=False)

print("Data cleaning complete! Cleaned dataset saved as 'cleaned_instagram_data.csv'")


