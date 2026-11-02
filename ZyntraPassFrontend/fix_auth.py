import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'conn.setRequestProperty("apikey", ANON_KEY)' in line:
        # Check next 2 lines if Authorization is already set
        has_auth = False
        for j in range(1, 3):
            if i + j < len(lines) and 'conn.setRequestProperty("Authorization"' in lines[i+j]:
                has_auth = True
        
        if not has_auth:
            # Add SERVICE_ROLE_KEY
            indent = line[:line.find('conn.')]
            new_lines.append(indent + 'conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")\n')

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Added missing Authorization headers to SupabaseApi")
