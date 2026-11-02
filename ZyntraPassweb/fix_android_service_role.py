import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'r', encoding='utf-8') as f:
    content = f.read()

SERVICE_ROLE = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU'

replacement = f"""    suspend fun updateRegistrationStatus(registrationId: String, newStatus: String): Boolean = withContext(Dispatchers.IO) {{
        try {{
            val url = URL("$URL_BASE/rest/v1/event_registrations?id=eq.$registrationId")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "PATCH"
            
            // Bypass RLS using service_role key
            val SERVICE_ROLE = "{SERVICE_ROLE}"
            conn.setRequestProperty("apikey", SERVICE_ROLE)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.setRequestProperty("Prefer", "return=representation")
            
            conn.doOutput = true
            val json = JSONObject().apply {{
                put("status", newStatus)
            }}
            
            java.io.OutputStreamWriter(conn.outputStream).use {{ it.write(json.toString()) }}
            
            if (conn.responseCode in 200..299) {{
                val responseString = conn.inputStream.bufferedReader().use {{ it.readText() }}
                val jsonArray = org.json.JSONArray(responseString)
                if (jsonArray.length() > 0) return@withContext true
            }}
        }} catch (e: Exception) {{ e.printStackTrace() }}
        return@withContext false
    }}"""

content = re.sub(r'\s*suspend fun updateRegistrationStatus.*?return@withContext false\s*\}', '\n\n' + replacement, content, flags=re.DOTALL)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done android!")
