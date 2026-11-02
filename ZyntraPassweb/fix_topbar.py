import os
import glob
import re

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "*.html"))

for file_path in html_files:
    if os.path.basename(file_path) == 'dashboard.html':
        continue  # already fixed manually
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue

    original = content

    # Fix broken top-bar:
    # Pattern 1: menu-btn followed by orphan closing divs and avatar/bell
    # We want to replace anything like:
    # <div class="top-bar">
    #     <button ...>☰</button>
    #     </div>     <- orphan
    #     <div class="...avatar...">...</div>  <- leftover
    #     </div>     <- orphan
    # </div>
    # With just:
    # <div class="top-bar">
    #     <button ...>☰</button>
    # </div>

    content = re.sub(
        r'(<div class="top-bar">\s*<button class="menu-btn">[^<]*</button>)\s*</div>\s*<div[^>]*(?:avatar|bell|profile)[^>]*>.*?</div>\s*</div>\s*</div>',
        r'\1\n    </div>',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Simpler fallback: just remove any line with profile-avatar that's not in sidebar
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # Remove leftover orphan avatar divs from top-bar (not sidebar-avatar)
        if 'id="profile-avatar"' in stripped or 'id="userAvatar"' in stripped:
            if 'sidebar' not in stripped and 'top-bar' not in stripped:
                continue
        new_lines.append(line)
    content = '\n'.join(new_lines)

    # Also remove orphan stray </div></div> after menu-btn
    # These look like:  </button>\n        </div>\n            <div ...>...</div>\n        </div>\n    </div>
    # We just want:  </button>\n    </div>

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed top-bar in {os.path.basename(file_path)}")

print("Done!")
