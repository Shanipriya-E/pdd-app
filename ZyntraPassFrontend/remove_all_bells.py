import os
import re

base_xml = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/'
xml_files = [f for f in os.listdir(base_xml) if f.endswith('.xml')]

for xml in xml_files:
    path = os.path.join(base_xml, xml)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Very flexible regex for the bell icon RelativeLayout
    # Matches <RelativeLayout ...> ... <TextView text="emoji" /> <TextView text="2" /> ... </RelativeLayout>
    new_content = re.sub(r'<RelativeLayout[^>]*layout_marginEnd="16dp"[^>]*>[\s\S]*?<TextView[^>]*textSize="24sp"[^>]*/>[\s\S]*?<TextView[^>]*text="2"[^>]*/>[\s\S]*?</RelativeLayout>', '', content)
    
    # Another pattern just in case the "2" isn't there or it's formatted differently
    new_content = re.sub(r'<RelativeLayout[^>]*layout_marginEnd="16dp"[^>]*>\s*<TextView[^>]*textSize="24sp"[^>]*/>\s*(<TextView[^>]*/>)?\s*</RelativeLayout>', '', new_content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed bell from {xml}")

print("Done removing bells.")
