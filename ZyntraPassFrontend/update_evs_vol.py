import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeEventsActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add volunteersMap
content = content.replace('private val registrationsMap = mutableMapOf<String, String>()', 'private val registrationsMap = mutableMapOf<String, String>()\n    private val volunteersMap = mutableMapOf<String, JSONObject>()')

# 2. Update loadEvents
load_ev_old = """            val regs = SupabaseApi.fetchAttendeeRegistrations(currentUserId)
            if (regs != null) {
                for (i in 0 until regs.length()) {
                    val r = regs.getJSONObject(i)
                    registrationsMap[r.optString("event_id")] = r.optString("status")
                }
            }
            
            renderEvents(eventsArray)"""

load_ev_new = """            val regs = SupabaseApi.fetchAttendeeRegistrations(currentUserId)
            if (regs != null) {
                for (i in 0 until regs.length()) {
                    val r = regs.getJSONObject(i)
                    registrationsMap[r.optString("event_id")] = r.optString("status")
                }
            }

            val vols = SupabaseApi.fetchVolunteerRequests(currentUserId)
            if (vols != null) {
                for (i in 0 until vols.length()) {
                    val v = vols.getJSONObject(i)
                    volunteersMap[v.optString("event_id")] = v
                }
            }
            
            renderEvents(eventsArray)"""
content = content.replace(load_ev_old, load_ev_new)

# 3. Update renderEvents for btnVolunteer
# Wait, AttendeeEventsActivity has this specific line:
# val isRegistered = registrationsMap.containsKey(eventId)
# if (!isRegistered) continue // ONLY SHOW MY EVENTS
#
# But now they can be registered AS A VOLUNTEER!
# So we need to show the event if they are registered OR if they are a volunteer.

content = content.replace('val isRegistered = registrationsMap.containsKey(eventId)\n            if (!isRegistered) continue // ONLY SHOW MY EVENTS', 'val isRegistered = registrationsMap.containsKey(eventId)\n            val volRecord = volunteersMap[eventId]\n            if (!isRegistered && volRecord == null) continue // ONLY SHOW MY EVENTS')

old_render = """            val btnRegister = view.findViewById<Button>(R.id.btnRegister)
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

new_render = """            val btnRegister = view.findViewById<Button>(R.id.btnRegister)
            val btnVolunteer = view.findViewById<Button>(R.id.btnVolunteer)
            
            if (isRegistered) {
                btnRegister.isEnabled = false
                btnRegister.text = "Registered"
                btnRegister.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnRegister.setTextColor(Color.parseColor("#64748B"))
                btnVolunteer.visibility = android.view.View.GONE
            } else {
                // If they are not an attendee, but they are here, they MUST be a volunteer
                btnRegister.visibility = android.view.View.GONE
                
                if (volRecord != null) {
                    val status = volRecord.optString("status")
                    val code = volRecord.optString("secret_code")
                    btnVolunteer.isEnabled = false
                    btnVolunteer.setBackgroundColor(Color.parseColor("#E2E8F0"))
                    btnVolunteer.setTextColor(Color.parseColor("#64748B"))
                    
                    if (status == "approved") {
                        btnVolunteer.text = "Volunteer Code: $code"
                        btnVolunteer.setTextColor(Color.parseColor("#10B981"))
                    } else {
                        btnVolunteer.text = "Volunteer Pending"
                    }
                }
            }"""
content = content.replace(old_render, new_render)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated AttendeeEventsActivity")
