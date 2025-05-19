import requests

url = "https://scontent-iad3-2.cdninstagram.com/v/t51.2885-15/479909927_18272819338271946_5743750884517967205_n.jpg?stp=dst-jpg_e35_s1080x1080_sh0.08_tt6&_nc_ht=scontent-iad3-2.cdninstagram.com&_nc_cat=106&_nc_oc=Q6cZ2QHU1GITs5_yqxjKOUxUJGjsWQHS4AXUllCuMuAv39noVlmmfQRLobiccsN9SVjlf-4&_nc_ohc=P6kcFGxgGqUQ7kNvwEnldap&_nc_gid=BxDdxLqRY5rO3BwBPiGs8w&edm=ANTKIIoBAAAA&ccb=7-5&oh=00_AfJpQ_1QaUlox442t_J7pjBYD5IeCjxY8-D54gMBzdG0VA&oe=683092A1&_nc_sid=d885a2"
headers = {
    "Authorization": "Bearer 31f3165f3c61e6c3063bc3ba85fe72a4baa9cb3c58dde9389b8ad66a2cdecca2"
}

response = requests.get(url, headers=headers, verify=False)

if response.status_code == 200:
    with open('image.jpg', 'wb') as f:
        f.write(response.content)
    print("Image downloaded successfully.")
else:
    print(f"Failed to download image. Status code: {response.status_code}")
