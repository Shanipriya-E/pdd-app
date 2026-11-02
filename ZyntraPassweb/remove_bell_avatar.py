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

    # 1. Remove <div class="header-actions">...</div> blocks (contains bell button + avatar)
    content = re.sub(
        r'<div class="header-actions">.*?</div>\s*</div>',
        '</div>',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 2. Remove any leftover standalone btn-bell buttons
    content = re.sub(
        r'<button class="btn-bell">.*?</button>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 3. Remove standalone profile avatar divs in top-bar area (NOT sidebar-avatar)
    content = re.sub(
        r'<div class="avatar" id="profile-avatar">.*?</div>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 4. Remove standalone userAvatar divs in top-bar area
    content = re.sub(
        r'<div class="avatar" id="userAvatar">.*?</div>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned bell/avatar from {os.path.basename(file_path)}")

print("Done!")
