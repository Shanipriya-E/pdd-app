import os

base_path = "c:/Users/Vishnu/zyntraPassForntend/app/src/main"
java_path = f"{base_path}/java/com/simats/zyntrapass"
res_path = f"{base_path}/res/layout"
manifest_path = f"{base_path}/AndroidManifest.xml"

# 1. Update activity_login.xml
login_xml = f"{res_path}/activity_login.xml"
with open(login_xml, 'r') as f:
    content = f.read()
if "etVolunteerCode" not in content:
    replacement = """
        <!-- Secret Key (Hidden by default) -->
        <EditText
            android:id="@+id/etSecretKey"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:hint="Secret Key (2FA)"
            android:textColorHint="#A8B2D1"
            android:textColor="#FFFFFF"
            android:inputType="textPassword"
            android:background="@drawable/bg_outlined_button"
            android:paddingHorizontal="16dp"
            android:layout_marginTop="16dp"
            android:visibility="gone"
            app:layout_constraintTop_toBottomOf="@id/etPassword" />

        <EditText
            android:id="@+id/etVolunteerCode"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:hint="Volunteer 4-Digit Code"
            android:textColorHint="#A8B2D1"
            android:textColor="#FFFFFF"
            android:inputType="numberPassword"
            android:background="@drawable/bg_outlined_button"
            android:paddingHorizontal="16dp"
            android:layout_marginTop="16dp"
            android:visibility="gone"
            app:layout_constraintTop_toBottomOf="@id/etSecretKey" />
"""
    content = content.replace('<!-- Secret Key (Hidden by default) -->\n        <EditText\n            android:id="@+id/etSecretKey"', replacement.split('<EditText')[0] + '<EditText\n            android:id="@+id/etSecretKey"')
    content = content.replace('app:layout_constraintTop_toBottomOf="@id/etSecretKey"', 'app:layout_constraintTop_toBottomOf="@id/etVolunteerCode"')
    with open(login_xml, 'w') as f:
        f.write(content)

# 2. Add VolunteerDashboardActivity.kt
dash_kt = f"{java_path}/VolunteerDashboardActivity.kt"
with open(dash_kt, 'w') as f:
    f.write("""package com.simats.zyntrapass

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class VolunteerDashboardActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_volunteer_dashboard)
    }
}
""")

# 3. Add activity_volunteer_dashboard.xml
dash_xml = f"{res_path}/activity_volunteer_dashboard.xml"
with open(dash_xml, 'w') as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Volunteer Dashboard Coming Soon!"
        android:textSize="20sp" />
</LinearLayout>
""")

# 4. Update LoginActivity.kt
login_kt = f"{java_path}/LoginActivity.kt"
with open(login_kt, 'r') as f:
    content = f.read()

if "etVolunteerCode" not in content:
    # Basic injection to handle hiding fields
    content = content.replace("private var selectedRole = \"\"", "private var selectedRole = \"\"\n    private lateinit var etVolunteerCode: EditText")
    content = content.replace("val etSecretKey = findViewById<EditText>(R.id.etSecretKey)", "val etSecretKey = findViewById<EditText>(R.id.etSecretKey)\n        etVolunteerCode = findViewById(R.id.etVolunteerCode)")
    
    # Hide/show logic
    content = content.replace("etSecretKey.visibility = View.VISIBLE", "etSecretKey.visibility = View.VISIBLE\n                etVolunteerCode.visibility = View.GONE")
    content = content.replace("etSecretKey.visibility = View.GONE", "etSecretKey.visibility = View.GONE\n                etVolunteerCode.visibility = if (selectedRole == \"volunteer\") View.VISIBLE else View.GONE")
    
    with open(login_kt, 'w') as f:
        f.write(content)

print("Scaffolding complete.")
