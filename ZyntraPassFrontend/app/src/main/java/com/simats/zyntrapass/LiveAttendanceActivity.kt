package com.simats.zyntrapass

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class LiveAttendanceActivity : AppCompatActivity() {

    private var allEvents: JSONArray? = null
    private var liveJob: Job? = null
    
    private lateinit var layoutList: LinearLayout
    private lateinit var layoutDetail: LinearLayout
    private lateinit var eventsContainer: LinearLayout
    private lateinit var participantsContainer: LinearLayout
    private lateinit var tvDetailTitle: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_live_attendance)

        val root = findViewById<View>(R.id.topBar).parent as View
        ViewCompat.setOnApplyWindowInsetsListener(root) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, 0)
            insets
        }

        layoutList = findViewById(R.id.layoutList)
        layoutDetail = findViewById(R.id.layoutDetail)
        eventsContainer = findViewById(R.id.eventsContainer)
        participantsContainer = findViewById(R.id.participantsContainer)
        tvDetailTitle = findViewById(R.id.tvDetailTitle)

        findViewById<View>(R.id.btnBack).setOnClickListener {
            liveJob?.cancel()
            layoutDetail.visibility = View.GONE
            layoutList.visibility = View.VISIBLE
        }

        findViewById<View>(R.id.btnMenu).setOnClickListener {
            // Open sidebar if available, otherwise go back
            val drawer = findViewById<androidx.drawerlayout.widget.DrawerLayout>(R.id.drawerLayout)
            if (drawer != null) {
                drawer.open()
            } else {
                startActivity(Intent(this, OrganizerDashboardActivity::class.java))
                finish()
            }
        }
        
        setupBottomNav()
        loadOngoingEvents()
    }

    private fun setupBottomNav() {
        findViewById<View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }
        findViewById<View>(R.id.navEvents)?.setOnClickListener {
            startActivity(Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<View>(R.id.navParticipants)?.setOnClickListener {
            startActivity(Intent(this, ParticipantsActivity::class.java))
            finish()
        }
    }

    private fun computeStatus(ev: JSONObject): String {
        val now = Date()
        val sdf = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())
        val startDate = ev.optString("start_date", "")
        val startTime = ev.optString("start_time", "00:00").take(5)
        val endDate = ev.optString("end_date", "")
        val endTime = ev.optString("end_time", "23:59").take(5)

        if (startDate.isEmpty()) return "upcoming"
        return try {
            val startDt = sdf.parse("$startDate $startTime") ?: return "upcoming"
            val endDt = if (endDate.isNotEmpty()) sdf.parse("$endDate $endTime") else null

            when {
                now.before(startDt) -> "upcoming"
                endDt != null && now.after(endDt) -> "completed"
                else -> "ongoing"
            }
        } catch (e: Exception) {
            "upcoming"
        }
    }

    private fun loadOngoingEvents() {
        CoroutineScope(Dispatchers.Main).launch {
            eventsContainer.removeAllViews()
            val loadingTv = TextView(this@LiveAttendanceActivity).apply { text = "Loading ongoing events..." }
            eventsContainer.addView(loadingTv)
            
            allEvents = SupabaseApi.fetchOrganizerEvents()
            
            eventsContainer.removeAllViews()
            
            val array = allEvents
            if (array == null || array.length() == 0) {
                val tv = TextView(this@LiveAttendanceActivity).apply { text = "No events to track." }
                eventsContainer.addView(tv)
                return@launch
            }
            
            var hasEvents = false
            for (i in 0 until array.length()) {
                val ev = array.getJSONObject(i)
                val status = computeStatus(ev)
                if (status == "ongoing" || status == "upcoming" || status == "completed") {
                    hasEvents = true
                    val view = createEventCard(ev, status)
                    eventsContainer.addView(view)
                }
            }
            
            if (!hasEvents) {
                val tv = TextView(this@LiveAttendanceActivity).apply { text = "No ongoing events to track." }
                eventsContainer.addView(tv)
            }
        }
    }

    private fun createEventCard(ev: JSONObject, status: String): View {
        val card = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(32, 32, 32, 32)
            setBackgroundColor(Color.WHITE) // assuming this exists
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply { setMargins(0, 0, 0, 32) }
            
            setOnClickListener {
                openLiveDetail(ev)
            }
        }
        
        val titleLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
        }
        
        val title = TextView(this).apply {
            text = ev.optString("title", "Event")
            textSize = 18f
            setTextColor(Color.parseColor("#0f172a"))
        }
        titleLayout.addView(title)
        card.addView(titleLayout)
        
        return card
    }

    private fun openLiveDetail(ev: JSONObject) {
        layoutList.visibility = View.GONE
        layoutDetail.visibility = View.VISIBLE
        tvDetailTitle.text = ev.optString("title", "Event")
        
        val eventId = ev.optString("id")
        
        liveJob?.cancel()
        liveJob = CoroutineScope(Dispatchers.Main).launch {
            participantsContainer.removeAllViews()
            participantsContainer.addView(TextView(this@LiveAttendanceActivity).apply { text = "Loading participants..." })
            
            val regsRes = withContext(Dispatchers.IO) {
                SupabaseApi.get("rest/v1/event_registrations?event_id=eq.$eventId&status=eq.approved&select=id,attendee_id")
            }
            if (regsRes == null) {
                participantsContainer.removeAllViews()
                participantsContainer.addView(TextView(this@LiveAttendanceActivity).apply { text = "Failed to load participants." })
                return@launch
            }
            
            val regs = JSONArray(regsRes)
            if (regs.length() == 0) {
                participantsContainer.removeAllViews()
                participantsContainer.addView(TextView(this@LiveAttendanceActivity).apply { text = "No approved participants to track." })
                return@launch
            }
            
            val uids = mutableListOf<String>()
            for (i in 0 until regs.length()) {
                uids.add("\"${regs.getJSONObject(i).optString("attendee_id")}\"")
            }
            
            val profilesMap = mutableMapOf<String, String>()
            withContext(Dispatchers.IO) {
                try {
                    val pRes = SupabaseApi.get("rest/v1/profiles?id=in.(${uids.joinToString(",")})&select=id,full_name")
                    if (pRes != null) {
                        val arr = JSONArray(pRes)
                        for (i in 0 until arr.length()) {
                            val obj = arr.getJSONObject(i)
                            profilesMap[obj.optString("id")] = obj.optString("full_name")
                        }
                    }
                } catch (e: Exception) {}
            }
            
            while (isActive) {
                val statsView = fetchLiveStats(eventId, regs, ev, profilesMap)
                participantsContainer.removeAllViews()
                participantsContainer.addView(statsView)
                delay(10000)
            }
        }
    }
    
    private suspend fun fetchLiveStats(eventId: String, regs: JSONArray, ev: JSONObject, profiles: Map<String, String>): View {
        return withContext(Dispatchers.IO) {
            val logsRes = SupabaseApi.get("rest/v1/attendance_logs?event_id=eq.$eventId&select=attendee_id,checkpoint_index")
            val cpCounts = mutableMapOf<String, Int>()
            if (logsRes != null) {
                val allLogs = JSONArray(logsRes)
                for (i in 0 until allLogs.length()) {
                    val lg = allLogs.getJSONObject(i)
                    val aId = lg.optString("attendee_id")
                    cpCounts[aId] = (cpCounts[aId] ?: 0) + 1
                }
            }
            
            val totalCp = ev.optInt("checkpoints_count", 4)
            
            val now = Date()
            val sdf = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())
            val startDate = ev.optString("start_date", "")
            val startTime = ev.optString("start_time", "00:00").take(5)
            val endDate = ev.optString("end_date", "")
            val endTime = ev.optString("end_time", "23:59").take(5)
            
            var elapsedSessions = 0
            try {
                if (startDate.isNotEmpty()) {
                    val start = sdf.parse("$startDate $startTime")
                    val end = if (endDate.isNotEmpty()) sdf.parse("$endDate $endTime") else null
                    if (start != null && end != null) {
                        if (now.after(end)) {
                            elapsedSessions = totalCp
                        } else if (now.after(start)) {
                            val dur = end.time - start.time
                            val win = dur / totalCp
                            val elap = now.time - start.time
                            elapsedSessions = (elap / win).toInt()
                        }
                    }
                }
            } catch (e: Exception) {}
            
            withContext(Dispatchers.Main) {
                val parent = LinearLayout(this@LiveAttendanceActivity).apply { orientation = LinearLayout.VERTICAL }
                for (i in 0 until regs.length()) {
                    val r = regs.getJSONObject(i)
                    val aId = r.optString("attendee_id")
                    val name = profiles[aId] ?: "Unknown Participant"
                    val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
                    
                    val attended = cpCounts[aId] ?: 0
                    val missed = maxOf(0, elapsedSessions - attended)
                    val remaining = maxOf(0, totalCp - elapsedSessions)
                    
                    val pct = if (totalCp > 0) Math.round((attended.toFloat() / totalCp) * 100) else 0
                    
                    val v = createParticipantCard(initials, name, attended, missed, remaining, pct)
                    parent.addView(v)
                }
                parent
            }
        }
    }
    
    private fun createParticipantCard(initials: String, name: String, att: Int, miss: Int, rem: Int, pct: Int): View {
        val card = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(32, 32, 32, 32)
            setBackgroundColor(Color.WHITE)
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply { setMargins(0, 0, 0, 16) }
        }
        
        val tvInit = TextView(this).apply {
            text = initials
            textSize = 18f
            setTextColor(Color.parseColor("#0d162a"))
            setPadding(16, 16, 16, 16)
        }
        card.addView(tvInit)
        
        val center = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, -2, 1f)
            setPadding(16, 0, 0, 0)
        }
        val tvName = TextView(this).apply { text = name; textSize = 16f; setTextColor(Color.BLACK); setTypeface(null, android.graphics.Typeface.BOLD) }
        val tvStats = TextView(this).apply { text = "$att Attended  |  $miss Missed  |  $rem Remaining"; textSize = 12f }
        center.addView(tvName)
        center.addView(tvStats)
        card.addView(center)
        
        val tvPct = TextView(this).apply { text = "$pct%"; textSize = 18f; setTextColor(Color.RED); setTypeface(null, android.graphics.Typeface.BOLD) }
        card.addView(tvPct)
        
        return card
    }

    override fun onDestroy() {
        super.onDestroy()
        liveJob?.cancel()
    }
}
