import codecs
html=codecs.open('certificates.html', 'r', 'utf-8').read()
if '<h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 8px;">Certificates</h1>' in html:
    print('SUCCESS: Certificates UI is present in certificates.html')
else:
    print('FAILED: Certificates UI missing')

if 'async function main() {' in html:
    matches = html.count('async function main() {')
    print(f'Matches for main(): {matches}')
