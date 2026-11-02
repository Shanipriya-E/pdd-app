import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeAttendanceActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"dY"? " +', '"" +')
content = content.replace('"dY". " +', '"" +')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed garbage strings")
