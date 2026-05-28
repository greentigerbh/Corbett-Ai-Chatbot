import os
import re
import time
import urllib.request
import urllib.error

# Ensure directory exists
os.makedirs('assets/images', exist_ok=True)

with open('nearby.html', 'r', encoding='utf-8') as f:
    html = f.read()

urls = list(set(re.findall(r'src="(https://commons\.wikimedia\.org/wiki/Special:FilePath/[^"]+)"', html)))
urls += list(set(re.findall(r'src="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+)"', html)))

print(f"Found {len(urls)} distinct images to download.")

for url in urls:
    # get filename from url
    if 'Special:FilePath' in url:
        filename = url.split('/')[-1].split('?')[0]
    else:
        filename = url.split('/')[-1]
    
    # URL decode filename to avoid weird chars
    import urllib.parse
    filename = urllib.parse.unquote(filename)
    # clean filename
    filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c in '._- ']).rstrip()
    
    filepath = f"assets/images/{filename}"
    
    if os.path.exists(filepath):
        print(f"Skipping {filename}, already downloaded.")
        # replace in html
        html = html.replace(url, filepath)
        continue

    print(f"Downloading {filename}...")
    
    success = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                with open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            success = True
            print("  Success")
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("  Rate limited, sleeping 5 seconds...")
                time.sleep(5)
            else:
                print(f"  HTTP Error {e.code}")
                break
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(2)
            
    if success:
        # Replace the url in html with local path
        html = html.replace(url, filepath)
    
    time.sleep(1)

with open('nearby.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Done!")
