import re

files = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_dashboard.xml',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_discover.xml'
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Remove bell icon
    text = re.sub(r'<RelativeLayout android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginEnd="16dp">\s*<TextView.*?>\s*<TextView.*?>\s*</RelativeLayout>', '', text, flags=re.DOTALL)
    
    # Add IDs to nav items if missing
    # Dashboard
    text = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*<TextView.*?text="Dashboard".*?>', 
                  r'<LinearLayout android:id="@+id/navDashboard" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard"', text, flags=re.DOTALL)
    
    # Dashboard in discover might have the icon before the text
    text = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Dashboard"[^>]+>',
                  r'<LinearLayout android:id="@+id/navDashboard" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', text)
    
    # Discover in dashboard has ID navDiscover, but in discover it might not?
    text = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Discover"[^>]+>',
                  r'<LinearLayout android:id="@+id/navDiscover" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Discover" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', text)

    # My
    text = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="My"[^>]+>',
                  r'<LinearLayout android:id="@+id/navMy" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="My" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', text)
    
    # Attendance
    text = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Attendance"[^>]+>',
                  r'<LinearLayout android:id="@+id/navAttendance" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Attendance" android:textSize="12sp" android:textColor="#64748B" android:textStyle="bold" />', text)
                  
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
