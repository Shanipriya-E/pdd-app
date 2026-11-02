import os

filepath = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\res\layout\activity_login.xml"
with open(filepath, 'r', encoding='utf-8') as f:
    xml = f.read()

xml = xml.replace('app:layout_constraintTop_toBottomOf="@id/rgRoles"', 'app:layout_constraintTop_toBottomOf="@id/btnRoleVolunteer"')

# Make etVolunteerCode look like the other EditTexts
correct_et_volunteer = '''<EditText
            android:id="@+id/etVolunteerCode"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:hint="Volunteer Code"
            android:textColorHint="#A8B2D1"
            android:textColor="#FFFFFF"
            android:inputType="number"
            android:background="@drawable/bg_outlined_button"
            android:paddingHorizontal="16dp"
            android:layout_marginTop="32dp"
            android:visibility="gone"
            app:layout_constraintTop_toBottomOf="@id/btnRoleVolunteer"
            app:layout_constraintStart_toStartOf="parent" />'''

# find the etVolunteerCode block and replace it
import re
xml = re.sub(r'<EditText\s+android:id="@+id/etVolunteerCode".*?/>', correct_et_volunteer, xml, flags=re.DOTALL)

# Adjust etEmail so it goes BELOW etVolunteerCode if needed, but since they toggle visibility, it might be fine, but constraint layout needs chaining or we can just group them!
# Since we don't want to break too much, let's just make both top-constrained to btnRoleVolunteer. They will overlap, but since one is GONE when the other is VISIBLE, it works perfectly!
# Let's check etEmail constraint: app:layout_constraintTop_toBottomOf="@id/btnRoleVolunteer" - YES!
# So if both etEmail and etVolunteerCode are constrained to btnRoleVolunteer, they will take the same space, but one will be GONE!

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(xml)

print("Fixed activity_login.xml constraints")
