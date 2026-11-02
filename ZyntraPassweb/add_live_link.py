import os
import glob

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "*.html"))

live_link = '        <a href="live.html" class="nav-item">\n            <span class="nav-icon">📡</span>\n            <span>Live</span>\n        </a>'

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue

    # Skip attendee pages that don't have an organizer bottom nav
    if 'attendee_signup' in file_path or 'organizer_signup' in file_path or 'index.html' in file_path:
        continue

    # Only add if bottom-nav exists and Live link is missing
    if 'class="bottom-nav"' not in content and 'bottom-nav' not in content:
        continue
    if 'live.html' in content:
        continue  # Already has the Live link

    # Find the closing </div> of the bottom-nav and insert before it
    # We look for Participants link and add Live right after
    if 'Participants</span>' in content or '>Participants<' in content:
        old = '</a>\n          \n      </div>'
        new = '</a>\n' + live_link + '\n      </div>'
        if old in content:
            content = content.replace(old, new)
        else:
            # Try another common format
            old2 = '>Participants</span>\n          </a>\n          \n      </div>'
            new2 = '>Participants</span>\n          </a>\n' + live_link + '\n      </div>'
            if old2 in content:
                content = content.replace(old2, new2)
            else:
                # Generic: insert before the closing </div> of bottom-nav
                import re
                content = re.sub(
                    r'(Participants</span>\s*</a>\s*)(</div>)',
                    r'\1' + live_link + '\n    ' + r'\2',
                    content,
                    flags=re.IGNORECASE
                )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added Live link to {os.path.basename(file_path)}")
    else:
        print(f"SKIPPED (no Participants link found): {os.path.basename(file_path)}")

print("Done!")
