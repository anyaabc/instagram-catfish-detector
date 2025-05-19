import requests

url = "https://api.brightdata.com/datasets/v3/snapshots"
headers = {
	"Authorization": "Bearer fa2dd8ca70f3d34bcd6195069d3fb61f111674ef59ee6c9837cbb3b8ce49c9b0",
}
params = {
	"dataset_id": "gd_lk5ns7kz21pck8jpis",
	"status": "ready",
}

response = requests.get(url, headers=headers, params=params)
print(response.json())