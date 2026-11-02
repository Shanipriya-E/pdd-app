import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/RoleSelectionActivity.kt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Toast.makeText(this, "Signup for $role coming soon! Try Organizer.", Toast.LENGTH_SHORT).show()', 'Snackbar.make(findViewById(R.id.mainRole), "Signup for $role coming soon! Try Organizer.", Snackbar.LENGTH_SHORT).show()')

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/RoleSelectionActivity.kt', 'w', encoding='utf-8') as f:
    f.write(text)
