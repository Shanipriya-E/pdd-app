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
        with open(file_path, 'r', encoding='utf-16') as f:
            content = f.read()

    original = content

    # Remove top-actions (bell and avatar)
    content = re.sub(r'<div class="top-actions">.*?</div>\s*</div>', '</div>', content, flags=re.DOTALL)
    content = re.sub(r'<div class="top-actions">.*?</div>', '', content, flags=re.DOTALL) # Fallback

    # Remove "More" from bottom nav
    content = re.sub(r'<a[^>]*nav-item[^>]*>\s*<span[^>]*>.*?</span>\s*More\s*</a>', '', content, flags=re.IGNORECASE)

    if content != original:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            with open(file_path, 'w', encoding='utf-16') as f:
                f.write(content)
        print(f"Removed icons from {os.path.basename(file_path)}")

print("Done removing icons from web app!")
