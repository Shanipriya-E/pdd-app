import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace for signUpOrganizer
text = re.sub(
    r'(val newUserId = userObj\.getString\("id"\)\s+profileData\.put\("id", newUserId\)\s+profileData\.put\("role", "organizer"\)\s+val profUrl = URL\("\$URL_BASE/rest/v1/profiles"\)\s+val profConn = profUrl\.openConnection\(\) as HttpURLConnection\s+profConn\.requestMethod = "POST"\s+profConn\.setRequestProperty\("apikey", ANON_KEY\)\s+profConn\.setRequestProperty\("Authorization", "Bearer )\$ANON_KEY("\))',
    r'val sessionObj = responseObj.optJSONObject("session")\n                val token = sessionObj?.optString("access_token") ?: ANON_KEY\n                \1$token\2',
    text
)

# Replace for signUpAttendee
text = re.sub(
    r'(val newUserId = userObj\.getString\("id"\)\s+// 2\. Insert Profile\s+profileData\.put\("id", newUserId\)\s+profileData\.put\("role", "attendee"\) // fallback standard role\s+// Try attendee_profiles first\s+val profUrl = URL\("\$URL_BASE/rest/v1/attendee_profiles"\)\s+val profConn = profUrl\.openConnection\(\) as HttpURLConnection\s+profConn\.requestMethod = "POST"\s+profConn\.setRequestProperty\("apikey", ANON_KEY\)\s+profConn\.setRequestProperty\("Authorization", "Bearer )\$ANON_KEY("\))',
    r'val sessionObj = responseObj.optJSONObject("session")\n                val token = sessionObj?.optString("access_token") ?: ANON_KEY\n                \1$token\2',
    text
)

text = re.sub(
    r'(fallbackConn\.setRequestProperty\("Authorization", "Bearer )\$ANON_KEY("\))',
    r'\1$token\2',
    text
)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'w', encoding='utf-8') as f:
    f.write(text)
