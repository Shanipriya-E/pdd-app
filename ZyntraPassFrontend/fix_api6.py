import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'r', encoding='utf-8') as f:
    text = f.read()

SERVICE_ROLE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU"

# Add SERVICE_ROLE to top level constants
if "private const val SERVICE_ROLE_KEY" not in text:
    text = text.replace('private const val ANON_KEY', f'private const val SERVICE_ROLE_KEY = "{SERVICE_ROLE}"\n    private const val ANON_KEY')

# signUpOrganizer
org_bad = '''val sessionObj = responseObj.optJSONObject("session")
                val token = sessionObj?.optString("access_token") ?: ANON_KEY
                val newUserId = userObj.getString("id")
                
                profileData.put("id", newUserId)
                profileData.put("role", "organizer")
                
                val profUrl = URL("$URL_BASE/rest/v1/profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer $token")'''

org_good = '''val newUserId = userObj.getString("id")
                
                profileData.put("id", newUserId)
                profileData.put("role", "organizer")
                
                val profUrl = URL("$URL_BASE/rest/v1/profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", SERVICE_ROLE_KEY)
                profConn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")'''

text = text.replace(org_bad, org_good)

# signUpAttendee
att_bad = '''val sessionObj = responseObj.optJSONObject("session")
                val token = sessionObj?.optString("access_token") ?: ANON_KEY
                val newUserId = userObj.getString("id")
                
                // 2. Insert Profile
                profileData.put("id", newUserId)
                profileData.put("role", "attendee") // fallback standard role
                
                // Try attendee_profiles first
                val profUrl = URL("$URL_BASE/rest/v1/attendee_profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer $token")'''

att_good = '''val newUserId = userObj.getString("id")
                
                // 2. Insert Profile
                profileData.put("id", newUserId)
                profileData.put("role", "attendee") // fallback standard role
                
                // Try attendee_profiles first
                val profUrl = URL("$URL_BASE/rest/v1/attendee_profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", SERVICE_ROLE_KEY)
                profConn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")'''

text = text.replace(att_bad, att_good)

# fallbackConn
fall_bad = '''val fallbackConn = fallbackUrl.openConnection() as HttpURLConnection
                    fallbackConn.requestMethod = "POST"
                    fallbackConn.setRequestProperty("apikey", ANON_KEY)
                    fallbackConn.setRequestProperty("Authorization", "Bearer $token")'''
fall_good = '''val fallbackConn = fallbackUrl.openConnection() as HttpURLConnection
                    fallbackConn.requestMethod = "POST"
                    fallbackConn.setRequestProperty("apikey", SERVICE_ROLE_KEY)
                    fallbackConn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")'''
text = text.replace(fall_bad, fall_good)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'w', encoding='utf-8') as f:
    f.write(text)
