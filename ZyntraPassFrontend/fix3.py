import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_organizer_signup.xml', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace match_parent with 0dp and add constraints for all children of ConstraintLayout except the ConstraintLayout itself
# The ConstraintLayout has id @+id/mainSignup and wrap_content height.
# We'll just replace 'android:layout_width="match_parent"' with 'android:layout_width="0dp"\n            app:layout_constraintStart_toStartOf="parent"\n            app:layout_constraintEnd_toEndOf="parent"'
# BUT ONLY inside the ConstraintLayout children. 
# The outer ScrollView has match_parent, ConstraintLayout has match_parent.
# We will do a targeted replace for all TextView, EditText, Button elements.

tags = ['TextView', 'EditText', 'Button']
for tag in tags:
    pattern = r'(<' + tag + r'[^>]*?)android:layout_width="match_parent"([^>]*?>)'
    replacement = r'\1android:layout_width="0dp"\n            app:layout_constraintStart_toStartOf="parent"\n            app:layout_constraintEnd_toEndOf="parent"\2'
    text = re.sub(pattern, replacement, text, flags=re.DOTALL)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_organizer_signup.xml', 'w', encoding='utf-8') as f:
    f.write(text)
