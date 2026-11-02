import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('conn.setRequestProperty("Authorization", "Bearer ${currentUserToken ?: ANON_KEY}")', 'conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
