import re, codecs
html=codecs.open('attendee_dashboard.html', 'r', 'utf-8').read()
m = re.search(r'<div class="bottom-nav">.*?</div>', html, re.DOTALL)
if m:
    print(m.group(0).encode('utf-8'))
