with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'r', encoding='utf-8') as f:
    text = f.read()

org_bad = '''val newUserId = userObj.getString("id")
                
                profileData.put("id", newUserId)
                profileData.put("role", "organizer")
                
                val profUrl = URL("\/rest/v1/profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer \")'''

org_good = '''val sessionObj = responseObj.optJSONObject("session")
                val token = sessionObj?.optString("access_token") ?: ANON_KEY
                val newUserId = userObj.getString("id")
                
                profileData.put("id", newUserId)
                profileData.put("role", "organizer")
                
                val profUrl = URL("\/rest/v1/profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer \")'''

text = text.replace(org_bad, org_good)

att_bad = '''val newUserId = userObj.getString("id")
                
                // 2. Insert Profile
                profileData.put("id", newUserId)
                profileData.put("role", "attendee") // fallback standard role
                
                // Try attendee_profiles first
                val profUrl = URL("\/rest/v1/attendee_profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer \")'''

att_good = '''val sessionObj = responseObj.optJSONObject("session")
                val token = sessionObj?.optString("access_token") ?: ANON_KEY
                val newUserId = userObj.getString("id")
                
                // 2. Insert Profile
                profileData.put("id", newUserId)
                profileData.put("role", "attendee") // fallback standard role
                
                // Try attendee_profiles first
                val profUrl = URL("\/rest/v1/attendee_profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", ANON_KEY)
                profConn.setRequestProperty("Authorization", "Bearer \")'''

text = text.replace(att_bad, att_good)

fall_bad = 'fallbackConn.setRequestProperty("Authorization", "Bearer \")'
fall_good = 'fallbackConn.setRequestProperty("Authorization", "Bearer \")'

text = text.replace(fall_bad, fall_good)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/SupabaseApi.kt', 'w', encoding='utf-8') as f:
    f.write(text)
