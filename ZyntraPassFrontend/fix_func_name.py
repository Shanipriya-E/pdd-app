import os
import re

# 1. Rename in SupabaseApi.kt
filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('suspend fun fetchVolunteerRequests(userId: String)', 'suspend fun fetchMyVolunteerRequests(userId: String)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update calls
files = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeEventsActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/EventDetailActivity.kt'
]

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('SupabaseApi.fetchVolunteerRequests(currentUserId)', 'SupabaseApi.fetchMyVolunteerRequests(currentUserId)')
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
    
print("Renamed fetchVolunteerRequests to fetchMyVolunteerRequests")
