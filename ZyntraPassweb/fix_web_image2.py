import os
import re

filepath = 'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/event_detail.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix banner-placeholder garbled text
content = re.sub(r'<div class="banner-placeholder">.*?</div', '<div class="banner-placeholder">🖼️</div', content)

new_js = """        // Banner
        if (ev.banner_image_url && ev.banner_image_url !== 'null') {
            document.getElementById('bannerContainer').innerHTML = `<img src="${ev.banner_image_url}" class="event-banner" alt="Banner">`;
        } else {
            document.getElementById('bannerContainer').innerHTML = `<img src="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200" class="event-banner" alt="Banner">`;
        }"""

content = re.sub(r'if\s*\(ev\.banner_image_url\)\s*\{\s*document\.getElementById\(\'bannerContainer\'\)\.innerHTML\s*=\s*`<img src="\$\{ev\.banner_image_url\}"[^>]*>`;\s*\}', new_js, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed web app image logic for event_detail.html")
