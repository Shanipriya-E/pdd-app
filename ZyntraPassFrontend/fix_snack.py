import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/OrganizerSignupActivity.kt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('import android.widget.Toast', 'import android.widget.Toast\nimport com.google.android.material.snackbar.Snackbar')
text = text.replace('Toast.makeText(this, "Please fill in all required fields", Toast.LENGTH_SHORT).show()', 'Snackbar.make(btnSubmitSignup, "Please fill in all required fields", Snackbar.LENGTH_SHORT).show()')
text = text.replace('Toast.makeText(this, "Passwords do not match", Toast.LENGTH_SHORT).show()', 'Snackbar.make(btnSubmitSignup, "Passwords do not match", Snackbar.LENGTH_SHORT).show()')
text = text.replace('Toast.makeText(this@OrganizerSignupActivity, "Registration failed", Toast.LENGTH_SHORT).show()', 'Snackbar.make(btnSubmitSignup, "Registration failed", Snackbar.LENGTH_SHORT).show()')
text = text.replace('Toast.makeText(this@OrganizerSignupActivity, "Account created! Please log in.", Toast.LENGTH_LONG).show()', 'Snackbar.make(btnSubmitSignup, "Account created! Please log in.", Snackbar.LENGTH_LONG).show()')

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/OrganizerSignupActivity.kt', 'w', encoding='utf-8') as f:
    f.write(text)
