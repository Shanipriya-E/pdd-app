import os

files = ['certificates.html', 'attendee_certificates.html']
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Just in case PowerShell corrupted the cross icon
    content = content.replace('>?<', '>&#215;<')
    content = content.replace('>??<', '>&#215;<')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
