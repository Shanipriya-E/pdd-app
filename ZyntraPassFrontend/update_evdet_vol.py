import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/EventDetailActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update loadEventDetails
# It needs to fetch registration and volunteer status! But wait, isRegistered was passed via intent!
# I can just fetch it again to be safe.
# Actually, wait. EventDetailActivity has isRegistered passed via intent.
# It does not know if they are a volunteer.
# So I should fetch the volunteer status inside EventDetailActivity.

old_logic = """            val btnAction = findViewById<Button>(R.id.btnAction)
            if (isRegistered) {
                btnAction.isEnabled = false
                btnAction.text = "Approved & Registered"
                btnAction.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnAction.setTextColor(Color.parseColor("#64748B"))
            } else {
                btnAction.setOnClickListener {
                    val options = arrayOf("As Attendee", "As Volunteer")
                    androidx.appcompat.app.AlertDialog.Builder(this@EventDetailActivity)
                        .setTitle("Register for Event")
                        .setItems(options) { _, which ->
                            handleRegister(which == 1)
                        }
                        .setNegativeButton("Cancel", null)
                        .show()
                }
            }"""

new_logic = """            val btnAction = findViewById<Button>(R.id.btnAction)
            
            val currentUserId = SupabaseApi.currentUserId
            var volRecord: org.json.JSONObject? = null
            if (currentUserId != null) {
                val vols = SupabaseApi.fetchVolunteerRequests(currentUserId)
                if (vols != null) {
                    for (i in 0 until vols.length()) {
                        val v = vols.getJSONObject(i)
                        if (v.optString("event_id") == eventId) {
                            volRecord = v
                            break
                        }
                    }
                }
            }
            
            if (isRegistered) {
                btnAction.isEnabled = false
                btnAction.text = "Approved & Registered"
                btnAction.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnAction.setTextColor(Color.parseColor("#64748B"))
            } else if (volRecord != null) {
                val status = volRecord.optString("status")
                val code = volRecord.optString("secret_code")
                btnAction.isEnabled = false
                btnAction.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnAction.setTextColor(Color.parseColor("#64748B"))
                
                if (status == "approved") {
                    btnAction.text = "Volunteer Code: $code"
                    btnAction.setTextColor(Color.parseColor("#10B981"))
                } else {
                    btnAction.text = "Volunteer Pending"
                }
            } else {
                btnAction.setOnClickListener {
                    val options = arrayOf("As Attendee", "As Volunteer")
                    androidx.appcompat.app.AlertDialog.Builder(this@EventDetailActivity)
                        .setTitle("Register for Event")
                        .setItems(options) { _, which ->
                            handleRegister(which == 1)
                        }
                        .setNegativeButton("Cancel", null)
                        .show()
                }
            }"""

content = content.replace(old_logic, new_logic)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated EventDetailActivity")
