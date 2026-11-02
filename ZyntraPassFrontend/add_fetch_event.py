import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """    suspend fun fetchEventById(eventId: String): org.json.JSONObject? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/events?id=eq.$eventId&select=*")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            
            if (conn.responseCode in 200..299) {
                val arr = org.json.JSONArray(conn.inputStream.bufferedReader().readText())
                if (arr.length() > 0) return@withContext arr.getJSONObject(0)
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }"""

# Insert before fetchEventsByIds
content = content.replace('    suspend fun fetchEventsByIds', new_func + '\n\n    suspend fun fetchEventsByIds')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added fetchEventById")
