package com.simats.zyntrapass

import android.content.Intent
import android.os.Bundle
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject

class AttendeeDashboardActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_attendee_dashboard)
        setupBottomNav()
        setupSidebar()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainAttendeeDashboard)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        

        loadProfile()
        loadStats()
    }

    private fun loadProfile() {
        val currentUserId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            // Try fetching attendee_profiles first
            var profileData: JSONObject? = null
            try {
                profileData = SupabaseApi.fetchAttendeeProfile(currentUserId)
            } catch(e: Exception) { e.printStackTrace() }
            
            if (profileData == null) {
                // fallback to main profiles table
                val profiles = SupabaseApi.fetchProfilesByIds(listOf(currentUserId))
                if (profiles != null && profiles.length() > 0) {
                    profileData = profiles.getJSONObject(0)
                }
            }

            if (profileData != null) {
                val fullName = profileData.optString("full_name", "User")
                if (fullName.isNotBlank()) {
                    val initials = fullName.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
                    findViewById<TextView>(R.id.tvAvatar).text = if (initials.isNotEmpty()) initials else "NU"
                }
            }
        }
    }

    private fun loadStats() {
        val currentUserId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            val regs = SupabaseApi.fetchAttendeeRegistrations(currentUserId)
            val vols = SupabaseApi.fetchMyVolunteerRequests(currentUserId)
            val logs = SupabaseApi.fetchAttendeeLogs(currentUserId)
            
            var totalRegistered = 0
            var upcoming = 0
            val attendedEventIds = mutableSetOf<String>()
            
            // Collect all unique event IDs we are registered for
            val registeredEventsMap = mutableMapOf<String, String>()
            
            if (regs != null) {
                for (i in 0 until regs.length()) {
                    val obj = regs.getJSONObject(i)
                    registeredEventsMap[obj.optString("event_id")] = obj.optString("status")
                }
            }
            if (vols != null) {
                for (i in 0 until vols.length()) {
                    val obj = vols.getJSONObject(i)
                    // If approved volunteer, treat as registered
                    if (obj.optString("status") == "approved") {
                        registeredEventsMap[obj.optString("event_id")] = "approved"
                    }
                }
            }
            
            totalRegistered = registeredEventsMap.size

            // Add from logs
            if (logs != null) {
                for (i in 0 until logs.length()) {
                    attendedEventIds.add(logs.getJSONObject(i).optString("event_id"))
                }
            }
            
            // Add from status
            for ((eventId, status) in registeredEventsMap) {
                if (status == "attended" || status == "verified") {
                    attendedEventIds.add(eventId)
                }
            }
            
            // Now calculate upcoming (excluding those already attended via GPS/status)
            for ((eventId, status) in registeredEventsMap) {
                if ((status == "approved" || status == "registered") && !attendedEventIds.contains(eventId)) {
                    upcoming++
                }
            }

            findViewById<TextView>(R.id.tvUpcomingCount).text = upcoming.toString()
            findViewById<TextView>(R.id.tvRegisteredCount).text = totalRegistered.toString()
            findViewById<TextView>(R.id.tvAttendedCount).text = attendedEventIds.size.toString()
        }
    }

    private fun setupBottomNav() { 
        findViewById<android.view.View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeDashboardActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navDiscover)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeDiscoverActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navMy)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeEventsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navAttendance)?.setOnClickListener {
            startActivity(android.content.Intent(this, AttendeeAttendanceActivity::class.java))
            finish()
        }
    }

    // ── Sidebar helper ──────────────────────────────────────────────────
    private fun setupSidebar() {
        val sidebar = findViewById<android.view.View>(R.id.sidebarPanel)
        val dim     = findViewById<android.view.View>(R.id.sidebarDim)
        val btnMenu = findViewById<android.view.View>(R.id.btnMenu)

        fun openSidebar() {
            sidebar.visibility = android.view.View.VISIBLE
            dim.visibility     = android.view.View.VISIBLE
            sidebar.animate().translationX(0f).setDuration(250).start()
            dim.animate().alpha(1f).setDuration(250).start()
        }
        fun closeSidebar() {
            sidebar.animate().translationX(-sidebar.width.toFloat()).setDuration(200).withEndAction {
                sidebar.visibility = android.view.View.GONE
            }.start()
            dim.animate().alpha(0f).setDuration(200).withEndAction {
                dim.visibility = android.view.View.GONE
            }.start()
        }

        // Load name into sidebar avatar
        val currentUserId = SupabaseApi.currentUserId
        if (currentUserId != null) {
            kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
                val profiles = SupabaseApi.fetchProfilesByIds(listOf(currentUserId))
                if (profiles != null && profiles.length() > 0) {
                    val name = profiles.getJSONObject(0).optString("full_name", "User")
                    val email = profiles.getJSONObject(0).optString("email", SupabaseApi.currentUserEmail ?: "")
                    val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2).ifEmpty { "U" }
                    findViewById<android.widget.TextView>(R.id.sidebarAvatar)?.text = initials
                    findViewById<android.widget.TextView>(R.id.sidebarName)?.text = name
                }
            }
        }

        btnMenu?.setOnClickListener { openSidebar() }
        dim?.setOnClickListener   { closeSidebar() }

        sidebar?.alpha = 1f
        sidebar?.translationX = -1500f   // start offscreen

        findViewById<android.view.View>(R.id.sidebarNavDashboard)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeDashboardActivity) {
                startActivity(android.content.Intent(this, AttendeeDashboardActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavDiscover)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeDiscoverActivity) {
                startActivity(android.content.Intent(this, AttendeeDiscoverActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavMyEvents)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeEventsActivity) {
                startActivity(android.content.Intent(this, AttendeeEventsActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavAttendance)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeAttendanceActivity) {
                startActivity(android.content.Intent(this, AttendeeAttendanceActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavCerts)?.setOnClickListener {
            closeSidebar()
            startActivity(android.content.Intent(this, AttendeeCertificatesActivity::class.java)); finish()
        }
        findViewById<android.view.View>(R.id.sidebarNavSettings)?.setOnClickListener {
            closeSidebar()
            startActivity(android.content.Intent(this, SettingsActivity::class.java)); finish()
        }
        findViewById<android.view.View>(R.id.sidebarNavLogout)?.setOnClickListener {
            SupabaseApi.currentUserId = null
            SupabaseApi.currentUserRole = null
            SupabaseApi.currentUserToken = null
            startActivity(android.content.Intent(this, LoginActivity::class.java).apply { 
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK 
            })
        }
    }
    // ────────────────────────────────────────────────────────────────────

}
