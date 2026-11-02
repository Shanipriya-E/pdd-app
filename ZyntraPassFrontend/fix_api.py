import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'r', encoding='utf-8') as f:
    text = f.read()

# For signUpOrganizer
pattern_org = r'(val newUserId = userObj\.getString\("id"\)\s*\n\s*profileData\.put\("id", newUserId\)\s*\n\s*profileData\.put\("role", "organizer"\)\s*\n\s*val profUrl = URL\("\/rest/v1/profiles"\)\s*\n\s*val profConn = profUrl\.openConnection\(\) as HttpURLConnection\s*\n\s*profConn\.requestMethod = "POST"\s*\n\s*profConn\.setRequestProperty\("apikey", ANON_KEY\)\s*\n\s*profConn\.setRequestProperty\("Authorization", "Bearer )\("\))'

replacement_org = r'''val sessionObj = responseObj.optJSONObject("session")
                val token = sessionObj?.optString("access_token") ?: ANON_KEY
                val newUserId = userObj.getString("id")
                
                profileData.put("id", newUserId)
                profileData.put("role", "organizer")
                
                val profUrl = URL("/rest/v1/profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer ")'''

text = re.sub(pattern_org, replacement_org, text)

# For signUpAttendee
pattern_att = r'(val newUserId = userObj\.getString\("id"\)\s*\n\s*// 2\. Insert Profile\s*\n\s*profileData\.put\("id", newUserId\)\s*\n\s*profileData\.put\("role", "attendee"\) // fallback standard role\s*\n\s*// Try attendee_profiles first\s*\n\s*val profUrl = URL\("\/rest/v1/attendee_profiles"\)\s*\n\s*val profConn = profUrl\.openConnection\(\) as HttpURLConnection\s*\n\s*profConn\.requestMethod = "POST"\s*\n\s*profConn\.setRequestProperty\("apikey", ANON_KEY\)\s*\n\s*profConn\.setRequestProperty\("Authorization", "Bearer )\("\))'

replacement_att = r'''val sessionObj = responseObj.optJSONObject("session")
                val token = sessionObj?.optString("access_token") ?: ANON_KEY
                val newUserId = userObj.getString("id")
                
                // 2. Insert Profile
                profileData.put("id", newUserId)
                profileData.put("role", "attendee") // fallback standard role
                
                // Try attendee_profiles first
                val profUrl = URL("/rest/v1/attendee_profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer ")'''

text = re.sub(pattern_att, replacement_att, text)

# Also fallbackConn
pattern_fall = r'(fallbackConn\.setRequestProperty\("Authorization", "Bearer )\("\))'
replacement_fall = r'\1\2'
text = re.sub(pattern_fall, replacement_fall, text)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'w', encoding='utf-8') as f:
    f.write(text)
