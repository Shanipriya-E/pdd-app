import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/CreateEventActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

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
if "fun setupBottomNav()" not in content:
    # insert before end of class
    content = content[:content.rfind('}')] + f"""
    private fun setupBottomNav() {{ {bottom_nav} }}
""" + "\n}"
    # call it in onCreate
    content = re.sub(r'(setContentView\(R\.layout\.activity_create_event\))', r'\1\n        setupBottomNav()', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Added setupBottomNav")
