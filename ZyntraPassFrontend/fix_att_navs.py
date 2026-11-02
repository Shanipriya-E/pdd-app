import os
import re

kt_files = [
    'AttendeeDashboardActivity.kt',
    'AttendeeDiscoverActivity.kt'
]
base_kt = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/'

bottom_nav = """
        findViewById<android.view.View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeDashboardActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navDiscover)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeDiscoverActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navMy)?.setOnClickListener {
            android.widget.Toast.makeText(this, "My Events coming soon", android.widget.Toast.LENGTH_SHORT).show()
        }
        findViewById<android.view.View>(R.id.navAttendance)?.setOnClickListener {
            android.widget.Toast.makeText(this, "Attendance history coming soon", android.widget.Toast.LENGTH_SHORT).show()
        }
"""

for kt in kt_files:
    path = os.path.join(base_kt, kt)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing navDiscover click listener to prevent conflicts
    content = re.sub(r'findViewById<android\.view\.View>\(R\.id\.navDiscover\)\?\.setOnClickListener\s*\{[^}]*\}', '', content)
    
    if "fun setupBottomNav()" not in content:
        content = re.sub(r'(setContentView\(R\.layout\.[^)]+\))', r'\1\n        setupBottomNav()', content)
        func = f"""
    private fun setupBottomNav() {{ {bottom_nav} }}
"""
        content = content[:content.rfind('}')] + func + "\n}"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Done Attendee")
