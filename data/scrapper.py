#ini untuk scrape data dari bright data
import requests

url = "https://api.brightdata.com/datasets/v3/trigger"
headers = {
	"Authorization": "Bearer fa2dd8ca70f3d34bcd6195069d3fb61f111674ef59ee6c9837cbb3b8ce49c9b0",
	"Content-Type": "application/json",
}
params = {
	"dataset_id": "gd_lk5ns7kz21pck8jpis",
	"include_errors": "true",
	"type": "discover_new",
	"discover_by": "url",
}
data = {
	"input": [{"url":"https://www.instagram.com/marcusfaberfdp","num_of_posts":10,"start_date":"01-01-2025","end_date":"03-01-2025","post_type":"Post"},{"url":"https://www.instagram.com/meta/","num_of_posts":"","posts_to_not_include":["3529568342229145484"],"start_date":"03-01-2025","end_date":"03-17-2025","post_type":"Reel"},{"url":"https://www.instagram.com/skintificid/tagged/","num_of_posts":5,"post_type":"Post","start_date":"","end_date":""}],
	"custom_output_fields": ["url","user_posted","num_comments","date_posted","likes","photos","post_id","content_type","followers","posts_count","profile_image_link","is_verified","user_posted_id","post_content","profile_url","images","photos_number","timestamp","error_code","warning","warning_code","shortcode"],
}

response = requests.post(url, headers=headers, params=params, json=data)
print(response.json())