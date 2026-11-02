import os

files = ['certificates.html', 'attendee_certificates.html']
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace('SUPABASE_ANON)', 'SUPABASE_ANON_KEY)')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
