import os
import re

files = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeEventsActivity.kt'
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the dialog code for btnView and replace it
    pattern = r'btnView\.setOnClickListener\s*\{[\s\S]*?\.show\(\)\s*\}'
    
    new_code = """btnView.setOnClickListener {
                val intent = android.content.Intent(this, EventDetailActivity::class.java)
                intent.putExtra("eventId", eventId)
                intent.putExtra("isRegistered", isRegistered)
                startActivity(intent)
            }"""
            
    content = re.sub(pattern, new_code, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")
