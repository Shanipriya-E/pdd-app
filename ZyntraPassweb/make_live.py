with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/participants.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace title
content = content.replace('<title>ZyntraPass - Participants</title>', '<title>ZyntraPass - Live Attendance</title>')
content = content.replace('<h1 class="title">Participants</h1>', '<h1 class="title">Live Attendance</h1>')
content = content.replace('<p class="subtitle">Review and manage join requests.</p>', '<p class="subtitle">Monitor real-time GPS check-ins for your ongoing events.</p>')

# Save as live.html
with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created live.html template")
