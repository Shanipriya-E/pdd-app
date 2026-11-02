import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/RoleSelectionActivity.kt', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'\s*findViewById<Button>\(R\.id\.btnVolunteer\)\.setOnClickListener\s*\{\s*handleRoleSelection\("Volunteer"\)\s*\}'
text = re.sub(pattern, '', text)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/RoleSelectionActivity.kt', 'w', encoding='utf-8') as f:
    f.write(text)
