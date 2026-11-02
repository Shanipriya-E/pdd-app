import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeAttendanceActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('class AttendeeDiscoverActivity', 'class AttendeeAttendanceActivity')
content = content.replace('R.layout.activity_attendee_discover', 'R.layout.activity_attendee_attendance')
content = content.replace('this@AttendeeDiscoverActivity', 'this@AttendeeAttendanceActivity')

# Rewrite loadEvents and renderEvents entirely for Attendance
new_logic = """
    private fun loadEvents() {
        val currentUserId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            val eventsArray = SupabaseApi.fetchAllEvents() ?: org.json.JSONArray()
            val logsArray = SupabaseApi.fetchAttendeeLogs(currentUserId) ?: org.json.JSONArray()
            
            // Build map of events
            val eventsMap = mutableMapOf<String, JSONObject>()
            val orgIds = mutableListOf<String>()
            for (i in 0 until eventsArray.length()) {
                val ev = eventsArray.getJSONObject(i)
                eventsMap[ev.optString("id")] = ev
                val orgId = ev.optString("organizer_id")
                if (orgId.isNotEmpty() && !orgIds.contains(orgId)) orgIds.add(orgId)
            }
            
            // Fetch organizers
            if (orgIds.isNotEmpty()) {
                val orgProfiles = SupabaseApi.fetchProfilesByIds(orgIds)
                if (orgProfiles != null) {
                    for (i in 0 until orgProfiles.length()) {
                        val p = orgProfiles.getJSONObject(i)
                        profilesMap[p.optString("id")] = p
                    }
                }
            }
            
            renderLogs(logsArray, eventsMap)
        }
    }

    private fun renderLogs(logs: JSONArray, eventsMap: Map<String, JSONObject>) {
        val container = findViewById<LinearLayout>(R.id.eventsContainer)
        container.removeAllViews()
        
        if (logs.length() == 0) {
            val tv = TextView(this).apply {
                text = "No attendance history found."
                setPadding(40, 40, 40, 40)
                textSize = 16f
            }
            container.addView(tv)
            return
        }

        val inflater = LayoutInflater.from(this)
        for (i in 0 until logs.length()) {
            val log = logs.getJSONObject(i)
            val eventId = log.optString("event_id")
            val ev = eventsMap[eventId] ?: continue
            val orgId = ev.optString("organizer_id")
            
            val org = profilesMap[orgId]
            val orgName = org?.optString("institution")?.takeIf { it.isNotBlank() } 
                          ?: org?.optString("full_name")?.takeIf { it.isNotBlank() } 
                          ?: "Unknown Organizer"
            
            val cat = ev.optString("category", "General").takeIf { it.isNotBlank() } ?: "General"
            
            val view = inflater.inflate(R.layout.item_discover_card, container, false)
            
            view.findViewById<TextView>(R.id.tvCardType).text = "Checked In"
            view.findViewById<TextView>(R.id.tvCardMatch).text = "Verified"
            view.findViewById<TextView>(R.id.tvCardLocationTop).text = "dY"? " + ev.optString("venue_name", "Online")
            view.findViewById<TextView>(R.id.tvEventTitle).text = ev.optString("title", "Untitled")
            view.findViewById<TextView>(R.id.tvEventOrg).text = orgName
            
            val checkInTime = log.optString("scanned_at", "Unknown").replace("T", " ").take(16)
            view.findViewById<TextView>(R.id.tvDate).text = "dY". " + checkInTime
            view.findViewById<TextView>(R.id.tvTime).text = ""
            view.findViewById<TextView>(R.id.tvDistance).text = "dY"? " + ev.optString("address", "Various")
            view.findViewById<TextView>(R.id.tvTag1).text = cat

            val btnRegister = view.findViewById<Button>(R.id.btnRegister)
            btnRegister.isEnabled = false
            btnRegister.text = "Attended"
            btnRegister.setBackgroundColor(android.graphics.Color.parseColor("#10B981"))
            btnRegister.setTextColor(android.graphics.Color.parseColor("#FFFFFF"))
            
            val btnView = view.findViewById<Button>(R.id.btnView)
            btnView.visibility = android.view.View.GONE
            
            container.addView(view)
        }
    }
"""

# Replace loadEvents, renderEvents, and handleRegister
import re
content = re.sub(r'private fun loadEvents\(\) \{[\s\S]*?private fun setupBottomNav\(\)', new_logic + '\n\n    private fun setupBottomNav()', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated AttendeeAttendanceActivity.kt")
