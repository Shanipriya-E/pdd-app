import re, codecs
html=codecs.open('dashboard.html', 'r', 'utf-8').read()
m = re.search(r'<!-- Top App Bar -->.*?<div class="container">', html, re.DOTALL)
if m:
    print(m.group(0))
