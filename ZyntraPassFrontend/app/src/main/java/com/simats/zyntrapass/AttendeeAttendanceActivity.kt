package com.simats.zyntrapass

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject

class AttendeeAttendanceActivity : AppCompatActivity() {

    private val profilesMap = mutableMapOf<String, JSONObject>()
    private val registrationsMap = mutableMapOf<String, String>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_attendee_attendance)
        setupBottomNav()
        setupSidebar()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainAttendeeDiscover)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, 0)
            insets
        }

        findViewById<LinearLayout>(R.id.navDashboard).setOnClickListener {
            startActivity(Intent(this, AttendeeDashboardActivity::class.java))
            finish()
        }

        loadAvatar()
        loadEvents()
    }

    private fun loadAvatar() {
        val currentUserId = SupabaseApi.currentUserId ?: return
        CoroutineScope(Dispatchers.Main).launch {
            var profileData: JSONObject? = null
            try { profileData = SupabaseApi.fetchAttendeeProfile(currentUserId) } catch (e: Exception) {}
            if (profileData == null) {
                val profiles = SupabaseApi.fetchProfilesByIds(listOf(currentUserId))
                if (profiles != null && profiles.length() > 0) profileData = profiles.getJSONObject(0)
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

    
    private fun loadEvents() {
        val currentUserId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            val eventsArray = SupabaseApi.fetchAllEvents() ?: org.json.JSONArray()
            val logsArray = SupabaseApi.fetchAttendeeLogs(currentUserId) ?: org.json.JSONArray()
            
            // Build map of events
            val eventsMap = mutableMapOf<String, JSONObject>()
            val orgIds = mutableListOf<String>()
            for (i in 0 until eventsArray.length()) {
                val ev = eventsArray.getJSONObject(i)
                eventsMap[ev.optString("id")] = ev
                val orgId = ev.optString("organizer_id")
                if (orgId.isNotEmpty() && !orgIds.contains(orgId)) orgIds.add(orgId)
            }
            
            // Fetch organizers
            if (orgIds.isNotEmpty()) {
                val orgProfiles = SupabaseApi.fetchProfilesByIds(orgIds)
                if (orgProfiles != null) {
                    for (i in 0 until orgProfiles.length()) {
                        val p = orgProfiles.getJSONObject(i)
                        profilesMap[p.optString("id")] = p
                    }
                }
            }
            
            renderLogs(logsArray, eventsMap)
        }
    }

    private fun renderLogs(logs: JSONArray, eventsMap: Map<String, JSONObject>) {
        val container = findViewById<LinearLayout>(R.id.eventsContainer)
        container.removeAllViews()
        
        if (logs.length() == 0) {
            val tv = TextView(this).apply {
                text = "No attendance history found."
                setPadding(40, 40, 40, 40)
                textSize = 16f
            }
            container.addView(tv)
            return
        }

        val inflater = LayoutInflater.from(this)
        for (i in 0 until logs.length()) {
            val log = logs.getJSONObject(i)
            val eventId = log.optString("event_id")
            val ev = eventsMap[eventId] ?: continue
            val orgId = ev.optString("organizer_id")
            
            val org = profilesMap[orgId]
            val orgName = org?.optString("institution")?.takeIf { it.isNotBlank() } 
                          ?: org?.optString("full_name")?.takeIf { it.isNotBlank() } 
                          ?: "Unknown Organizer"
            
            val cat = ev.optString("category", "General").takeIf { it.isNotBlank() } ?: "General"
            
            val view = inflater.inflate(R.layout.item_discover_card, container, false)
            
            view.findViewById<TextView>(R.id.tvCardType).text = "Checked In"
            view.findViewById<TextView>(R.id.tvCardMatch).text = "Verified"
            view.findViewById<TextView>(R.id.tvCardLocationTop).text = "" + ev.optString("venue_name", "Online")
            view.findViewById<TextView>(R.id.tvEventTitle).text = ev.optString("title", "Untitled")
            view.findViewById<TextView>(R.id.tvEventOrg).text = orgName
            
            val checkInTime = log.optString("scanned_at", "Unknown").replace("T", " ").take(16)
            view.findViewById<TextView>(R.id.tvDate).text = "" + checkInTime
            view.findViewById<TextView>(R.id.tvTime).text = ""
            view.findViewById<TextView>(R.id.tvDistance).text = "" + ev.optString("address", "Various")
            view.findViewById<TextView>(R.id.tvTag1).text = cat

            val btnRegister = view.findViewById<Button>(R.id.btnRegister)
            btnRegister.isEnabled = false
            btnRegister.text = "Attended"
            btnRegister.setBackgroundColor(android.graphics.Color.parseColor("#10B981"))
            btnRegister.setTextColor(android.graphics.Color.parseColor("#FFFFFF"))
            
            val btnView = view.findViewById<Button>(R.id.btnView)
            btnView.visibility = android.view.View.GONE
            
            container.addView(view)
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
