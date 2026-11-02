import os
import glob
import re

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "*.html"))

menu_js = """
    // Global Sidebar and Menu logic injected by update script
    document.addEventListener("DOMContentLoaded", () => {
        const menuBtn = document.querySelector('.menu-btn');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');

        if (menuBtn && sidebar && overlay) {
            menuBtn.addEventListener('click', () => {
                sidebar.classList.add('active');
                overlay.classList.add('active');
            });
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('active');
                overlay.classList.remove('active');
            });
        }
    });
"""

for file_path in html_files:
    if os.path.basename(file_path) in ['index.html', 'temp_script.html', 'attendee_dashboard.html', 'attendee_attendance.html', 'attendee_discover.html', 'attendee_my_events.html', 'attendee_event_detail.html']:
        continue # Skip attendee and login files

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Fix Live link in bottom nav
    content = re.sub(r'<a\s+href="[^"]*"\s+class="nav-item(\s+active)?"\s*>(\s*<span[^>]*>.*?</span>\s*)*Live\s*</a>', 
                     r'<a href="live.html" class="nav-item\1">\2Live</a>', content, flags=re.IGNORECASE)

    # 2. Fix Live link in sidebar
    content = re.sub(r'<a\s+href="[^"]*"\s+class="sidebar-item(\s+active)?"\s*>(\s*<span[^>]*>.*?</span>\s*)*Live Attendance\s*</a>', 
                     r'<a href="live.html" class="sidebar-item\1">\2Live Attendance</a>', content, flags=re.IGNORECASE)

    # 3. Add sidebar toggle logic if missing
    if "menuBtn.addEventListener" not in content and "<script>" in content:
        # Find the last </script> tag
        parts = content.rsplit('</script>', 1)
        if len(parts) == 2:
            content = parts[0] + menu_js + '</script>' + parts[1]

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(file_path)}")

print("Done fixing navigation issues!")
