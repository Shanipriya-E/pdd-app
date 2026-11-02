import os
import glob
import re

directory = "c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout"
xml_files = glob.glob(os.path.join(directory, "*.xml"))

for file_path in xml_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # Fix the trailing slash error: `/ android:visibility="gone">` -> `android:visibility="gone" />`
    content = content.replace('/ android:visibility="gone">', 'android:visibility="gone" />')
    
    # Fix the LinearLayout error: `> android:visibility="gone">`
    # We want `<LinearLayout android:visibility="gone" ...>`
    content = re.sub(r'<LinearLayout([^>]*)>\s*android:visibility="gone">', r'<LinearLayout android:visibility="gone"\1>', content)
    
    # Fix `<LinearLayout ... >\n<TextView .../><TextView ... text="More"/></LinearLayout> android:visibility="gone">`?
    # No, the previous regex was:
    # r'\1 android:visibility="gone">\n<TextView...'
    # If the regex outputted `android:visibility="gone">`, we just need to clean it up.
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed XML syntax in {os.path.basename(file_path)}")

print("Done fixing XML!")
