import requests
url='https://forocoches.substack.com/p/14-anos-sin-andres-montes-filtran'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
html = requests.get(url, headers=headers).text
print(html)