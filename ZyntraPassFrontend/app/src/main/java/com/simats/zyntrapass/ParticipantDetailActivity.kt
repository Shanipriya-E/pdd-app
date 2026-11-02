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

class ParticipantDetailActivity : AppCompatActivity() {

    // Live summary counters
    private var sumTotal   = 0
    private var sumPending = 0
    private var sumApproved = 0
    private var sumRejected = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_participant_detail)
        setupBottomNav()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainParticipantDetail)) { v, insets ->
            val sb = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(sb.left, sb.top, sb.right, 0)
            insets
        }

        val eventId    = intent.getStringExtra("event_id") ?: run { finish(); return }
        val eventTitle = intent.getStringExtra("event_title") ?: "Event"

        // Avatar
        val name = SupabaseApi.currentUserName ?: "User"
        val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
        findViewById<TextView>(R.id.tvUserAvatar).text = initials

        // Top bar heading
        findViewById<TextView>(R.id.tvTopTitle).text = eventTitle
        findViewById<TextView>(R.id.tvEventName).text = eventTitle

        // Back button
        findViewById<View>(R.id.btnBack).setOnClickListener { finish() }

        // Bottom nav
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

        loadParticipants(eventId)
    }

    private fun loadParticipants(eventId: String) {
        val list = findViewById<LinearLayout>(R.id.llParticipantsList)
        CoroutineScope(Dispatchers.Main).launch {
            // Fetch registrations
            val regs = SupabaseApi.fetchEventRegistrations(eventId)

            list.removeAllViews()

            if (regs == null || regs.length() == 0) {
                list.addView(makeEmptyView("No join requests yet for this event."))
                updateSummaryUI(0, 0, 0, 0)
                return@launch
            }

            // Collect user IDs and fetch profiles
            val userIds = (0 until regs.length()).map { regs.getJSONObject(it).optString("attendee_id") }
            val profiles = SupabaseApi.fetchProfilesByIds(userIds) ?: JSONArray()

            // Build profile map
            val profileMap = mutableMapOf<String, JSONObject>()
            for (i in 0 until profiles.length()) {
                val p = profiles.getJSONObject(i)
                profileMap[p.optString("id")] = p
            }

            // Calculate initial summary
            sumTotal = regs.length()
            sumPending  = 0; sumApproved = 0; sumRejected = 0
            for (i in 0 until regs.length()) {
                when (regs.getJSONObject(i).optString("status")) {
                    "registered" -> sumPending++
                    "approved"   -> sumApproved++
                    "rejected"   -> sumRejected++
                }
            }
            updateSummaryUI(sumTotal, sumPending, sumApproved, sumRejected)
            findViewById<TextView>(R.id.tvEventSub).text = "Participant requests · $sumTotal total"

            // Render participant cards
            for (i in 0 until regs.length()) {
                val reg     = regs.getJSONObject(i)
                val regId   = reg.optString("id")
                val userId  = reg.optString("attendee_id")
                val status  = reg.optString("status", "registered")
                val profile = profileMap[userId] ?: JSONObject()

                val fullName = profile.optString("full_name", "Unknown User").let {
                    if (it.isBlank()) "Unknown User" else it
                }
                val sub = listOfNotNull(
                    profile.optString("institution").takeIf { it.isNotBlank() },
                    profile.optString("area_city").takeIf { it.isNotBlank() }
                ).joinToString(" · ").ifBlank {
                    profile.optString("email").takeIf { it.isNotBlank() } ?: ""
                }

                val initials = fullName.split(" ")
                    .mapNotNull { it.firstOrNull()?.uppercase() }
                    .joinToString("").take(2)

                val cardView = layoutInflater.inflate(R.layout.item_participant_card, list, false)
                cardView.findViewById<TextView>(R.id.tvParticipantAvatar).text = initials
                cardView.findViewById<TextView>(R.id.tvParticipantName).text = fullName
                cardView.findViewById<TextView>(R.id.tvParticipantSub).text = sub

                val chip      = cardView.findViewById<TextView>(R.id.tvStatusChip)
                
                applyStatusChip(chip, status)

                val isPending  = status == "registered"

                // Add click listener for bottom sheet modal
                cardView.setOnClickListener {
                    showParticipantModal(regId, status, profile, chip, isPending)
                }

                list.addView(cardView)
            }
        }
    }

    private fun showParticipantModal(
        regId: String,
        currentStatus: String,
        profile: JSONObject,
        chip: TextView,
        wasPending: Boolean
    ) {
        val bottomSheetDialog = com.google.android.material.bottomsheet.BottomSheetDialog(this)
        val view = layoutInflater.inflate(R.layout.dialog_participant_detail, null)
        bottomSheetDialog.setContentView(view)

        val fullName = profile.optString("full_name", "Unknown User").let { if (it.isBlank()) "Unknown User" else it }
        val initials = fullName.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
        
        view.findViewById<TextView>(R.id.dpAvatar).text = initials
        view.findViewById<TextView>(R.id.dpName).text = fullName
        view.findViewById<TextView>(R.id.dpEmail).text = profile.optString("email").takeIf { it.isNotBlank() } ?: "No email provided"
        view.findViewById<TextView>(R.id.dpInstitution).text = profile.optString("institution").takeIf { it.isNotBlank() } ?: "-"
        view.findViewById<TextView>(R.id.dpArea).text = profile.optString("area_city").takeIf { it.isNotBlank() } ?: "-"
        view.findViewById<TextView>(R.id.dpRole).text = profile.optString("role").takeIf { it.isNotBlank() } ?: "-"

        val statusMap = mapOf("registered" to "Pending", "approved" to "Approved", "rejected" to "Rejected", "attended" to "Attended")
        view.findViewById<TextView>(R.id.dpStatus).text = statusMap[currentStatus] ?: currentStatus

        val isApproved = currentStatus == "approved" || currentStatus == "attended"
        val isRejected = currentStatus == "rejected"

        val btnAccept = view.findViewById<Button>(R.id.dpBtnAccept)
        val btnReject = view.findViewById<Button>(R.id.dpBtnReject)

        btnAccept.isEnabled = !isApproved
        btnAccept.alpha = if (!isApproved) 1f else 0.4f
        btnReject.isEnabled = !isRejected && !isApproved
        btnReject.alpha = if (!isRejected && !isApproved) 1f else 0.4f

        btnAccept.setOnClickListener {
            handleActionModal(regId, "approved", chip, wasPending, bottomSheetDialog)
        }
        btnReject.setOnClickListener {
            handleActionModal(regId, "rejected", chip, wasPending, bottomSheetDialog)
        }

        bottomSheetDialog.show()
    }

    private fun handleActionModal(
        regId: String,
        newStatus: String,
        chip: TextView,
        wasPending: Boolean,
        dialog: com.google.android.material.bottomsheet.BottomSheetDialog
    ) {
        applyStatusChip(chip, newStatus)
        if (wasPending) sumPending = maxOf(0, sumPending - 1)
        if (newStatus == "approved") sumApproved++
        else if (newStatus == "rejected") sumRejected++
        updateSummaryUI(sumTotal, sumPending, sumApproved, sumRejected)

        CoroutineScope(Dispatchers.Main).launch {
            val success = SupabaseApi.updateRegistrationStatus(regId, newStatus)
            if (!success) {
                Toast.makeText(this@ParticipantDetailActivity, "Failed to update status.", Toast.LENGTH_SHORT).show()
            }
        }
        dialog.dismiss()
    }


    private fun applyStatusChip(chip: TextView, status: String) {
        val (label, bg, fg) = when (status) {
            "registered" -> Triple("Pending",  "#FFF4E5", "#D97706")
            "approved"   -> Triple("Accepted", "#DCFCE7", "#16A34A")
            "rejected"   -> Triple("Rejected", "#FEE2E2", "#DC2626")
            "attended"   -> Triple("Attended", "#E0E7FF", "#5B54E3")
            else         -> Triple(status,      "#F1F5F9", "#475569")
        }
        chip.text = label
        chip.setTextColor(Color.parseColor(fg))
        chip.backgroundTintList = ColorStateList.valueOf(Color.parseColor(bg))
    }

    private fun updateSummaryUI(total: Int, pending: Int, approved: Int, rejected: Int) {
        findViewById<TextView>(R.id.tvSumTotal).text    = total.toString()
        findViewById<TextView>(R.id.tvSumPending).text  = pending.toString()
        findViewById<TextView>(R.id.tvSumApproved).text = approved.toString()
        findViewById<TextView>(R.id.tvSumRejected).text = rejected.toString()
    }

    private fun makeEmptyView(msg: String) = TextView(this).apply {
        text = msg
        textSize = 14f
        gravity = android.view.Gravity.CENTER
        setTextColor(Color.parseColor("#64748B"))
        setPadding(0, 60, 0, 0)
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