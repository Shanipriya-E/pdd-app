import os
import re

xml_files = [
    'activity_organizer_dashboard.xml',
    'activity_events.xml',
    'activity_participants.xml',
    'activity_live_attendance.xml',
    'activity_create_event.xml'
]
base_xml = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/'

for xml in xml_files:
    path = os.path.join(base_xml, xml)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove bell icon block
    content = re.sub(r'<RelativeLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginEnd="16dp">\s*<TextView[^>]*>\s*<TextView[^>]*>\s*</RelativeLayout>', '', content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
