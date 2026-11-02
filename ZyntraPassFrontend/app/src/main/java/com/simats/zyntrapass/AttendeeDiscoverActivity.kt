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

class AttendeeDiscoverActivity : AppCompatActivity() {

    private val profilesMap = mutableMapOf<String, JSONObject>()
    private val registrationsMap = mutableMapOf<String, String>()
    private val volunteersMap = mutableMapOf<String, JSONObject>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_attendee_discover)
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
            val eventsArray = SupabaseApi.fetchAllEvents() ?: return@launch
            
            // Collect organizers
            val orgIds = mutableListOf<String>()
            for (i in 0 until eventsArray.length()) {
                val orgId = eventsArray.getJSONObject(i).optString("organizer_id")
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
            
            // Fetch registrations
            val regs = SupabaseApi.fetchAttendeeRegistrations(currentUserId)
            if (regs != null) {
                for (i in 0 until regs.length()) {
                    val r = regs.getJSONObject(i)
                    registrationsMap[r.optString("event_id")] = r.optString("status")
                }
            }

            val vols = SupabaseApi.fetchMyVolunteerRequests(currentUserId)
            if (vols != null) {
                for (i in 0 until vols.length()) {
                    val v = vols.getJSONObject(i)
                    volunteersMap[v.optString("event_id")] = v
                }
            }
            
            renderEvents(eventsArray)
        }
    }

    private fun renderEvents(events: JSONArray) {
        val container = findViewById<LinearLayout>(R.id.eventsContainer)
        container.removeAllViews()
        
        if (events.length() == 0) {
            val tv = TextView(this).apply {
                text = "No events found."
                setPadding(40, 40, 40, 40)
                textSize = 16f
            }
            container.addView(tv)
            return
        }

        val inflater = LayoutInflater.from(this)
        for (i in 0 until events.length()) {
            val ev = events.getJSONObject(i)
            val eventId = ev.optString("id")
            val orgId = ev.optString("organizer_id")
            
            val org = profilesMap[orgId]
            val orgName = org?.optString("institution")?.takeIf { it.isNotBlank() } 
                          ?: org?.optString("full_name")?.takeIf { it.isNotBlank() } 
                          ?: "Unknown Organizer"
            
            val isRegistered = registrationsMap.containsKey(eventId)
            val cat = ev.optString("category", "General").takeIf { it.isNotBlank() } ?: "General"
            
            val view = inflater.inflate(R.layout.item_discover_card, container, false)
            
            view.findViewById<TextView>(R.id.tvCardType).text = cat
            view.findViewById<TextView>(R.id.tvCardMatch).text = "${(60..99).random()}% Match" // Dummy
            view.findViewById<TextView>(R.id.tvCardLocationTop).text = "📍 " + ev.optString("venue_name", "Online")
            view.findViewById<TextView>(R.id.tvEventTitle).text = ev.optString("title", "Untitled")
            view.findViewById<TextView>(R.id.tvEventOrg).text = orgName
            view.findViewById<TextView>(R.id.tvDate).text = "📅 " + ev.optString("start_date", "TBA")
            view.findViewById<TextView>(R.id.tvTime).text = "🕒 " + ev.optString("start_time", "TBA")
            view.findViewById<TextView>(R.id.tvDistance).text = "📍 " + ev.optString("address", "Various")
            view.findViewById<TextView>(R.id.tvTag1).text = cat

            
            val btnView = view.findViewById<Button>(R.id.btnView)
            btnView.setOnClickListener {
                val intent = android.content.Intent(this, EventDetailActivity::class.java)
                intent.putExtra("eventId", eventId)
                intent.putExtra("isRegistered", isRegistered)
                startActivity(intent)
            }

            val btnRegister = view.findViewById<Button>(R.id.btnRegister)
            val btnVolunteer = view.findViewById<Button>(R.id.btnVolunteer)
            
            val volRecord = volunteersMap[eventId]
            
            if (isRegistered) {
                btnRegister.isEnabled = false
                btnRegister.text = "Registered"
                btnRegister.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnRegister.setTextColor(Color.parseColor("#64748B"))
                btnVolunteer.visibility = android.view.View.GONE
            } else {
                btnRegister.setOnClickListener {
                    handleRegister(eventId, btnRegister, orgId, false)
                }
                
                if (volRecord != null) {
                    val status = volRecord.optString("status")
                    val code = volRecord.optString("secret_code")
                    btnVolunteer.isEnabled = false
                    btnVolunteer.setBackgroundColor(Color.parseColor("#E2E8F0"))
                    btnVolunteer.setTextColor(Color.parseColor("#64748B"))
                    
                    if (status == "approved") {
                        btnVolunteer.text = "Volunteer Code: $code"
                        btnVolunteer.setTextColor(Color.parseColor("#10B981")) // Green text for approved code
                    } else {
                        btnVolunteer.text = "Volunteer Pending"
                    }
                } else {
                    btnVolunteer.setOnClickListener {
                        handleRegister(eventId, btnVolunteer, orgId, true)
                    }
                }
            }
            
            container.addView(view)
        }
    }
    
    private fun handleRegister(eventId: String, btn: Button, orgId: String, isVolunteer: Boolean) {
        val currentUserId = SupabaseApi.currentUserId ?: return
        btn.isEnabled = false
        btn.text = "Registering..."
        
        CoroutineScope(Dispatchers.Main).launch {
            val success = if (isVolunteer) {
                SupabaseApi.registerAsVolunteer(eventId, orgId, currentUserId)
            } else {
                SupabaseApi.registerForEvent(eventId, currentUserId)
            }
            
            if (success) {
                Toast.makeText(this@AttendeeDiscoverActivity, if (isVolunteer) "Volunteer request sent!" else "Registered!", Toast.LENGTH_SHORT).show()
                btn.text = if (isVolunteer) "Pending" else "Registered"
                btn.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btn.setTextColor(Color.parseColor("#64748B"))
                registrationsMap[eventId] = if (isVolunteer) "pending" else "registered"
            } else {
                Toast.makeText(this@AttendeeDiscoverActivity, "Error registering", Toast.LENGTH_SHORT).show()
                btn.isEnabled = true
                btn.text = "Register"
            }
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
