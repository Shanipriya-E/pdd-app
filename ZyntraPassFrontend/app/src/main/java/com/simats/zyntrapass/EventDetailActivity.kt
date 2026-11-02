package com.simats.zyntrapass

import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject

class EventDetailActivity : AppCompatActivity() {

    private lateinit var eventId: String
    private var isRegistered = false
    private var orgId = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_event_detail)

        eventId = intent.getStringExtra("eventId") ?: return finish()
        isRegistered = intent.getBooleanExtra("isRegistered", false)

        findViewById<ImageButton>(R.id.btnBack).setOnClickListener { finish() }

        loadEventDetails()
    }

    private fun loadEventDetails() {
        CoroutineScope(Dispatchers.Main).launch {
            val ev = SupabaseApi.fetchEventById(eventId) ?: return@launch
            
            orgId = ev.optString("organizer_id")
            
            val orgProfiles = SupabaseApi.fetchProfilesByIds(listOf(orgId))
            val orgName = if (orgProfiles != null && orgProfiles.length() > 0) {
                val p = orgProfiles.getJSONObject(0)
                p.optString("institution").takeIf { it.isNotBlank() } ?: p.optString("full_name")
            } else {
                "Unknown Organizer"
            }

            findViewById<TextView>(R.id.tvTitle).text = ev.optString("title", "Untitled Event")
            findViewById<TextView>(R.id.tvOrg).text = "By $orgName"
            
            findViewById<TextView>(R.id.tvTag1).text = ev.optString("category", "General")
            findViewById<TextView>(R.id.tvTag2).text = ev.optString("type", "Event")
            
            val dateStr = ev.optString("date", "Unknown").take(10)
            findViewById<TextView>(R.id.tvDate).text = dateStr
            
            val sd = ev.optString("start_date", "").take(10)
            val ed = ev.optString("end_date", "").take(10)
            val st = ev.optString("start_time", "").take(8)
            val et = ev.optString("end_time", "").take(8)
            findViewById<TextView>(R.id.tvTime).text = "$st - $et"
            
            findViewById<TextView>(R.id.tvLocation).text = ev.optString("venue_name", "Online")
            findViewById<TextView>(R.id.tvDescription).text = ev.optString("description", "No description available.")

            // Load banner with Glide. Fallback to an aesthetic Unsplash image if null/empty
            val bannerUrl = ev.optString("banner_image_url")
            val ivBanner = findViewById<ImageView>(R.id.ivBanner)
            if (bannerUrl.isNotEmpty() && bannerUrl != "null") {
                Glide.with(this@EventDetailActivity).load(bannerUrl).into(ivBanner)
            } else {
                // Default image
                Glide.with(this@EventDetailActivity).load("https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800").into(ivBanner)
            }

            val btnAction = findViewById<Button>(R.id.btnAction)
            
            val currentUserId = SupabaseApi.currentUserId
            var volRecord: org.json.JSONObject? = null
            if (currentUserId != null) {
                val vols = SupabaseApi.fetchMyVolunteerRequests(currentUserId)
                if (vols != null) {
                    for (i in 0 until vols.length()) {
                        val v = vols.getJSONObject(i)
                        if (v.optString("event_id") == eventId) {
                            volRecord = v
                            break
                        }
                    }
                }
            }
            
            if (isRegistered) {
                btnAction.isEnabled = false
                btnAction.text = "Approved & Registered"
                btnAction.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnAction.setTextColor(Color.parseColor("#64748B"))
            } else if (volRecord != null) {
                val status = volRecord.optString("status")
                val code = volRecord.optString("secret_code")
                btnAction.isEnabled = false
                btnAction.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnAction.setTextColor(Color.parseColor("#64748B"))
                
                if (status == "approved") {
                    btnAction.text = "Volunteer Code: $code"
                    btnAction.setTextColor(Color.parseColor("#10B981"))
                } else {
                    btnAction.text = "Volunteer Pending"
                }
            } else {
                btnAction.setOnClickListener {
                    val options = arrayOf("As Attendee", "As Volunteer")
                    androidx.appcompat.app.AlertDialog.Builder(this@EventDetailActivity)
                        .setTitle("Register for Event")
                        .setItems(options) { _, which ->
                            handleRegister(which == 1)
                        }
                        .setNegativeButton("Cancel", null)
                        .show()
                }
            }
        }
    }

    private fun handleRegister(isVolunteer: Boolean) {
        val currentUserId = SupabaseApi.currentUserId ?: return
        val btnAction = findViewById<Button>(R.id.btnAction)
        btnAction.isEnabled = false
        btnAction.text = "Registering..."
        
        CoroutineScope(Dispatchers.Main).launch {
            val success = if (isVolunteer) {
                SupabaseApi.registerAsVolunteer(eventId, orgId, currentUserId)
            } else {
                SupabaseApi.registerForEvent(eventId, currentUserId)
            }
            
            if (success) {
                Toast.makeText(this@EventDetailActivity, if (isVolunteer) "Volunteer request sent!" else "Registered!", Toast.LENGTH_SHORT).show()
                btnAction.text = "Approved & Registered"
                btnAction.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnAction.setTextColor(Color.parseColor("#64748B"))
            } else {
                Toast.makeText(this@EventDetailActivity, "Registration failed", Toast.LENGTH_SHORT).show()
                btnAction.isEnabled = true
                btnAction.text = "Register Now"
            }
        }
    }
}
