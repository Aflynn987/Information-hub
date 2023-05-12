import requests

url = "https://www.theguardian.com/media/2023/may/11/cnn-chris-licht-trump-town-hall"
response = requests.get(url)
if response.status_code == 200:
    print(response.text)
else:
    print("Error: Unable to retrieve HTML content from URL")