import requests

url = "https://www.rte.ie/news/business/2023/0510/1382716-retailers/"
response = requests.get(url)
if response.status_code == 200:
    print(response.text)
else:
    print("Error: Unable to retrieve HTML content from URL")