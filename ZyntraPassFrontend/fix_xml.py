import os

files = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_dashboard.xml',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_discover.xml'
]

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.replace('android:text="Dashboard"\n        </LinearLayout>', 'android:text="Dashboard" />\n        </LinearLayout>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
