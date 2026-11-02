with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_organizer_signup.xml', 'r', encoding='utf-8') as f:
    content = f.read()

bad_string = "0dp\"
            app:layout_constraintStart_toStartOf=\"parent\"
            app:layout_constraintEnd_toEndOf=\"parent\""
good_string = "0dp\"\n            app:layout_constraintStart_toStartOf=\"parent\"\n            app:layout_constraintEnd_toEndOf=\"parent\""
content = content.replace(bad_string, good_string)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_organizer_signup.xml', 'w', encoding='utf-8') as f:
    f.write(content)
