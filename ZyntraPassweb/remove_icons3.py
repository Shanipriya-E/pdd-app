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

    # 1. Remove the entire <a ...> ... More ... </a> from the bottom nav
    # The bottom nav is usually inside <div class="bottom-nav">
    # We will just replace any line that contains class="nav-item" and "More"
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'class="nav-item"' in line and 'More' in line:
            continue
        new_lines.append(line)
    content = '\n'.join(new_lines)

    # 2. Also ensure top-actions are completely gone
    content = re.sub(r'<div class="top-actions">.*?</div>\s*</div>', '</div>', content, flags=re.DOTALL)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned up More and top-actions in {os.path.basename(file_path)}")

print("Done cleaning up Web icons!")
