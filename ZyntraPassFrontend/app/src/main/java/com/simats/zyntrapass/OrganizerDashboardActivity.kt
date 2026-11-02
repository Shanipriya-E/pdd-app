package com.simats.zyntrapass

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.GravityCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.drawerlayout.widget.DrawerLayout
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class OrganizerDashboardActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_organizer_dashboard)
        setupBottomNav()

        val drawerLayout = findViewById<DrawerLayout>(R.id.drawerLayout)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainDashboard)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(0, systemBars.top, 0, systemBars.bottom)
            insets
        }

        findViewById<ImageView>(R.id.btnMenu).setOnClickListener {
            drawerLayout.openDrawer(GravityCompat.START)
        }

        val name = SupabaseApi.currentUserName ?: "Organizer"
        val inst = SupabaseApi.currentUserInstitution ?: "Institution"
        val city = SupabaseApi.currentUserCity ?: "City"
        val email = SupabaseApi.currentUserEmail ?: "email@example.com"
        val initials = name.split(" ").mapNotNull { it.firstOrNull()?.toString() }.joinToString("").take(2).uppercase()

        // Populate Main Dashboard
        findViewById<TextView>(R.id.tvGreeting).text = "Good evening, $name"
        findViewById<TextView>(R.id.tvGreetingSub).text = "$inst · $city · 0 events"

        // Populate Sidebar
        findViewById<TextView>(R.id.tvSidebarAvatar).text = initials
        findViewById<TextView>(R.id.tvSidebarName).text = name
        findViewById<TextView>(R.id.tvSidebarEmail).text = email

        findViewById<TextView>(R.id.btnSidebarLogout).setOnClickListener {
            SupabaseApi.currentUserId = null
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }

        findViewById<View>(R.id.btnLiveAttendance)?.setOnClickListener {
            startActivity(Intent(this, LiveAttendanceActivity::class.java))
        }
        
        findViewById<View>(R.id.btnCreateEvent).setOnClickListener {
            startActivity(Intent(this, CreateEventActivity::class.java))
        }

        findViewById<View>(R.id.navEvents)?.setOnClickListener {
            startActivity(Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<View>(R.id.navParticipants)?.setOnClickListener {
            startActivity(Intent(this, ParticipantsActivity::class.java))
            finish()
        }

        // Sidebar nav
        findViewById<TextView>(R.id.navSidebarDashboard)?.setOnClickListener {
            // Already on Dashboard, just close drawer
            findViewById<androidx.drawerlayout.widget.DrawerLayout>(R.id.drawerLayout)?.closeDrawers()
        }
        findViewById<TextView>(R.id.navSidebarEvents)?.setOnClickListener {
            startActivity(Intent(this, EventsActivity::class.java))
        }
        findViewById<TextView>(R.id.navSidebarParticipants)?.setOnClickListener {
            startActivity(Intent(this, ParticipantsActivity::class.java))
        }
        findViewById<TextView>(R.id.navSidebarLive)?.setOnClickListener {
            // Can route to events or show toast since there's no LiveAttendanceActivity
            startActivity(Intent(this, LiveAttendanceActivity::class.java))
        }
        findViewById<TextView>(R.id.navSidebarVolunteers)?.setOnClickListener {
            startActivity(Intent(this, VolunteersActivity::class.java))
        }
        findViewById<TextView>(R.id.navSidebarCertificates)?.setOnClickListener {
            startActivity(Intent(this, CertificatesActivity::class.java))
        }
        findViewById<TextView>(R.id.navSidebarSettings)?.setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }

        setupCard(findViewById(R.id.cardEvents), "TOTAL EVENTS", "...", "Loading...", "📅")
        setupCard(findViewById(R.id.cardRegistrations), "REGISTRATIONS", "...", "Loading...", "👥")
        setupCard(findViewById(R.id.cardVerified), "VERIFIED ATTENDEES", "...", "Loading...", "✅")
        setupCard(findViewById(R.id.cardPending), "PENDING", "...", "Loading...", "⏳")
        setupCard(findViewById(R.id.cardCertificates), "CERTIFICATES", "...", "Loading...", "🎓")
        
        loadDashboardStats(inst, city)
    }

    private fun loadDashboardStats(inst: String, city: String) {
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            try {
                val eventsArray = SupabaseApi.fetchOrganizerEvents()
                var totalEvents = 0
                val eventIds = mutableListOf<String>()
                if (eventsArray != null) {
                    totalEvents = eventsArray.length()
                    for (i in 0 until totalEvents) {
                        eventIds.add(eventsArray.getJSONObject(i).getString("id"))
                    }
                }

                var totalRegs = 0
                var verifiedRegs = 0
                var pendingRegs = 0

                val regsArray = SupabaseApi.fetchRegistrationCountsForEvents(eventIds)
                if (regsArray != null) {
                    for (i in 0 until regsArray.length()) {
                        val status = regsArray.getJSONObject(i).optString("status", "")
                        if (status == "registered" || status == "approved" || status == "attended") totalRegs++
                        if (status == "attended") verifiedRegs++
                        if (status == "registered") pendingRegs++
                    }
                }

                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                    findViewById<TextView>(R.id.tvGreetingSub).text = "$inst • $city • $totalEvents events"
                    
                    setupCard(findViewById(R.id.cardEvents), "TOTAL EVENTS", totalEvents.toString(), "$totalEvents upcoming", "📅")
                    setupCard(findViewById(R.id.cardRegistrations), "REGISTRATIONS", totalRegs.toString(), "Across all events", "👥")
                    setupCard(findViewById(R.id.cardVerified), "VERIFIED ATTENDEES", verifiedRegs.toString(), "Checked in", "✅")
                    setupCard(findViewById(R.id.cardPending), "PENDING", pendingRegs.toString(), "Awaiting checkpoints", "⏳")
                    setupCard(findViewById(R.id.cardCertificates), "CERTIFICATES", verifiedRegs.toString(), "Issued", "🎓")
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    private fun setupCard(cardView: View, title: String, value: String, subtitle: String, icon: String) {
        cardView.findViewById<TextView>(R.id.tvStatTitle).text = title
        cardView.findViewById<TextView>(R.id.tvStatValue).text = value
        cardView.findViewById<TextView>(R.id.tvStatSubtitle).text = subtitle
        cardView.findViewById<TextView>(R.id.tvStatIcon).text = icon
    }

    private fun setupBottomNav() { 
        findViewById<android.view.View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(android.content.Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navEvents)?.setOnClickListener {
            startActivity(android.content.Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navParticipants)?.setOnClickListener {
            startActivity(android.content.Intent(this, ParticipantsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navLive)?.setOnClickListener {
            startActivity(android.content.Intent(this, LiveAttendanceActivity::class.java))
            finish()
        }
 }

}