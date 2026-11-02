import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\s*<button class="role-btn" data-role="volunteer">I am a Volunteer</button>', '', text)

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
