import urllib.request
import re

with open('g:/gagan/uncle_bot/nearby.html', 'r', encoding='utf-8') as f:
    html = f.read()

urls = re.findall(r'src="(https://[^"]+)"', html)
for url in set(urls):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        res = urllib.request.urlopen(req, timeout=5)
        print(f'OK: {url}')
    except Exception as e:
        print(f'FAIL: {url} - {e}')
