import os
import re

app_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main"
res_dir = os.path.join(app_dir, r"res\layout")

def add_to_sidebar(xml_file):
    filepath = os.path.join(res_dir, xml_file)
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        xml = f.read()
    
    if 'navSidebarCertificates' in xml:
        return
        
    cert_item = '                <TextView android:id="@+id/navSidebarCertificates" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="&#128220;   Certificates" android:textColor="#E2E8F0" android:padding="16dp" android:textSize="14sp" android:textStyle="bold" />\n'
    
    xml = xml.replace('android:id="@+id/navSidebarSettings"', cert_item + '                <TextView android:id="@+id/navSidebarSettings"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(xml)

add_to_sidebar('activity_organizer_dashboard.xml')
add_to_sidebar('activity_attendee_dashboard.xml')
print("XML sidebars updated")
