import os
import re

files = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDashboardActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeEventsActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeAttendanceActivity.kt'
]

new_nav = """
    private fun setupBottomNav() { 
        findViewById<android.view.View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeDashboardActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navDiscover)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeDiscoverActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navMy)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeEventsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navAttendance)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeAttendanceActivity::class.java))
            finish()
        }
    }
}
"""

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace from private fun setupBottomNav() to the end of the file
        content = re.sub(r'private fun setupBottomNav\(\) \{[\s\S]*$', new_nav.lstrip(), content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")
