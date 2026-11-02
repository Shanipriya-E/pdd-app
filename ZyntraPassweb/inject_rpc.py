import os

filepath = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\java\com\simats\zyntrapass\SupabaseApi.kt"
with open(filepath, 'r', encoding='utf-8') as f:
    kt = f.read()

inject = """
    suspend fun postRpc(rpcName: String, payload: JSONObject): String? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/rpc/$rpcName")
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
                if (connection.contentLength > 0 || connection.responseCode == 200) {
                    val stream = try { connection.inputStream } catch(e: Exception) { null }
                    stream?.bufferedReader()?.use { it.readText() } ?: "{}"
                } else "{}"
            } else null
        } catch (e: Exception) { null }
    }
"""

if 'suspend fun postRpc' not in kt:
    kt = kt.replace('object SupabaseApi {', 'object SupabaseApi {' + inject)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(kt)
    print("Injected postRpc into SupabaseApi")
else:
    print("postRpc already exists")
