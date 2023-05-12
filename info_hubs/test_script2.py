import requests

url = "https://www.theamericanconservative.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print(response.text)
else:
    print("Error: Unable to retrieve HTML content from URL")