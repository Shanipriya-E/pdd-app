import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDashboardActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_loadStats = """    private fun loadStats() {
        val currentUserId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            val regs = SupabaseApi.fetchAttendeeRegistrations(currentUserId)
            val logs = SupabaseApi.fetchAttendeeLogs(currentUserId)
            
            if (regs != null) {
                val totalRegistered = regs.length()
                var upcoming = 0
                val attendedEventIds = mutableSetOf<String>()
                
                // Add from logs
                if (logs != null) {
                    for (i in 0 until logs.length()) {
                        attendedEventIds.add(logs.getJSONObject(i).optString("event_id"))
                    }
                }
                
                // Add from status and calculate upcoming
                for (i in 0 until totalRegistered) {
                    val status = regs.getJSONObject(i).optString("status")
                    val eventId = regs.getJSONObject(i).optString("event_id")
                    
                    if (status == "attended" || status == "verified") {
                        attendedEventIds.add(eventId)
                    }
                }
                
                // Now calculate upcoming (excluding those already attended via GPS/status)
                for (i in 0 until totalRegistered) {
                    val status = regs.getJSONObject(i).optString("status")
                    val eventId = regs.getJSONObject(i).optString("event_id")
                    
                    if ((status == "approved" || status == "registered") && !attendedEventIds.contains(eventId)) {
                        upcoming++
                    }
                }

                findViewById<TextView>(R.id.tvUpcomingCount).text = upcoming.toString()
                findViewById<TextView>(R.id.tvRegisteredCount).text = totalRegistered.toString()
                findViewById<TextView>(R.id.tvAttendedCount).text = attendedEventIds.size.toString()
            }
        }
    }"""

new_loadStats = """    private fun loadStats() {
        val currentUserId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            val regs = SupabaseApi.fetchAttendeeRegistrations(currentUserId)
            val vols = SupabaseApi.fetchMyVolunteerRequests(currentUserId)
            val logs = SupabaseApi.fetchAttendeeLogs(currentUserId)
            
            var totalRegistered = 0
            var upcoming = 0
            val attendedEventIds = mutableSetOf<String>()
            
            // Collect all unique event IDs we are registered for
            val registeredEventsMap = mutableMapOf<String, String>()
            
            if (regs != null) {
                for (i in 0 until regs.length()) {
                    val obj = regs.getJSONObject(i)
                    registeredEventsMap[obj.optString("event_id")] = obj.optString("status")
                }
            }
            if (vols != null) {
                for (i in 0 until vols.length()) {
                    val obj = vols.getJSONObject(i)
                    // If approved volunteer, treat as registered
                    if (obj.optString("status") == "approved") {
                        registeredEventsMap[obj.optString("event_id")] = "approved"
                    }
                }
            }
            
            totalRegistered = registeredEventsMap.size

            // Add from logs
            if (logs != null) {
                for (i in 0 until logs.length()) {
                    attendedEventIds.add(logs.getJSONObject(i).optString("event_id"))
                }
            }
            
            // Add from status
            for ((eventId, status) in registeredEventsMap) {
                if (status == "attended" || status == "verified") {
                    attendedEventIds.add(eventId)
                }
            }
            
            // Now calculate upcoming (excluding those already attended via GPS/status)
            for ((eventId, status) in registeredEventsMap) {
                if ((status == "approved" || status == "registered") && !attendedEventIds.contains(eventId)) {
                    upcoming++
                }
            }

            findViewById<TextView>(R.id.tvUpcomingCount).text = upcoming.toString()
            findViewById<TextView>(R.id.tvRegisteredCount).text = totalRegistered.toString()
            findViewById<TextView>(R.id.tvAttendedCount).text = attendedEventIds.size.toString()
        }
    }"""

content = content.replace(old_loadStats, new_loadStats)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated loadStats in AttendeeDashboardActivity")
