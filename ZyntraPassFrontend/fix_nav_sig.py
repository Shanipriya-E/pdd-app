import re

activities = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDashboardActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeEventsActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeAttendanceActivity.kt',
]

for filepath in activities:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The script incorrectly put `setupSidebar() {` as the body of setupBottomNav.
    # Fix: restore the `private fun setupBottomNav() {` signature
    content = content.replace(
        'private fun setupBottomNav()\n        setupSidebar() {',
        'private fun setupBottomNav() {'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

print("Done!")
