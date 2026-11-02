import os

kt_files = [
    'OrganizerDashboardActivity.kt',
    'EventsActivity.kt',
    'ParticipantsActivity.kt',
    'LiveAttendanceActivity.kt'
]
base_kt = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/'

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

for kt in kt_files:
    path = os.path.join(base_kt, kt)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If already added, skip
    if "R.id.navLive" in content and "LiveAttendanceActivity::class.java" in content:
        # maybe navDashboard is missing?
        if "R.id.navDashboard" not in content:
            content = content.replace('setContentView(', 'setContentView(') # anchor
            # just inject at the end of onCreate roughly... 
            # I'll just append before the last '}' of onCreate. Since it's hard with regex, I'll use a hack:
            # find setContentView(R.layout...) and inject after
            pass

    # simpler: just add a function call and definition
    if "fun setupBottomNav()" not in content:
        # Insert call after setContentView
        import re
        content = re.sub(r'(setContentView\(R\.layout\.[^)]+\))', r'\1\n        setupBottomNav()', content)
        
        # Insert function at the end of class
        func = f"""
    private fun setupBottomNav() {{ {bottom_nav} }}
"""
        content = content[:content.rfind('}')] + func + "\n}"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Done")
