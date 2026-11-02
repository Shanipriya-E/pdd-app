import os

files = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_dashboard.xml',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_discover.xml'
]

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.replace(
        '<LinearLayout android:id="@+id/navDashboard" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard" />\n        </LinearLayout>',
        '<LinearLayout android:id="@+id/navDashboard" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="⊞" android:textSize="24sp" android:textColor="#3B35A8" android:textStyle="bold" />\n            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard" android:textSize="12sp" android:textColor="#3B35A8" android:textStyle="bold" />\n        </LinearLayout>'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
