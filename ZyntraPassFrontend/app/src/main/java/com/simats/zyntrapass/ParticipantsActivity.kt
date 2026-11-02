package com.simats.zyntrapass

import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.LinearLayout
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
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ParticipantsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_participants)
        setupBottomNav()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainParticipants)) { v, insets ->
            val sb = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(sb.left, sb.top, sb.right, 0)
            insets
        }

        findViewById<android.widget.ImageView>(R.id.btnMenu).setOnClickListener {
            startActivity(Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }

        // Avatar
        val name = SupabaseApi.currentUserName ?: "User"
        val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
        findViewById<TextView>(R.id.tvUserAvatar).text = initials

        // Bottom nav
        findViewById<View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }
        findViewById<View>(R.id.navEvents)?.setOnClickListener {
            startActivity(Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<View>(R.id.navLive)?.setOnClickListener {
            startActivity(Intent(this, LiveAttendanceActivity::class.java))
            finish()
        }

        loadEventsWithCounts()
    }

    private fun loadEventsWithCounts() {
        val feed = findViewById<LinearLayout>(R.id.llEventsFeed)
        CoroutineScope(Dispatchers.Main).launch {
            val events = SupabaseApi.fetchOrganizerEvents()
            feed.removeAllViews()

            if (events == null || events.length() == 0) {
                feed.addView(makeTextView("No events found. Create an event first."))
                return@launch
            }

            // Collect all event IDs to fetch counts in one call
            val eventIds = (0 until events.length()).map { events.getJSONObject(it).optString("id") }
            val allRegs = SupabaseApi.fetchRegistrationCountsForEvents(eventIds) ?: JSONArray()

            // Build counts map: eventId -> {total, pending}
            val counts = mutableMapOf<String, Pair<Int, Int>>() // total, pending
            eventIds.forEach { counts[it] = Pair(0, 0) }
            for (i in 0 until allRegs.length()) {
                val r = allRegs.getJSONObject(i)
                val eid = r.optString("event_id")
                val status = r.optString("status")
                val cur = counts[eid] ?: Pair(0, 0)
                val newTotal = cur.first + 1
                val newPending = cur.second + if (status == "registered") 1 else 0
                counts[eid] = Pair(newTotal, newPending)
            }

            // Render each event card
            for (i in 0 until events.length()) {
                val ev = events.getJSONObject(i)
                val eventId = ev.optString("id")
                val title = ev.optString("title", "Untitled")
                val status = computeStatus(ev)
                val (total, pending) = counts[eventId] ?: Pair(0, 0)

                val cardView = layoutInflater.inflate(R.layout.item_event_participant_card, feed, false)

                // Title
                cardView.findViewById<TextView>(R.id.tvEventTitle).text = title

                // Status chip
                val chip = cardView.findViewById<TextView>(R.id.tvStatusChip)
                chip.text = status
                val (bgHex, fgHex) = when (status) {
                    "upcoming"  -> Pair("#EEF2FF", "#3B35A8")
                    "ongoing"   -> Pair("#DCFCE7", "#166534")
                    "completed" -> Pair("#F1F5F9", "#475569")
                    "cancelled" -> Pair("#FEE2E2", "#991B1B")
                    else        -> Pair("#EEF2FF", "#3B35A8")
                }
                chip.backgroundTintList = ColorStateList.valueOf(Color.parseColor(bgHex))
                chip.setTextColor(Color.parseColor(fgHex))

                // Status color bar
                cardView.findViewById<View>(R.id.vStatusBar).backgroundTintList =
                    ColorStateList.valueOf(Color.parseColor(fgHex))

                // Total requests
                cardView.findViewById<TextView>(R.id.tvTotalRequests).text =
                    "$total request${if (total != 1) "s" else ""} total"

                // Pending badge
                val pendingBadge = cardView.findViewById<TextView>(R.id.tvPendingBadge)
                if (pending == 0) {
                    pendingBadge.text = "No pending"
                    pendingBadge.setTextColor(Color.parseColor("#94A3B8"))
                    pendingBadge.backgroundTintList = ColorStateList.valueOf(Color.parseColor("#F1F5F9"))
                } else {
                    pendingBadge.text = "$pending pending"
                    pendingBadge.setTextColor(Color.parseColor("#D97706"))
                    pendingBadge.backgroundTintList = ColorStateList.valueOf(Color.parseColor("#FFF4E5"))
                }

                // Click → detail screen
                cardView.setOnClickListener {
                    val intent = Intent(this@ParticipantsActivity, ParticipantDetailActivity::class.java)
                    intent.putExtra("event_id", eventId)
                    intent.putExtra("event_title", title)
                    startActivity(intent)
                }

                feed.addView(cardView)
            }
        }
    }

    private fun computeStatus(ev: JSONObject): String {
        val stored = ev.optString("status", "upcoming").lowercase()
        if (stored == "cancelled") return "cancelled"
        val now = Date()
        val sdf = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())
        val startDate = ev.optString("start_date", "")
        val startTime = ev.optString("start_time", "00:00").let { if (it.length >= 5) it.substring(0, 5) else "00:00" }
        val endDate   = ev.optString("end_date", "")
        val endTime   = ev.optString("end_time", "23:59").let { if (it.length >= 5) it.substring(0, 5) else "23:59" }
        if (startDate.isEmpty()) return stored
        return try {
            val startDt = sdf.parse("$startDate $startTime") ?: return stored
            val endDt   = if (endDate.isNotEmpty()) sdf.parse("$endDate $endTime") else null
            when {
                now.before(startDt)              -> "upcoming"
                endDt != null && now.after(endDt) -> "completed"
                else                              -> "ongoing"
            }
        } catch (e: Exception) { stored }
    }

    private fun makeTextView(msg: String) = TextView(this).apply {
        text = msg
        textSize = 14f
        gravity = android.view.Gravity.CENTER
        setTextColor(Color.parseColor("#64748B"))
        setPadding(0, 80, 0, 0)
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