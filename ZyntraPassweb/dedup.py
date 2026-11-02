with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_attendance.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Keep only up to the first </html>
first_end = content.find('</html>') + len('</html>')
content = content[:first_end]

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_attendance.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned up duplicate content. Lines:", content.count('\n'))
