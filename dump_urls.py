import re
with open('g:/gagan/uncle_bot/nearby.html', 'r', encoding='utf-8') as f:
    html = f.read()
urls = re.findall(r'src="(.*?)"', html)
for url in urls:
    if 'wiki' in url.lower():
        print(url)
