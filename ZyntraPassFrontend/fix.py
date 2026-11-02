with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_organizer_signup.xml', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'0dp\"\
\s+app:layout_constraintStart_toStartOf=\"parent\"\
\s+app:layout_constraintEnd_toEndOf=\"parent\"', '0dp\"\n            app:layout_constraintStart_toStartOf=\"parent\"\n            app:layout_constraintEnd_toEndOf=\"parent\"', content)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_organizer_signup.xml', 'w', encoding='utf-8') as f:
    f.write(content)
