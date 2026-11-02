import os

filepath = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\java\com\simats\zyntrapass\SupabaseApi.kt"
with open(filepath, 'r', encoding='utf-8') as f:
    kt = f.read()

inject = """
    // Generic HTTP Methods
    suspend fun get(endpoint: String): String? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/$endpoint")
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "GET"
            connection.setRequestProperty("apikey", ANON_KEY)
            currentUserToken?.let { connection.setRequestProperty("Authorization", "Bearer $it") }
            if (connection.responseCode in 200..299) {
                connection.inputStream.bufferedReader().use { it.readText() }
            } else null
        } catch (e: Exception) { null }
    }

    suspend fun patch(endpoint: String, payload: JSONObject): String? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/$endpoint")
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "PATCH"
            connection.doOutput = true
            connection.setRequestProperty("Content-Type", "application/json")
            connection.setRequestProperty("apikey", ANON_KEY)
            currentUserToken?.let { connection.setRequestProperty("Authorization", "Bearer $it") }
            val writer = OutputStreamWriter(connection.outputStream)
            writer.write(payload.toString())
            writer.flush()
            if (connection.responseCode in 200..299) {
                if (connection.contentLength > 0) connection.inputStream.bufferedReader().use { it.readText() } else "{}"
            } else null
        } catch (e: Exception) { null }
    }

    suspend fun postArray(endpoint: String, payload: org.json.JSONArray): String? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/$endpoint")
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "POST"
            connection.doOutput = true
            connection.setRequestProperty("Content-Type", "application/json")
            connection.setRequestProperty("apikey", ANON_KEY)
            currentUserToken?.let { connection.setRequestProperty("Authorization", "Bearer $it") }
            val writer = OutputStreamWriter(connection.outputStream)
            writer.write(payload.toString())
            writer.flush()
            if (connection.responseCode in 200..299) {
                if (connection.contentLength > 0) connection.inputStream.bufferedReader().use { it.readText() } else "{}"
            } else null
        } catch (e: Exception) { null }
    }
"""

if 'suspend fun get(endpoint' not in kt:
    kt = kt.replace('object SupabaseApi {', 'object SupabaseApi {' + inject)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(kt)
    print("Injected generic HTTP methods into SupabaseApi")
else:
    print("Methods already exist")
