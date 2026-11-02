import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/CreateEventActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace date format for Start Date
content = content.replace('String.format("%02d-%02d-%d", d, m + 1, y)', 'String.format("%d-%02d-%02d", y, m + 1, d)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated date format to yyyy-MM-dd")
