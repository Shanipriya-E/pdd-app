import codecs
html=codecs.open('certificates.html', 'r', 'utf-8').read()
start = html.find('<div class="container"')
end = html.find('<!--', start)
print(html[start:end])
