import os
import re

base_kt = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/'
base_xml = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/'

kt_files = [f for f in os.listdir(base_kt) if f.endswith('.kt')]
xml_files = [f for f in os.listdir(base_xml) if f.endswith('.xml')]

# 1. Remove Bell Icon from all XML files
for xml in xml_files:
    path = os.path.join(base_xml, xml)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove bell icon block
    new_content = re.sub(r'<RelativeLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginEnd="16dp">\s*<TextView[^>]*>\s*<TextView[^>]*>\s*</RelativeLayout>', '', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed bell from {xml}")

# 2. Add Nav IDs for Organizer screens
organizer_xmls = [
    'activity_settings.xml', 
    'activity_certificates.xml', 
    'activity_volunteers.xml',
    'activity_participant_detail.xml'
]
for xml in organizer_xmls:
    path = os.path.join(base_xml, xml)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    # Dashboard
    content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*<TextView[^>]*text="Dashboard"',
                     r'<LinearLayout android:id="@+id/navDashboard" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard"', content)
    content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Dashboard"[^>]+>',
                     r'<LinearLayout android:id="@+id/navDashboard" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', content)

    # Events
    content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Events"[^>]+>',
                     r'<LinearLayout android:id="@+id/navEvents" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Events" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', content)

    # Participants
    content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Participants"[^>]+>',
                     r'<LinearLayout android:id="@+id/navParticipants" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Participants" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', content)

    # Live
    content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Live"[^>]+>',
                     r'<LinearLayout android:id="@+id/navLive" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Live" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', content)

    if original != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added Nav IDs to {xml}")

# 3. Add setupBottomNav to Organizer Activities
organizer_kts = [
    'SettingsActivity.kt',
    'CertificatesActivity.kt',
    'VolunteersActivity.kt',
    'ParticipantDetailActivity.kt'
]

bottom_nav = """
        findViewById<android.view.View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(android.content.Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navEvents)?.setOnClickListener {
            startActivity(android.content.Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navParticipants)?.setOnClickListener {
            startActivity(android.content.Intent(this, ParticipantsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navLive)?.setOnClickListener {
            startActivity(android.content.Intent(this, LiveAttendanceActivity::class.java))
            finish()
        }
"""

for kt in organizer_kts:
    path = os.path.join(base_kt, kt)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "fun setupBottomNav()" not in content and "setContentView" in content:
        content = re.sub(r'(setContentView\(R\.layout\.[^)]+\))', r'\1\n        setupBottomNav()', content)
        func = f"""
    private fun setupBottomNav() {{ {bottom_nav} }}
"""
        content = content[:content.rfind('}')] + func + "\n}"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added setupBottomNav to {kt}")

print("Done all updates.")
