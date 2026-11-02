import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_func = """    suspend fun registerAsVolunteer(eventId: String, organizerId: String, userId: String): Boolean = 
withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/volunteer_requests")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.doOutput = true
            
            val json = JSONObject().apply {
                put("event_id", eventId)
                put("organizer_id", organizerId)
                put("volunteer_id", userId)
                put("status", "pending")
            }
            java.io.OutputStreamWriter(conn.outputStream).use { it.write(json.toString()) }
            
            if (conn.responseCode in 200..299) return@withContext true
            
            val errorMsg = conn.errorStream?.bufferedReader()?.use { it.readText() }
            println("Volunteer registration failed: $errorMsg")
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext false
    }"""

new_func = """    suspend fun registerAsVolunteer(eventId: String, organizerId: String, userId: String): Boolean = 
withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/volunteers")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.doOutput = true
            
            val json = JSONObject().apply {
                put("event_id", eventId)
                put("user_id", userId)
                put("status", "pending")
            }
            java.io.OutputStreamWriter(conn.outputStream).use { it.write(json.toString()) }
            
            if (conn.responseCode in 200..299) return@withContext true
            
            val errorMsg = conn.errorStream?.bufferedReader()?.use { it.readText() }
            println("Volunteer registration failed: $errorMsg")
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext false
    }"""

# Use string replace
content = content.replace(old_func, new_func)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated registerAsVolunteer in SupabaseApi")
