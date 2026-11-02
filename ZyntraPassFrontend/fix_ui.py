import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/item_discover_card.xml'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_xml = """            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal">
                <Button android:id="@+id/btnView" android:layout_width="0dp" android:layout_weight="1" android:layout_height="48dp" android:text="View Event" android:textAllCaps="false" android:backgroundTint="#FFFFFF" android:textColor="#0F172A" app:strokeColor="#E2E8F0" app:strokeWidth="1dp" android:layout_marginEnd="6dp" />
                <Button android:id="@+id/btnRegister" android:layout_width="0dp" android:layout_weight="1" android:layout_height="48dp" android:text="Register" android:textAllCaps="false" android:backgroundTint="#5B54E3" android:textColor="#FFFFFF" android:layout_marginStart="6dp" />
            </LinearLayout>"""

new_xml = """            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:layout_marginBottom="8dp">
                <Button android:id="@+id/btnView" android:layout_width="0dp" android:layout_weight="1" android:layout_height="48dp" android:text="View Event" android:textAllCaps="false" android:backgroundTint="#FFFFFF" android:textColor="#0F172A" app:strokeColor="#E2E8F0" app:strokeWidth="1dp" android:layout_marginEnd="6dp" />
                <Button android:id="@+id/btnRegister" android:layout_width="0dp" android:layout_weight="1" android:layout_height="48dp" android:text="Register" android:textAllCaps="false" android:backgroundTint="#5B54E3" android:textColor="#FFFFFF" android:layout_marginStart="6dp" />
            </LinearLayout>
            <Button android:id="@+id/btnVolunteer" android:layout_width="match_parent" android:layout_height="48dp" android:text="Volunteer for Event" android:textAllCaps="false" android:backgroundTint="#FFFFFF" android:textColor="#5B54E3" app:strokeColor="#5B54E3" app:strokeWidth="1dp" />"""

content = content.replace(old_xml, new_xml)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated XML")
