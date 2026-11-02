import os
import glob
import re

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "*.html"))

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='utf-16') as f:
                content = f.read()
        except Exception:
            continue

    original = content

    # Remove top-actions (bell and avatar) which contains nested divs
    # We can match up to the end of the avatar div.
    content = re.sub(r'<div class="top-actions">\s*<div class="bell-icon">.*?</div>\s*<div class="avatar"[^>]*>.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    
    # Just in case they are slightly different
    content = re.sub(r'<div class="top-actions">[\s\S]*?<div class="avatar"[^>]*>[\s\S]*?</div>\s*</div>', '', content, flags=re.IGNORECASE)

    # Remove "More" from bottom nav
    content = re.sub(r'<a[^>]*nav-item[^>]*>\s*<span[^>]*>.*?</span>\s*More\s*</a>', '', content, flags=re.IGNORECASE)

    if content != original:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Removed icons from {os.path.basename(file_path)}")
        except Exception:
            pass

print("Done removing icons from web app!")
