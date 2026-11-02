import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace handleRegister logic with the dialog
old_logic = """
            if (isRegistered) {
                btnRegister.isEnabled = false
                btnRegister.text = "Registered"
                btnRegister.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnRegister.setTextColor(Color.parseColor("#64748B"))
            } else {
                btnRegister.setOnClickListener {
                    handleRegister(eventId, btnRegister)
                }
            }
"""

new_logic = """
            if (isRegistered) {
                btnRegister.isEnabled = false
                btnRegister.text = "Registered"
                btnRegister.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnRegister.setTextColor(Color.parseColor("#64748B"))
            } else {
                btnRegister.setOnClickListener {
                    val options = arrayOf("As Attendee", "As Volunteer")
                    androidx.appcompat.app.AlertDialog.Builder(this@AttendeeDiscoverActivity)
                        .setTitle("Register for Event")
                        .setItems(options) { _, which ->
                            if (which == 0) {
                                handleRegister(eventId, btnRegister, orgId, false)
                            } else {
                                handleRegister(eventId, btnRegister, orgId, true)
                            }
                        }
                        .setNegativeButton("Cancel", null)
                        .show()
                }
            }
"""
content = content.replace(old_logic, new_logic)

old_handle = "private fun handleRegister(eventId: String, btn: Button) {"
new_handle = """
    private fun handleRegister(eventId: String, btn: Button, orgId: String, isVolunteer: Boolean) {
        val currentUserId = SupabaseApi.currentUserId ?: return
        btn.isEnabled = false
        btn.text = "Registering..."
        
        CoroutineScope(Dispatchers.Main).launch {
            val success = if (isVolunteer) {
                SupabaseApi.registerAsVolunteer(eventId, orgId, currentUserId)
            } else {
                SupabaseApi.registerForEvent(eventId, currentUserId)
            }
            
            if (success) {
                Toast.makeText(this@AttendeeDiscoverActivity, if (isVolunteer) "Volunteer request sent!" else "Registered!", Toast.LENGTH_SHORT).show()
                btn.text = if (isVolunteer) "Pending" else "Registered"
                btn.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btn.setTextColor(Color.parseColor("#64748B"))
                registrationsMap[eventId] = if (isVolunteer) "pending" else "registered"
            } else {
                Toast.makeText(this@AttendeeDiscoverActivity, "Error registering", Toast.LENGTH_SHORT).show()
                btn.isEnabled = true
                btn.text = "Register"
            }
        }
    }
"""

# Replace the entire old handleRegister method
content = re.sub(r'private fun handleRegister\(eventId: String, btn: Button\) \{[\s\S]*?\}\s*\}', new_handle.strip() + '\n', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
