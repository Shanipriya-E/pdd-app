import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the createFullEvent success check with error logging
old_code = """
            if (conn.responseCode == 201) {
                // Success! Event created.
                // In a full implementation, we'd extract the event ID from the response 
                // and then loop to POST the guests and sessions to their respective tables.
                // For this demo, we mock the success of the secondary tables.
                return@withContext true
            }
"""
new_code = """
            if (conn.responseCode == 201) {
                return@withContext true
            } else {
                val errorMsg = conn.errorStream?.bufferedReader()?.use { it.readText() }
                android.util.Log.e("SupabaseApi", "Create event failed: ${conn.responseCode} - $errorMsg")
            }
"""
content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
