activities = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDashboardActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeEventsActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeAttendanceActivity.kt',
]

for filepath in activities:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if setupSidebar() is called in onCreate already
    if 'setupSidebar()' not in content:
        content = content.replace('setupBottomNav()', 'setupBottomNav()\n        setupSidebar()')
        print(f"Added setupSidebar() call in {filepath}")
    else:
        print(f"setupSidebar() already present in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
