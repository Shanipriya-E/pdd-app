import os
import glob
import re

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "*.html"))

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue

    original = content

    content = re.sub(r'<a href="#" class="nav-item">\s*<span class="nav-icon">.*?</span>\s*<span>More</span>\s*</a>', '', content, flags=re.IGNORECASE|re.DOTALL)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned up multi-line More in {os.path.basename(file_path)}")

print("Done cleaning up multi-line More!")
