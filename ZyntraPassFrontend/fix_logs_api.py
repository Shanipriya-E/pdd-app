import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('attendance_logs?attendee_id=eq.$userId&select=event_id"', 'attendance_logs?attendee_id=eq.$userId&select=*"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated SupabaseApi logs")
