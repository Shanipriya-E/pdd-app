import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """    suspend fun fetchVolunteerRequests(userId: String): org.json.JSONArray? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/volunteers?user_id=eq.$userId&select=event_id,status,secret_code")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            
            if (conn.responseCode in 200..299) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }"""

content = content.replace('suspend fun fetchAttendeeRegistrations', new_func + '\n\n    suspend fun fetchAttendeeRegistrations')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added fetchVolunteerRequests")
