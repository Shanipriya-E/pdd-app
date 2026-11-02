import os
import glob
import re

directory = "c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout"
xml_files = glob.glob(os.path.join(directory, "*.xml"))

for file_path in xml_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. Hide tvAvatar or tvUserAvatar
    # Look for the opening tag of tvAvatar or tvUserAvatar and add visibility
    content = re.sub(
        r'(<TextView[^>]*android:id="@+id/tv(?:User)?Avatar"[^>]*)>',
        r'\1 android:visibility="gone">', 
        content
    )

    # 2. Hide btnNotifications (bell)
    content = re.sub(
        r'(<(?:ImageView|TextView)[^>]*android:id="@+id/(?:btn)?Notifications"[^>]*)>',
        r'\1 android:visibility="gone">', 
        content
    )
    
    # 3. Also hide any explicit notification icons if they don't have that ID but have an obvious drawable
    content = re.sub(
        r'(<ImageView[^>]*android:src="@android:drawable/ic_dialog_info"[^>]*)>',
        r'\1 android:visibility="gone">', 
        content
    )

    # 4. Hide "More" LinearLayout from bottom nav
    # The block looks like <LinearLayout ...> ... "More" ... </LinearLayout>
    # We can match it if it has weight="1" and contains "More"
    content = re.sub(
        r'(<LinearLayout[^>]*android:layout_weight="1"[^>]*>)\s*<TextView[^>]*>\s*<TextView[^>]*android:text="More"[^>]*>\s*</LinearLayout>',
        r'\1 android:visibility="gone">\n<TextView android:layout_width="wrap_content" android:layout_height="wrap_content"/><TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="More"/></LinearLayout>',
        content, flags=re.IGNORECASE|re.DOTALL
    )
    
    # Actually, setting visibility on the LinearLayout is much easier if we just match it carefully
    def hide_more_block(match):
        block = match.group(0)
        if 'visibility="gone"' not in block:
            return block.replace('<LinearLayout ', '<LinearLayout android:visibility="gone" ')
        return block

    content = re.sub(r'<LinearLayout[^>]*android:layout_weight="1"[^>]*>[\s\S]*?android:text="More"[\s\S]*?</LinearLayout>', hide_more_block, content, flags=re.IGNORECASE)

    # Note: Because the regex might have added visibility twice, let's just make sure.
    # It's fine for now, Android parses it or ignores duplicates if we don't do it blindly.
    # Wait, XML parser throws error if duplicated attributes!
    # Let's clean up duplicate visibility="gone":
    content = content.replace('android:visibility="gone" android:visibility="gone"', 'android:visibility="gone"')

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Removed icons from {os.path.basename(file_path)}")

print("Done removing icons from Android app!")
