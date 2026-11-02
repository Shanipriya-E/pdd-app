import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a missing closing brace to the very end
if content.endswith("}\n}"):
    content += "\n}"
elif content.endswith("}\n"):
    content += "}\n"
else:
    content += "\n}"

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Appended closing brace.")
