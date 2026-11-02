import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """            val btnRegister = view.findViewById<Button>(R.id.btnRegister)
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
            }"""

new_logic = """            val btnRegister = view.findViewById<Button>(R.id.btnRegister)
            val btnVolunteer = view.findViewById<Button>(R.id.btnVolunteer)
            
            if (isRegistered) {
                btnRegister.isEnabled = false
                btnRegister.text = "Registered"
                btnRegister.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnRegister.setTextColor(Color.parseColor("#64748B"))
                btnVolunteer.visibility = android.view.View.GONE
            } else {
                btnRegister.setOnClickListener {
                    handleRegister(eventId, btnRegister, orgId, false)
                }
                btnVolunteer.setOnClickListener {
                    handleRegister(eventId, btnVolunteer, orgId, true)
                }
            }"""

content = content.replace(old_logic, new_logic)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated DiscoverActivity")
