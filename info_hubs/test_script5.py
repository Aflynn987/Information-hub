from urllib.parse import urlparse

url1 = 'https://www.rte.ie/'
url2 = 'https://www.theguardian.com'
url3 = 'https://www.theamericanconservative.com/'
url4 = 'https://www.dailykos.com/'
domain_name = urlparse(url4).netloc.split('.')[1]
# domain_name = ' '.join(word.capitalize() for word in parsed_url.split('-'))
# parsed_url = urlparse(url2)
# domain_name = parsed_url.netloc.split('.')[1].replace('-', ' ')
print(domain_name)