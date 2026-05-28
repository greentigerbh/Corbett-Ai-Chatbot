import os
import glob

# Rename the malformed Cafe image
for f in glob.glob('assets/images/Outdoor_Caf*'):
    if f != 'assets/images/Outdoor_Cafe.jpg':
        os.rename(f, 'assets/images/Outdoor_Cafe.jpg')
        print(f"Renamed {f} to Outdoor_Cafe.jpg")

with open('g:/gagan/uncle_bot/nearby.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the cafe HTML reference
import re
html = re.sub(r'assets/images/Outdoor_Caf[^"]+', 'assets/images/Outdoor_Cafe.jpg', html)

# Fix the tenting HTML reference which failed to download
# We'll use Campfire_and_sparks_in_Anttoora_3.jpg for Riverside Camping as a fallback
html = html.replace('https://commons.wikimedia.org/wiki/Special:FilePath/Tenting_on_the_Old_Camp_Ground_-_Project_Gutenberg_eText_21566.png?width=800', 'assets/images/Campfire_and_sparks_in_Anttoora_3.jpg')
html = html.replace('https://upload.wikimedia.org/wikipedia/commons/c/cc/Tenting_on_the_Old_Camp_Ground_-_Project_Gutenberg_eText_21566.png', 'assets/images/Campfire_and_sparks_in_Anttoora_3.jpg')

with open('g:/gagan/uncle_bot/nearby.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Fixed remaining image issues.")
