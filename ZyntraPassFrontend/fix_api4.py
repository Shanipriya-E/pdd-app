with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('conn.setRequestProperty("Authorization", "Bearer \")', 'conn.setRequestProperty("Authorization", "Bearer \")')

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'w', encoding='utf-8') as f:
    f.write(text)
