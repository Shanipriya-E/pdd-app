package com.simats.zyntrapass

import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.Color
import android.os.Bundle
import android.view.View
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
import java.text.SimpleDateFormat
import java.util.Locale

class VolunteersActivity : AppCompatActivity() {

    private var allRequests = JSONArray()
    private val profilesMap = mutableMapOf<String, JSONObject>()
    private val eventsMap = mutableMapOf<String, String>()
    private var currentTab = "pending"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_volunteers)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainVolunteers)) { v, insets ->
            val sb = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(sb.left, sb.top, sb.right, 0)
            insets
        }

        // Avatar
        val name = SupabaseApi.currentUserName ?: "User"
        val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
        findViewById<TextView>(R.id.tvUserAvatar).text = initials

        // Set emojis safely from Kotlin
        findViewById<TextView>(R.id.iconPending)?.text = "🤝"
        findViewById<TextView>(R.id.iconApproved)?.text = "✅"
        findViewById<TextView>(R.id.iconRejected)?.text = "❌"

        setupTabs()
        setupBottomNav()
        loadData()
    }

    private fun setupTabs() {
        val tabRequests = findViewById<LinearLayout>(R.id.tabRequests)
        val tabApproved = findViewById<LinearLayout>(R.id.tabApproved)
        val tabRejected = findViewById<LinearLayout>(R.id.tabRejected)
        
        tabRequests.setOnClickListener { switchTab("pending") }
        tabApproved.setOnClickListener { switchTab("approved") }
        tabRejected.setOnClickListener { switchTab("rejected") }
    }

    private fun switchTab(tab: String) {
        currentTab = tab
        
        // Reset all tabs to inactive
        val tabRequests = findViewById<LinearLayout>(R.id.tabRequests)
        val tabApproved = findViewById<LinearLayout>(R.id.tabApproved)
        val tabRejected = findViewById<LinearLayout>(R.id.tabRejected)
        
        listOf(tabRequests, tabApproved, tabRejected).forEach {
            it.setBackgroundResource(0)
            val tv = it.getChildAt(0) as TextView
            tv.setTextColor(Color.parseColor("#475569"))
            val badge = it.getChildAt(1) as TextView
            badge.backgroundTintList = ColorStateList.valueOf(Color.parseColor("#F1F5F9"))
            badge.setTextColor(Color.parseColor("#334155"))
        }

        // Set active tab
        val activeLayout = when (tab) {
            "pending" -> tabRequests
            "approved" -> tabApproved
            else -> tabRejected
        }
        
        activeLayout.setBackgroundResource(R.drawable.bg_tab_indicator)
        val activeTv = activeLayout.getChildAt(0) as TextView
        activeTv.setTextColor(Color.parseColor("#3B35A8"))
        val activeBadge = activeLayout.getChildAt(1) as TextView
        activeBadge.backgroundTintList = ColorStateList.valueOf(Color.parseColor("#EEF2FF"))
        activeBadge.setTextColor(Color.parseColor("#3B35A8"))

        renderList()
    }

    private fun setupBottomNav() {
        findViewById<View>(R.id.navDashboard).setOnClickListener {
            startActivity(Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }
        findViewById<View>(R.id.navEvents).setOnClickListener {
            startActivity(Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<View>(R.id.navParticipants).setOnClickListener {
            startActivity(Intent(this, ParticipantsActivity::class.java))
            finish()
        }
    }

    private fun loadData() {
        val orgId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            val requests = SupabaseApi.fetchVolunteerRequests(orgId) ?: JSONArray()
            allRequests = requests
            
            val userIds = mutableSetOf<String>()
            val eventIds = mutableSetOf<String>()
            
            for (i in 0 until requests.length()) {
                val r = requests.getJSONObject(i)
                userIds.add(r.optString("volunteer_id"))
                eventIds.add(r.optString("event_id"))
            }

            if (userIds.isNotEmpty()) {
                val profiles = SupabaseApi.fetchProfilesByIds(userIds.toList()) ?: JSONArray()
                for (i in 0 until profiles.length()) {
                    val p = profiles.getJSONObject(i)
                    profilesMap[p.optString("id")] = p
                }
            }

            if (eventIds.isNotEmpty()) {
                val events = SupabaseApi.fetchEventsByIds(eventIds.toList()) ?: JSONArray()
                for (i in 0 until events.length()) {
                    val e = events.getJSONObject(i)
                    eventsMap[e.optString("id")] = e.optString("title")
                }
            }
            
            updateStats()
            renderList()
        }
    }

    private fun updateStats() {
        var pendingCount = 0
        var approvedCount = 0
        var rejectedCount = 0

        for (i in 0 until allRequests.length()) {
            val status = allRequests.getJSONObject(i).optString("status")
            when (status) {
                "pending" -> pendingCount++
                "approved" -> approvedCount++
                "rejected" -> rejectedCount++
            }
        }

        findViewById<TextView>(R.id.tvStatPending).text = pendingCount.toString()
        findViewById<TextView>(R.id.tvStatApproved).text = approvedCount.toString()
        findViewById<TextView>(R.id.tvStatRejected).text = rejectedCount.toString()
        
        findViewById<TextView>(R.id.badgeRequests).text = pendingCount.toString()
        findViewById<TextView>(R.id.badgeApproved).text = approvedCount.toString()
        findViewById<TextView>(R.id.badgeRejected).text = rejectedCount.toString()
    }

    private fun renderList() {
        val feed = findViewById<LinearLayout>(R.id.llVolunteerFeed)
        feed.removeAllViews()

        val filtered = mutableListOf<JSONObject>()
        for (i in 0 until allRequests.length()) {
            val r = allRequests.getJSONObject(i)
            if (r.optString("status") == currentTab) {
                filtered.add(r)
            }
        }

        if (filtered.isEmpty()) {
            val emptyMsg = when (currentTab) {
                "pending" -> "No pending requests\nVolunteer requests from students appear here for review."
                "approved" -> "No approved volunteers\nVolunteers you accept will be listed here."
                else -> "No rejected volunteers\nVolunteer requests from students appear here for review."
            }
            feed.addView(makeEmptyView(emptyMsg))
            return
        }

        val sdfIn = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        val sdfOut = SimpleDateFormat("dd MMM yyyy", Locale.getDefault())

        for (req in filtered) {
            val cardView = layoutInflater.inflate(R.layout.item_volunteer_card, feed, false)
            
            val reqId = req.optString("id")
            val profile = profilesMap[req.optString("volunteer_id")] ?: JSONObject()
            val name = profile.optString("full_name", "Unknown User")
            val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
            
            cardView.findViewById<TextView>(R.id.tvVolAvatar).apply {
                text = initials
                when (currentTab) {
                    "pending" -> {
                        backgroundTintList = ColorStateList.valueOf(Color.parseColor("#CCFBF1"))
                        setTextColor(Color.parseColor("#0F766E"))
                    }
                    "approved" -> {
                        backgroundTintList = ColorStateList.valueOf(Color.parseColor("#E0E7FF"))
                        setTextColor(Color.parseColor("#5B54E3"))
                    }
                    "rejected" -> {
                        backgroundTintList = ColorStateList.valueOf(Color.parseColor("#F1F5F9"))
                        setTextColor(Color.parseColor("#64748B"))
                    }
                }
            }
            
            cardView.findViewById<TextView>(R.id.tvVolName).text = name
            
            cardView.findViewById<TextView>(R.id.tvVolStatus).apply {
                text = currentTab
                when (currentTab) {
                    "pending" -> {
                        backgroundTintList = ColorStateList.valueOf(Color.parseColor("#FFFBEB"))
                        setTextColor(Color.parseColor("#D97706"))
                    }
                    "approved" -> {
                        backgroundTintList = ColorStateList.valueOf(Color.parseColor("#DCFCE7"))
                        setTextColor(Color.parseColor("#16A34A"))
                    }
                    "rejected" -> {
                        backgroundTintList = ColorStateList.valueOf(Color.parseColor("#FEE2E2"))
                        setTextColor(Color.parseColor("#DC2626"))
                    }
                }
            }

            cardView.findViewById<TextView>(R.id.tvVolInstitution).text = profile.optString("institution", "Institution")
            
            val email = profile.optString("email")
            val tvEmail = cardView.findViewById<TextView>(R.id.tvVolEmail)
            if (email.isNotEmpty()) {
                tvEmail.text = "📧 $email"
                tvEmail.visibility = View.VISIBLE
            } else {
                tvEmail.visibility = View.GONE
            }

            val phone = req.optString("phone")
            val tvPhone = cardView.findViewById<TextView>(R.id.tvVolPhone)
            if (phone.isNotEmpty()) {
                tvPhone.text = "📞 $phone"
                tvPhone.visibility = View.VISIBLE
            } else {
                tvPhone.visibility = View.GONE
            }

            cardView.findViewById<TextView>(R.id.tvVolEvent).text = eventsMap[req.optString("event_id")] ?: "Unknown Event"
            
            val dateStr = req.optString("created_at")
            var formattedDate = dateStr
            try {
                if (dateStr.isNotEmpty()) {
                    val d = sdfIn.parse(dateStr.split(".")[0])
                    if (d != null) formattedDate = sdfOut.format(d)
                }
            } catch (e: Exception) {}
            cardView.findViewById<TextView>(R.id.tvVolDate).text = formattedDate

            val msg = req.optString("message")
            val tvMsg = cardView.findViewById<TextView>(R.id.tvVolMessage)
            if (msg.isNotEmpty()) {
                tvMsg.text = "\"$msg\""
                tvMsg.visibility = View.VISIBLE
            } else {
                tvMsg.visibility = View.GONE
            }

            val llActions = cardView.findViewById<LinearLayout>(R.id.llVolActions)
            val tvStatusMsg = cardView.findViewById<TextView>(R.id.tvVolStatusMsg)
            
            if (currentTab == "pending") {
                llActions.visibility = View.VISIBLE
                tvStatusMsg.visibility = View.GONE
                
                val btnAccept = cardView.findViewById<Button>(R.id.btnAcceptVol)
                val btnReject = cardView.findViewById<Button>(R.id.btnRejectVol)
                
                btnAccept.setOnClickListener { handleAction(reqId, "approved", btnAccept, btnReject) }
                btnReject.setOnClickListener { handleAction(reqId, "rejected", btnAccept, btnReject) }
            } else {
                llActions.visibility = View.GONE
                tvStatusMsg.visibility = View.VISIBLE
                if (currentTab == "approved") {
                    tvStatusMsg.text = "Scanning access is active for this volunteer."
                    tvStatusMsg.setTextColor(Color.parseColor("#5B54E3"))
                } else {
                    tvStatusMsg.text = "Request was rejected."
                    tvStatusMsg.setTextColor(Color.parseColor("#64748B"))
                }
            }

            feed.addView(cardView)
        }
    }

    private fun handleAction(reqId: String, newStatus: String, btnAccept: Button, btnReject: Button) {
        btnAccept.isEnabled = false
        btnReject.isEnabled = false
        
        if (newStatus == "approved") btnAccept.text = "⏳" else btnReject.text = "⏳"

        CoroutineScope(Dispatchers.Main).launch {
            val success = SupabaseApi.updateVolunteerStatus(reqId, newStatus)
            if (success) {
                // Update local state
                for (i in 0 until allRequests.length()) {
                    val r = allRequests.getJSONObject(i)
                    if (r.optString("id") == reqId) {
                        r.put("status", newStatus)
                        break
                    }
                }
                updateStats()
                renderList() // Re-render to remove from current tab
            } else {
                Toast.makeText(this@VolunteersActivity, "Failed to update status", Toast.LENGTH_SHORT).show()
                btnAccept.isEnabled = true
                btnReject.isEnabled = true
                btnAccept.text = "Accept"
                btnReject.text = "Reject"
            }
        }
    }

    private fun makeEmptyView(msg: String) = TextView(this).apply {
        text = msg
        textSize = 14f
        gravity = android.view.Gravity.CENTER
        setTextColor(Color.parseColor("#64748B"))
        setPadding(0, 80, 0, 0)
    }
}
