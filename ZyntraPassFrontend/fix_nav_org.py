import os
import re

kt_files = [
    'OrganizerDashboardActivity.kt',
    'EventsActivity.kt',
    'ParticipantsActivity.kt',
    'LiveAttendanceActivity.kt',
    'CreateEventActivity.kt'
]

xml_files = [
    'activity_organizer_dashboard.xml',
    'activity_events.xml',
    'activity_participants.xml',
    'activity_live_attendance.xml',
    'activity_create_event.xml'
]

base_kt = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/'
base_xml = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/'

for xml in xml_files:
    path = os.path.join(base_xml, xml)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
                     
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for kt in kt_files:
    path = os.path.join(base_kt, kt)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to add bottom nav listeners securely at the end of onCreate
    listeners = """
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
    # Remove existing ones to avoid duplication
    content = re.sub(r'findViewById<View>\(R\.id\.navDashboard\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    content = re.sub(r'findViewById<View>\(R\.id\.navEvents\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    content = re.sub(r'findViewById<View>\(R\.id\.navParticipants\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    content = re.sub(r'findViewById<View>\(R\.id\.navLive\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    
    # Same with android.view.View
    content = re.sub(r'findViewById<android\.view\.View>\(R\.id\.navDashboard\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    content = re.sub(r'findViewById<android\.view\.View>\(R\.id\.navEvents\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    content = re.sub(r'findViewById<android\.view\.View>\(R\.id\.navParticipants\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    content = re.sub(r'findViewById<android\.view\.View>\(R\.id\.navLive\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    
    # insert before the last closing brace of onCreate.
    # A bit risky to regex, better to find the end of onCreate. But we can just append it before `loadData()` or at the end of onCreate.
    pass # I'll do this carefully per file.

print("Done XML")
