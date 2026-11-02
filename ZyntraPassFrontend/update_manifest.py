import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/AndroidManifest.xml'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

activities = """
        <activity android:name=".EventDetailActivity" android:exported="false" />
"""

if "EventDetailActivity" not in content:
    content = content.replace('</application>', activities + '    </application>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added EventDetailActivity to manifest")
else:
    print("Already added to manifest")
