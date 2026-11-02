import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/CreateEventActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the launcher to the class
launcher_code = """
    private var currentUploadButton: android.widget.TextView? = null
    private val pickImageLauncher = registerForActivityResult(androidx.activity.result.contract.ActivityResultContracts.GetContent()) { uri: android.net.Uri? ->
        if (uri != null) {
            currentUploadButton?.text = "Photo Selected"
            currentUploadButton?.setBackgroundResource(R.drawable.bg_primary_button) // A nice background
            currentUploadButton?.setTextColor(android.graphics.Color.parseColor("#FFFFFF"))
        }
    }
"""
if "pickImageLauncher" not in content:
    content = content.replace('class CreateEventActivity : AppCompatActivity() {', 'class CreateEventActivity : AppCompatActivity() {\n' + launcher_code)

# Replace the Toast in addGuestView with the launcher
mock_toast = 'Toast.makeText(this@CreateEventActivity, "Upload Photo Clicked (Mock)", Toast.LENGTH_SHORT).show()'
real_code = """
                currentUploadButton = guestView.findViewById<android.widget.TextView>(R.id.btnUploadPhoto)
                pickImageLauncher.launch("image/*")
"""
content = content.replace(mock_toast, real_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated CreateEventActivity photo mock")
