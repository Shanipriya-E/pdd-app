import os
import glob

directory = "c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb"
html_files = glob.glob(os.path.join(directory, "attendee_*.html"))

for file_path in html_files:
    if 'attendee_dashboard' in file_path:
        continue  # Already fixed
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue

    original = content

    # Replace: sb.from('attendee_profiles') with profiles
    content = content.replace("sb.from('attendee_profiles')", "sb.from('profiles')")
    content = content.replace('sb.from("attendee_profiles")', 'sb.from("profiles")')

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed attendee_profiles ref in {os.path.basename(file_path)}")

print("Done!")
