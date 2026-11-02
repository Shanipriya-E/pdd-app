import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_create_event.xml'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace linearly to be safe
content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Dashboard"[^>]*>',
                 r'<LinearLayout android:id="@+id/navDashboard" android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard" android:textColor="#5B54E3" android:textSize="11sp" android:textStyle="bold" android:layout_marginTop="2dp" />', content)

content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Events"[^>]*>',
                 r'<LinearLayout android:id="@+id/navEvents" android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Events" android:textColor="#4A5568" android:textSize="11sp" android:layout_marginTop="2dp" />', content)

content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Participants"[^>]*>',
                 r'<LinearLayout android:id="@+id/navParticipants" android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Participants" android:textColor="#4A5568" android:textSize="11sp" android:layout_marginTop="2dp" />', content)

content = re.sub(r'<LinearLayout android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\s*(<TextView[^>]+>)\s*<TextView[^>]+text="Live"[^>]*>',
                 r'<LinearLayout android:id="@+id/navLive" android:layout_width="0dp" android:layout_height="match_parent" android:layout_weight="1" android:orientation="vertical" android:gravity="center_horizontal">\n            \1\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Live" android:textColor="#4A5568" android:textSize="11sp" android:layout_marginTop="2dp" />', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
