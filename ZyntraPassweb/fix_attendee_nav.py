import os
import glob
import re

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "attendee_*.html"))

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue

    original = content

    # Fix bottom nav attendance link
    content = re.sub(
        r'<a href="#" class="nav-item">([^<]*)<span class="nav-icon">([^<]*)</span><span>Attendance</span></a>',
        r'<a href="attendee_attendance.html" class="nav-item">\1<span class="nav-icon">\2</span><span>Attendance</span></a>',
        content
    )
    
    # Also catch cases without nav-icon span just in case, or different ordering
    content = re.sub(
        r'<a href="#" class="nav-item">([\s\S]*?)<span>Attendance</span></a>',
        r'<a href="attendee_attendance.html" class="nav-item">\1<span>Attendance</span></a>',
        content
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed attendance link in {os.path.basename(file_path)}")

print("Done!")
