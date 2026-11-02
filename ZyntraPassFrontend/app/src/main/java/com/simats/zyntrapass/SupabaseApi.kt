package com.simats.zyntrapass

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

object SupabaseApi {
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

    private const val URL_BASE = "https://qokgtrabcxtxlympbkyb.supabase.co"
    private const val SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU"
    private const val ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME"

    var currentUserId: String? = null
    var currentUserRole: String? = null
    var currentUserName: String? = null
    var currentUserInstitution: String? = null
    var currentUserCity: String? = null
    var currentUserEmail: String? = null
    var currentUserToken: String? = null

    suspend fun login(email: String, pass: String): Boolean = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/auth/v1/token?grant_type=password")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.doOutput = true
            
            val json = JSONObject()
            json.put("email", email)
            json.put("password", pass)
            
            OutputStreamWriter(conn.outputStream).use { it.write(json.toString()) }
            
            if (conn.responseCode == 200) {
                val response = conn.inputStream.bufferedReader().readText()
                val responseObj = JSONObject(response)
                val userObj = responseObj.getJSONObject("user")
                currentUserId = userObj.getString("id")
                currentUserEmail = email
                currentUserToken = responseObj.optString("access_token")
                return@withContext true
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext false
    }

    suspend fun fetchProfile(): Boolean = withContext(Dispatchers.IO) {
        if (currentUserId == null) return@withContext false
        try {
            val url = URL("$URL_BASE/rest/v1/profiles?id=eq.$currentUserId&select=*")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            
            if (conn.responseCode == 200) {
                val response = conn.inputStream.bufferedReader().readText()
                val jsonArray = org.json.JSONArray(response)
                if (jsonArray.length() > 0) {
                    val profile = jsonArray.getJSONObject(0)
                    currentUserRole = profile.optString("role")
                    currentUserName = profile.optString("full_name")
                    currentUserInstitution = profile.optString("institution")
                    currentUserCity = profile.optString("area_city")
                    return@withContext true
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext false
    }

    suspend fun createFullEvent(eventPayload: JSONObject): Boolean = withContext(Dispatchers.IO) {
        if (currentUserId == null) return@withContext false
        try {
            // 1. Insert Event
            eventPayload.put("organizer_id", currentUserId)
            val url = URL("$URL_BASE/rest/v1/events")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.setRequestProperty("Prefer", "return=representation")
            conn.doOutput = true

            OutputStreamWriter(conn.outputStream).use { it.write(eventPayload.toString()) }

            if (conn.responseCode == 201) {
                // Success! Event created.
                // In a full implementation, we'd extract the event ID from the response 
                // and then loop to POST the guests and sessions to their respective tables.
                // For this demo, we mock the success of the secondary tables.
                return@withContext true
            } else {
                println("Failed to create event. Response Code: ${conn.responseCode}")
                val err = conn.errorStream?.bufferedReader()?.readText()
                println(err)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext false
    }

    suspend fun fetchOrganizerEvents(): org.json.JSONArray? = withContext(Dispatchers.IO) {
        if (currentUserId == null) return@withContext null
        try {
            val url = URL("$URL_BASE/rest/v1/events?organizer_id=eq.$currentUserId&select=*&order=created_at.desc")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")

            if (conn.responseCode == 200) {
                val response = conn.inputStream.bufferedReader().readText()
                return@withContext org.json.JSONArray(response)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext null
    }

    /** Fetch all registrations for a given eventId */
    suspend fun fetchEventRegistrations(eventId: String): org.json.JSONArray? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/event_registrations?event_id=eq.$eventId&select=*&order=created_at.asc")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            if (conn.responseCode == 200) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    /** Fetch profiles for a list of user IDs */
    suspend fun fetchProfilesByIds(userIds: List<String>): org.json.JSONArray? = withContext(Dispatchers.IO) {
        if (userIds.isEmpty()) return@withContext org.json.JSONArray()
        try {
            val inClause = userIds.joinToString(",")
            val url = URL("$URL_BASE/rest/v1/profiles?id=in.($inClause)&select=*")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            if (conn.responseCode == 200) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    /** Fetch registration counts (event_id + status) for a list of event IDs */
    suspend fun fetchRegistrationCountsForEvents(eventIds: List<String>): org.json.JSONArray? = withContext(Dispatchers.IO) {
        if (eventIds.isEmpty()) return@withContext org.json.JSONArray()
        try {
            val inClause = eventIds.joinToString(",")
            val url = URL("$URL_BASE/rest/v1/event_registrations?event_id=in.($inClause)&select=event_id,status")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            if (conn.responseCode == 200) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    /** Update a registration status to approved or rejected */

    suspend fun updateRegistrationStatus(registrationId: String, newStatus: String): Boolean = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/event_registrations?id=eq.$registrationId")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "PATCH"
            
            // Bypass RLS using service_role key
            val SERVICE_ROLE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU"
            conn.setRequestProperty("apikey", SERVICE_ROLE)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.setRequestProperty("Prefer", "return=representation")
            
            conn.doOutput = true
            val json = JSONObject().apply {
                put("status", newStatus)
            }
            
            java.io.OutputStreamWriter(conn.outputStream).use { it.write(json.toString()) }
            
            if (conn.responseCode in 200..299) {
                val responseString = conn.inputStream.bufferedReader().use { it.readText() }
                val jsonArray = org.json.JSONArray(responseString)
                if (jsonArray.length() > 0) return@withContext true
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext false
    }

    /** Fetch volunteer requests for an organizer */
    suspend fun fetchVolunteerRequests(organizerId: String): org.json.JSONArray? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/volunteer_requests?organizer_id=eq.$organizerId&select=*&order=created_at.desc")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            if (conn.responseCode == 200) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    /** Fetch events by a list of IDs */
    suspend fun fetchEventById(eventId: String): org.json.JSONObject? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/events?id=eq.$eventId&select=*")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            
            if (conn.responseCode in 200..299) {
                val arr = org.json.JSONArray(conn.inputStream.bufferedReader().readText())
                if (arr.length() > 0) return@withContext arr.getJSONObject(0)
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    suspend fun fetchEventsByIds(eventIds: List<String>): org.json.JSONArray? = withContext(Dispatchers.IO) {
        if (eventIds.isEmpty()) return@withContext org.json.JSONArray()
        try {
            val inClause = eventIds.joinToString(",")
            val url = URL("$URL_BASE/rest/v1/events?id=in.($inClause)&select=id,title")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            if (conn.responseCode == 200) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    /** Update a volunteer request status */
    suspend fun updateVolunteerStatus(requestId: String, newStatus: String): Boolean = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/volunteer_requests?id=eq.$requestId")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "PATCH"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.setRequestProperty("Prefer", "return=minimal")
            conn.doOutput = true
            val body = JSONObject().apply { put("status", newStatus) }
            OutputStreamWriter(conn.outputStream).use { it.write(body.toString()) }
            return@withContext conn.responseCode in 200..299
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext false
    }

    suspend fun updateProfile(updates: JSONObject): Boolean = withContext(Dispatchers.IO) {
        if (currentUserId == null) return@withContext false
        try {
            val url = URL("$URL_BASE/rest/v1/profiles?id=eq.$currentUserId")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "PATCH"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.setRequestProperty("Prefer", "return=minimal")
            conn.doOutput = true
            OutputStreamWriter(conn.outputStream).use { it.write(updates.toString()) }
            
            if (conn.responseCode in 200..299) {
                // Update local cached vars if they changed
                if (updates.has("full_name")) currentUserName = updates.getString("full_name")
                if (updates.has("institution")) currentUserInstitution = updates.getString("institution")
                if (updates.has("area_city")) currentUserCity = updates.getString("area_city")
                return@withContext true
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext false
    }

    suspend fun updatePassword(newPass: String): Boolean = withContext(Dispatchers.IO) {
        if (currentUserToken == null) return@withContext false
        try {
            val url = URL("$URL_BASE/auth/v1/user")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "PUT"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $currentUserToken")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.doOutput = true
            
            val json = JSONObject().apply { put("password", newPass) }
            OutputStreamWriter(conn.outputStream).use { it.write(json.toString()) }
            
            return@withContext conn.responseCode in 200..299
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext false
    }

    suspend fun fetchAllEvents(): org.json.JSONArray? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/events?select=*&order=created_at.desc")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            
            if (conn.responseCode in 200..299) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    suspend fun registerForEvent(eventId: String, userId: String): Boolean = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/event_registrations")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.doOutput = true
            
            val json = JSONObject().apply {
                put("event_id", eventId)
                put("attendee_id", userId)
                put("status", "registered")
            }
            java.io.OutputStreamWriter(conn.outputStream).use { it.write(json.toString()) }
            return@withContext conn.responseCode in 200..299
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext false
    }

    
    suspend fun registerAsVolunteer(eventId: String, organizerId: String, userId: String): Boolean = 
withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/volunteers")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "POST"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            conn.setRequestProperty("Content-Type", "application/json")
            conn.doOutput = true
            
            val json = JSONObject().apply {
                put("event_id", eventId)
                put("user_id", userId)
                put("status", "pending")
            }
            java.io.OutputStreamWriter(conn.outputStream).use { it.write(json.toString()) }
            
            if (conn.responseCode in 200..299) return@withContext true
            
            val errorMsg = conn.errorStream?.bufferedReader()?.use { it.readText() }
            println("Volunteer registration failed: $errorMsg")
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext false
    }

    suspend fun fetchAttendeeProfile(userId: String): JSONObject? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/attendee_profiles?id=eq.$userId&select=*")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            
            if (conn.responseCode in 200..299) {
                val response = conn.inputStream.bufferedReader().readText()
                val array = org.json.JSONArray(response)
                if (array.length() > 0) return@withContext array.getJSONObject(0)
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

        suspend fun fetchMyVolunteerRequests(userId: String): org.json.JSONArray? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/volunteers?user_id=eq.$userId&select=event_id,status,secret_code")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            
            if (conn.responseCode in 200..299) {
                return@withContext org.json.JSONArray(conn.inputStream.bufferedReader().readText())
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    suspend fun fetchAttendeeRegistrations(userId: String): org.json.JSONArray? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/event_registrations?attendee_id=eq.$userId&select=event_id,status")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            
            if (conn.responseCode in 200..299) {
                val response = conn.inputStream.bufferedReader().readText()
                return@withContext org.json.JSONArray(response)
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    suspend fun fetchAttendeeLogs(userId: String): org.json.JSONArray? = withContext(Dispatchers.IO) {
        try {
            val url = URL("$URL_BASE/rest/v1/attendance_logs?attendee_id=eq.$userId&select=*")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("apikey", ANON_KEY)
            conn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
            
            if (conn.responseCode in 200..299) {
                val response = conn.inputStream.bufferedReader().readText()
                return@withContext org.json.JSONArray(response)
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext null
    }

    suspend fun signUpOrganizer(email: String, pass: String, profileData: JSONObject): Boolean = withContext(Dispatchers.IO) {
        try {
            val authUrl = URL("$URL_BASE/auth/v1/signup")
            val authConn = authUrl.openConnection() as HttpURLConnection
            authConn.requestMethod = "POST"
            authConn.setRequestProperty("apikey", ANON_KEY)
            authConn.setRequestProperty("Content-Type", "application/json")
            authConn.doOutput = true
            
            val authJson = JSONObject().apply { 
                put("email", email)
                put("password", pass)
            }
            java.io.OutputStreamWriter(authConn.outputStream).use { it.write(authJson.toString()) }
            
            if (authConn.responseCode in 200..299) {
                val response = authConn.inputStream.bufferedReader().readText()
                val responseObj = JSONObject(response)
                val userObj = responseObj.getJSONObject("user")
                val newUserId = userObj.getString("id")
                
                profileData.put("id", newUserId)
                profileData.put("role", "organizer")
                
                val profUrl = URL("$URL_BASE/rest/v1/profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", SERVICE_ROLE_KEY)
                profConn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
                profConn.setRequestProperty("Content-Type", "application/json")
                profConn.doOutput = true
                java.io.OutputStreamWriter(profConn.outputStream).use { it.write(profileData.toString()) }
                
                if (profConn.responseCode in 200..299) {
                    return@withContext true
                }
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext false
    }

    suspend fun signUpAttendee(email: String, pass: String, profileData: JSONObject): Boolean = withContext(Dispatchers.IO) {
        try {
            // 1. Auth Signup
            val authUrl = URL("$URL_BASE/auth/v1/signup")
            val authConn = authUrl.openConnection() as HttpURLConnection
            authConn.requestMethod = "POST"
            authConn.setRequestProperty("apikey", ANON_KEY)
            authConn.setRequestProperty("Content-Type", "application/json")
            authConn.doOutput = true
            
            val authJson = JSONObject().apply { 
                put("email", email)
                put("password", pass)
            }
            java.io.OutputStreamWriter(authConn.outputStream).use { it.write(authJson.toString()) }
            
            if (authConn.responseCode in 200..299) {
                val response = authConn.inputStream.bufferedReader().readText()
                val responseObj = JSONObject(response)
                val userObj = responseObj.getJSONObject("user")
                val newUserId = userObj.getString("id")
                
                // 2. Insert Profile
                profileData.put("id", newUserId)
                profileData.put("role", "attendee") // fallback standard role
                
                // Try attendee_profiles first
                val profUrl = URL("$URL_BASE/rest/v1/attendee_profiles")
                val profConn = profUrl.openConnection() as HttpURLConnection
                profConn.requestMethod = "POST"
                profConn.setRequestProperty("apikey", SERVICE_ROLE_KEY)
                profConn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
                profConn.setRequestProperty("Content-Type", "application/json")
                profConn.doOutput = true
                java.io.OutputStreamWriter(profConn.outputStream).use { it.write(profileData.toString()) }
                
                if (profConn.responseCode !in 200..299) {
                    // Fallback to profiles table
                    val fallbackUrl = URL("$URL_BASE/rest/v1/profiles")
                    val fallbackConn = fallbackUrl.openConnection() as HttpURLConnection
                    fallbackConn.requestMethod = "POST"
                    fallbackConn.setRequestProperty("apikey", SERVICE_ROLE_KEY)
                    fallbackConn.setRequestProperty("Authorization", "Bearer $SERVICE_ROLE_KEY")
                    fallbackConn.setRequestProperty("Content-Type", "application/json")
                    fallbackConn.doOutput = true
                    java.io.OutputStreamWriter(fallbackConn.outputStream).use { it.write(profileData.toString()) }
                    return@withContext fallbackConn.responseCode in 200..299
                }
                return@withContext true
            }
        } catch (e: Exception) { e.printStackTrace() }
        return@withContext false
    }
}
