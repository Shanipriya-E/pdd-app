package com.simats.zyntrapass

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray

class VolunteerDashboardActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_volunteer_dashboard)
        
        findViewById<TextView>(R.id.btnLogout).setOnClickListener {
            getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).edit().clear().apply()
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }
        
        findViewById<Button>(R.id.btnScan).setOnClickListener {
            startActivity(Intent(this, VolunteerScanActivity::class.java))
        }
        findViewById<View>(R.id.navScan)?.setOnClickListener {
            startActivity(Intent(this, VolunteerScanActivity::class.java))
        }
        
        findViewById<View>(R.id.navParticipants)?.setOnClickListener {
            startActivity(Intent(this, VolunteerParticipantsActivity::class.java))
        }
        
        loadEventDetails()
    }
    
    private fun loadEventDetails() {
        val prefs = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE)
        val eventId = prefs.getString("event_id", "") ?: ""
        val userId = SupabaseApi.currentUserId
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Fetch Greeting
                if (userId != null) {
                    val profile = SupabaseApi.fetchAttendeeProfile(userId)
                    if (profile != null) {
                        val fullName = profile.optString("full_name", "")
                        val firstName = fullName.split(" ").firstOrNull() ?: "Volunteer"
                        
                        val hour = java.util.Calendar.getInstance().get(java.util.Calendar.HOUR_OF_DAY)
                        val greet = when (hour) {
                            in 0..11 -> "Good morning"
                            in 12..16 -> "Good afternoon"
                            else -> "Good evening"
                        }
                        
                        withContext(Dispatchers.Main) {
                            findViewById<TextView>(R.id.tvGreeting).text = "$greet, $firstName"
                        }
                    }
                }

                // Fetch Event Details
                val res = SupabaseApi.get("rest/v1/events?id=eq.$eventId")
                if (res != null) {
                    val array = JSONArray(res)
                    if (array.length() > 0) {
                        val obj = array.getJSONObject(0)
                        
                        val title = obj.optString("title", "Event")
                        val date = obj.optString("start_date", "")
                        val startTime = obj.optString("start_time", "")
                        val endTime = obj.optString("end_time", "")
                        val venue = obj.optString("venue_name", "Online").takeIf { it.isNotBlank() } ?: "Online"
                        
                        val checkpoints = obj.optInt("checkpoints_count", 4)
                        val radius = obj.optInt("attendance_radius_meters", 100)
                        val qrRefresh = obj.optInt("qr_refresh_interval_sec", 60)
                        
                        val timeStr = if (endTime.isNotBlank()) "$startTime to $endTime" else startTime
                        val meta = "$date · $timeStr · $venue"
                        val details = "$checkpoints checkpoints · $radius m geofence · QR expires every ${qrRefresh}s"
                        
                        withContext(Dispatchers.Main) {
                            findViewById<TextView>(R.id.tvEventName).text = title
                            findViewById<TextView>(R.id.tvEventMeta)?.text = meta
                            findViewById<TextView>(R.id.tvEventDetails)?.text = details
                        }
                    }
                }
            } catch (e: Exception) { e.printStackTrace() }
        }
    }
}
