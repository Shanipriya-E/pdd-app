import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt'
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
            
            val volRecord = volunteersMap[eventId]
            
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
                
                if (volRecord != null) {
                    val status = volRecord.optString("status")
                    val code = volRecord.optString("secret_code")
                    btnVolunteer.isEnabled = false
                    btnVolunteer.setBackgroundColor(Color.parseColor("#E2E8F0"))
                    btnVolunteer.setTextColor(Color.parseColor("#64748B"))
                    
                    if (status == "approved") {
                        btnVolunteer.text = "Volunteer Code: $code"
                        btnVolunteer.setTextColor(Color.parseColor("#10B981")) // Green text for approved code
                    } else {
                        btnVolunteer.text = "Volunteer Pending"
                    }
                } else {
                    btnVolunteer.setOnClickListener {
                        handleRegister(eventId, btnVolunteer, orgId, true)
                    }
                }
            }"""
content = content.replace(old_render, new_render)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated AttendeeDiscoverActivity")
