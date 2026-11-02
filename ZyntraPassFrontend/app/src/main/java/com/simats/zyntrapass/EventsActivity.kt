package com.simats.zyntrapass

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.ImageView
import com.bumptech.glide.Glide
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject
import org.json.JSONArray
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class EventsActivity : AppCompatActivity() {

    private var allEvents: JSONArray? = null
    private var currentFilter = "all"
    private var searchQuery = ""

    /** Compute real-time status from start/end date+time fields */
    private fun computeStatus(ev: JSONObject): String {
        val storedStatus = ev.optString("status", "upcoming").lowercase()
        if (storedStatus == "cancelled") return "cancelled"

        val now = Date()
        val sdf = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())

        val startDate = ev.optString("start_date", "")
        val startTime = ev.optString("start_time", "00:00").let { if (it.length >= 5) it.substring(0, 5) else "00:00" }
        val endDate   = ev.optString("end_date", "")
        val endTime   = ev.optString("end_time", "23:59").let { if (it.length >= 5) it.substring(0, 5) else "23:59" }

        if (startDate.isEmpty()) return storedStatus

        return try {
            val startDt = sdf.parse("$startDate $startTime") ?: return storedStatus
            val endDt   = if (endDate.isNotEmpty()) sdf.parse("$endDate $endTime") else null

            when {
                now.before(startDt) -> "upcoming"
                endDt != null && now.after(endDt) -> "completed"
                else -> "ongoing"
            }
        } catch (e: Exception) {
            storedStatus
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_events)
        setupBottomNav()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainEvents)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, 0) // Keep bottom for nav
            insets
        }

        // Setup Avatar
        findViewById<ImageView>(R.id.btnMenu).setOnClickListener {
            startActivity(Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }

        val avatar = findViewById<TextView>(R.id.tvUserAvatar)
        val name = SupabaseApi.currentUserName ?: "User"
        avatar.text = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)

        findViewById<View>(R.id.btnCreateEvent).setOnClickListener {
            startActivity(Intent(this, CreateEventActivity::class.java))
        }

        // Bottom Nav setup
        findViewById<View>(R.id.navDashboard).setOnClickListener {
            startActivity(Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }

        // Participants nav — index 2 of bottomNav (no id assigned in layout)
        val bottomNav = findViewById<LinearLayout>(R.id.bottomNav)
        bottomNav.getChildAt(2)?.setOnClickListener {
            startActivity(Intent(this, ParticipantsActivity::class.java))
            finish()
        }
        
        // Live nav - index 3
        bottomNav.getChildAt(3)?.setOnClickListener {
            startActivity(Intent(this, LiveAttendanceActivity::class.java))
            finish()
        }

        setupTabs()

        findViewById<android.widget.EditText>(R.id.etSearch).addTextChangedListener(object : android.text.TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: android.text.Editable?) {
                searchQuery = s.toString().trim().lowercase()
                renderEvents()
            }
        })
        loadEvents()
    }

    private fun loadEvents() {
        CoroutineScope(Dispatchers.Main).launch {
            allEvents = SupabaseApi.fetchOrganizerEvents()
            updateBadges()
            renderEvents()
        }
    }

    private fun setupTabs() {
        val tabIds = listOf(
            Triple(R.id.tabAll, "all", R.id.badgeAll),
            Triple(R.id.tabUpcoming, "upcoming", R.id.badgeUpcoming),
            Triple(R.id.tabOngoing, "ongoing", R.id.badgeOngoing),
            Triple(R.id.tabCompleted, "completed", R.id.badgeCompleted),
            Triple(R.id.tabCancelled, "cancelled", R.id.badgeCancelled)
        )

        tabIds.forEach { (tabId, filter, badgeId) ->
            findViewById<View>(tabId).setOnClickListener {
                currentFilter = filter
                // Reset all tabs styles
                tabIds.forEach { (id, _, bId) ->
                    val tab = findViewById<LinearLayout>(id)
                    tab.setBackgroundResource(0) // Remove underline
                    (tab.getChildAt(0) as TextView).setTextColor(android.graphics.Color.parseColor("#475569"))
                    findViewById<TextView>(bId).apply {
                        setTextColor(android.graphics.Color.parseColor("#334155"))
                        backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#F1F5F9"))
                    }
                }
                
                // Set active style
                val activeTab = findViewById<LinearLayout>(tabId)
                activeTab.setBackgroundResource(R.drawable.bg_tab_indicator)
                (activeTab.getChildAt(0) as TextView).setTextColor(android.graphics.Color.parseColor("#3B35A8"))
                findViewById<TextView>(badgeId).apply {
                    setTextColor(android.graphics.Color.parseColor("#3B35A8"))
                    backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#EEF2FF"))
                }

                renderEvents()
            }
        }
    }

    private fun updateBadges() {
        val counts = mutableMapOf("all" to 0, "upcoming" to 0, "ongoing" to 0, "completed" to 0, "cancelled" to 0)
        
        allEvents?.let { events ->
            counts["all"] = events.length()
            for (i in 0 until events.length()) {
                val status = computeStatus(events.getJSONObject(i))
                counts[status] = (counts[status] ?: 0) + 1
            }
        }

        findViewById<TextView>(R.id.badgeAll).text = counts["all"].toString()
        findViewById<TextView>(R.id.badgeUpcoming).text = counts["upcoming"].toString()
        findViewById<TextView>(R.id.badgeOngoing).text = counts["ongoing"].toString()
        findViewById<TextView>(R.id.badgeCompleted).text = counts["completed"].toString()
        findViewById<TextView>(R.id.badgeCancelled).text = counts["cancelled"].toString()
    }

    private fun renderEvents() {
        val feed = findViewById<LinearLayout>(R.id.llEventsFeed)
        feed.removeAllViews()

        if (allEvents == null || allEvents!!.length() == 0) {
            val empty = TextView(this).apply {
                text = "No events found."
                textSize = 14f
                gravity = android.view.Gravity.CENTER
                setTextColor(android.graphics.Color.parseColor("#64748B"))
                setPadding(0, 100, 0, 0)
            }
            feed.addView(empty)
            return
        }

        var renderedCount = 0
        for (i in 0 until allEvents!!.length()) {
            val ev = allEvents!!.getJSONObject(i)
            val status = computeStatus(ev)
            
            if (currentFilter != "all" && status != currentFilter) continue
            val titleStr = ev.optString("title", "").lowercase()
            if (searchQuery.isNotEmpty() && !titleStr.contains(searchQuery)) continue
            
            val view = layoutInflater.inflate(R.layout.item_event_card, feed, false)
            
            // Status badge with color coding
            val statusBadge = view.findViewById<TextView>(R.id.tvStatusBadge)
            statusBadge.text = status
            val (bgColor, textColor) = when (status) {
                "upcoming"  -> Pair("#EEF2FF", "#3B35A8")
                "ongoing"   -> Pair("#DCFCE7", "#166534")
                "completed" -> Pair("#F1F5F9", "#475569")
                "cancelled" -> Pair("#FEE2E2", "#991B1B")
                else        -> Pair("#EEF2FF", "#3B35A8")
            }
            statusBadge.setTextColor(android.graphics.Color.parseColor(textColor))
            statusBadge.backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor(bgColor))

            view.findViewById<TextView>(R.id.tvCategoryBadge).text = ev.optString("category", "Event")
            view.findViewById<TextView>(R.id.tvCheckpointsBadge).text = "${ev.optInt("checkpoints_count", 0)} checkpoints"
            view.findViewById<TextView>(R.id.tvEventTitle).text = ev.optString("title", "Untitled event")
            
            val bannerUrl = ev.optString("banner_image_url", "")
            val ivBanner = view.findViewById<ImageView>(R.id.ivEventImage)
            if (bannerUrl.isNotEmpty()) {
                Glide.with(this).load(bannerUrl).into(ivBanner)
            } else {
                ivBanner.setBackgroundColor(android.graphics.Color.parseColor("#F1F5F9"))
            }

            feed.addView(view)
            renderedCount++
        }

        if (renderedCount == 0) {
            val empty = TextView(this).apply {
                text = "No events in this category."
                textSize = 14f
                gravity = android.view.Gravity.CENTER
                setTextColor(android.graphics.Color.parseColor("#64748B"))
                setPadding(0, 100, 0, 0)
            }
            feed.addView(empty)
        }
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