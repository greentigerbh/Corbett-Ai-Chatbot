import urllib.request
import urllib.parse
import json
import re
import time

def get_wikimedia_image(query):
    try:
        search_url = f'https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srsearch={urllib.parse.quote(query + " filetype:bitmap")}&utf8=&format=json&srlimit=5'
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            search_results = data.get('query', {}).get('search', [])
            
            for res in search_results:
                title = res['title']
                if not (title.lower().endswith('.jpg') or title.lower().endswith('.jpeg') or title.lower().endswith('.png')):
                    continue
                
                info_url = f'https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json'
                req2 = urllib.request.Request(info_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req2) as response2:
                    data2 = json.loads(response2.read().decode())
                    pages = data2.get('query', {}).get('pages', {})
                    for page_id, page_info in pages.items():
                        if 'imageinfo' in page_info:
                            return page_info['imageinfo'][0]['url']
        return None
    except Exception as e:
        print(f'Error fetching image for {query}: {e}')
        return None

queries = {
    'Devbhoomi Outdoor Adventure Park in Ramnagar': 'zipline adventure park',
    'Starscapes Observatory Corbett night sky': 'night sky stars astrophotography',
    'Falcon Drop bungee jump': 'bungee jumping',
    'Panther Edge rooftop bungee': 'bungee jump adventure',
    'Riverside camping': 'tents camping riverside',
    'Birdwatching in the forest': 'kingfisher bird india',
    'Nature walk path': 'forest trail walking india',
    'Cycling trail': 'mountain biking forest trail',
    'Forest edge café': 'outdoor cafe nature',
    'Bonfire evening': 'campfire bonfire night',
    'Kosi river picnic': 'picnic by river',
    'Outdoor photography spot': 'nature photography landscape',
    'Secret Trail': 'dense forest trail jungle',
    'Detail view': 'jungle leaf macro',
    'Map Background': 'topographic map terrain'
}

html_file = 'g:/gagan/uncle_bot/nearby.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

for alt_text, query in queries.items():
    print(f'Searching for: {alt_text}...')
    img_url = get_wikimedia_image(query)
    if img_url:
        print(f'  Found: {img_url}')
        tag_pattern = re.compile(r'<img[^>]+alt="' + re.escape(alt_text) + r'"[^>]*>', re.DOTALL | re.IGNORECASE)
        match = tag_pattern.search(html)
        if match:
            tag = match.group(0)
            new_tag = re.sub(r'src="[^"]+"', f'src="{img_url}"', tag)
            html = html.replace(tag, new_tag)
        else:
            print(f'  Warning: img tag with alt="{alt_text}" not found.')
    else:
        print(f'  No image found for {query}')
    time.sleep(1)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done updating images!')
