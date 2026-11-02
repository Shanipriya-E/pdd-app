import os
import glob
import re

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "*.html"))

# Pattern: direct getElementById for removed elements without null check
patterns_to_fix = [
    "profile-avatar",
    "userAvatar",
    "btnNotifications",
]

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue

    original = content

    for elem_id in patterns_to_fix:
        # Replace: document.getElementById('X').textContent = ...
        # With: const _el_X = document.getElementById('X'); if(_el_X) _el_X.textContent = ...
        # But only if it's a direct .textContent or .innerHTML assignment without null check
        content = re.sub(
            rf"document\.getElementById\(['\"]({elem_id})['\"]\)\.(textContent|innerHTML)\s*=",
            rf"(document.getElementById('\1') || {{}}).\2 =",
            content
        )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed null refs in {os.path.basename(file_path)}")

print("Done!")
