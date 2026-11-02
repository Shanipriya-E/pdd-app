import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_role_selection.xml', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'\s*<Button\s+android:id="@\+id/btnVolunteer".*?/>'
text = re.sub(pattern, '', text, flags=re.DOTALL)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_role_selection.xml', 'w', encoding='utf-8') as f:
    f.write(text)
