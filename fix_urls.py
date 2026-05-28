import re

with open('g:/gagan/uncle_bot/nearby.html', 'r', encoding='utf-8') as f:
    html = f.read()

def replace_url(match):
    full_url = match.group(1)
    # Extract filename from the end of the URL
    filename = full_url.split('/')[-1]
    # Construct the Special:FilePath URL
    new_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}?width=800"
    print(f"Replaced: {filename}")
    return f'src="{new_url}"'

# Make sure to catch both src="..." cases.
# In nearby.html we might have multiple matches
new_html, count = re.subn(r'src="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+)"', replace_url, html)

print(f"Total replaced: {count}")

with open('g:/gagan/uncle_bot/nearby.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
