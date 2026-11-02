import os

xml_content = """<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F7F9FC">

    <!-- Top Bar -->
    <LinearLayout
        android:id="@+id/topBar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:background="#FFFFFF"
        android:padding="16dp"
        android:gravity="center_vertical"
        android:elevation="4dp"
        app:layout_constraintTop_toTopOf="parent">

        <ImageButton
            android:id="@+id/btnBack"
            android:layout_width="44dp"
            android:layout_height="44dp"
            android:background="@drawable/bg_outlined_button"
            android:src="@android:drawable/ic_menu_revert"
            app:tint="#0F172A" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Event Details"
            android:textColor="#0F172A"
            android:textSize="18sp"
            android:textStyle="bold"
            android:layout_marginStart="16dp" />
    </LinearLayout>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="0dp"
        app:layout_constraintTop_toBottomOf="@id/topBar"
        app:layout_constraintBottom_toTopOf="@id/bottomBar">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:paddingBottom="40dp">

            <!-- Banner Image -->
            <ImageView
                android:id="@+id/ivBanner"
                android:layout_width="match_parent"
                android:layout_height="250dp"
                android:scaleType="centerCrop"
                android:background="#E2E8F0" />

            <!-- Main Card -->
            <androidx.cardview.widget.CardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginHorizontal="20dp"
                android:layout_marginTop="-30dp"
                app:cardCornerRadius="20dp"
                app:cardElevation="4dp"
                app:cardBackgroundColor="#FFFFFF">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="24dp">

                    <LinearLayout
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:orientation="horizontal"
                        android:layout_marginBottom="16dp">
                        <TextView
                            android:id="@+id/tvTag1"
                            android:layout_width="wrap_content"
                            android:layout_height="wrap_content"
                            android:background="@drawable/bg_primary_button"
                            android:backgroundTint="#F1F5F9"
                            android:textColor="#475569"
                            android:textSize="12sp"
                            android:textStyle="bold"
                            android:paddingHorizontal="12dp"
                            android:paddingVertical="6dp"
                            android:layout_marginEnd="8dp" />
                        <TextView
                            android:id="@+id/tvTag2"
                            android:layout_width="wrap_content"
                            android:layout_height="wrap_content"
                            android:background="@drawable/bg_primary_button"
                            android:backgroundTint="#F1F5F9"
                            android:textColor="#475569"
                            android:textSize="12sp"
                            android:textStyle="bold"
                            android:paddingHorizontal="12dp"
                            android:paddingVertical="6dp" />
                    </LinearLayout>

                    <TextView
                        android:id="@+id/tvTitle"
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content"
                        android:textColor="#0F172A"
                        android:textSize="24sp"
                        android:textStyle="bold"
                        android:layout_marginBottom="8dp" />

                    <TextView
                        android:id="@+id/tvOrg"
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content"
                        android:textColor="#3B35A8"
                        android:textSize="15sp"
                        android:textStyle="bold"
                        android:layout_marginBottom="24dp" />

                    <LinearLayout
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content"
                        android:orientation="vertical">
                        
                        <LinearLayout
                            android:layout_width="match_parent"
                            android:layout_height="wrap_content"
                            android:orientation="horizontal"
                            android:layout_marginBottom="16dp">
                            <TextView
                                android:layout_width="40dp"
                                android:layout_height="40dp"
                                android:background="@drawable/bg_circle"
                                android:backgroundTint="#F8FAFC"
                                android:text="📅"
                                android:gravity="center"
                                android:textSize="20sp" />
                            <LinearLayout
                                android:layout_width="wrap_content"
                                android:layout_height="wrap_content"
                                android:orientation="vertical"
                                android:layout_marginStart="12dp">
                                <TextView
                                    android:layout_width="wrap_content"
                                    android:layout_height="wrap_content"
                                    android:text="Date"
                                    android:textColor="#64748B"
                                    android:textSize="13sp"
                                    android:textStyle="bold" />
                                <TextView
                                    android:id="@+id/tvDate"
                                    android:layout_width="wrap_content"
                                    android:layout_height="wrap_content"
                                    android:textColor="#0F172A"
                                    android:textSize="15sp"
                                    android:textStyle="bold" />
                            </LinearLayout>
                        </LinearLayout>

                        <LinearLayout
                            android:layout_width="match_parent"
                            android:layout_height="wrap_content"
                            android:orientation="horizontal"
                            android:layout_marginBottom="16dp">
                            <TextView
                                android:layout_width="40dp"
                                android:layout_height="40dp"
                                android:background="@drawable/bg_circle"
                                android:backgroundTint="#F8FAFC"
                                android:text="🕒"
                                android:gravity="center"
                                android:textSize="20sp" />
                            <LinearLayout
                                android:layout_width="wrap_content"
                                android:layout_height="wrap_content"
                                android:orientation="vertical"
                                android:layout_marginStart="12dp">
                                <TextView
                                    android:layout_width="wrap_content"
                                    android:layout_height="wrap_content"
                                    android:text="Time"
                                    android:textColor="#64748B"
                                    android:textSize="13sp"
                                    android:textStyle="bold" />
                                <TextView
                                    android:id="@+id/tvTime"
                                    android:layout_width="wrap_content"
                                    android:layout_height="wrap_content"
                                    android:textColor="#0F172A"
                                    android:textSize="15sp"
                                    android:textStyle="bold" />
                            </LinearLayout>
                        </LinearLayout>

                        <LinearLayout
                            android:layout_width="match_parent"
                            android:layout_height="wrap_content"
                            android:orientation="horizontal">
                            <TextView
                                android:layout_width="40dp"
                                android:layout_height="40dp"
                                android:background="@drawable/bg_circle"
                                android:backgroundTint="#F8FAFC"
                                android:text="📍"
                                android:gravity="center"
                                android:textSize="20sp" />
                            <LinearLayout
                                android:layout_width="wrap_content"
                                android:layout_height="wrap_content"
                                android:orientation="vertical"
                                android:layout_marginStart="12dp">
                                <TextView
                                    android:layout_width="wrap_content"
                                    android:layout_height="wrap_content"
                                    android:text="Location"
                                    android:textColor="#64748B"
                                    android:textSize="13sp"
                                    android:textStyle="bold" />
                                <TextView
                                    android:id="@+id/tvLocation"
                                    android:layout_width="wrap_content"
                                    android:layout_height="wrap_content"
                                    android:textColor="#0F172A"
                                    android:textSize="15sp"
                                    android:textStyle="bold" />
                            </LinearLayout>
                        </LinearLayout>
                    </LinearLayout>
                </LinearLayout>
            </androidx.cardview.widget.CardView>

            <TextView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="About this event"
                android:textColor="#0F172A"
                android:textSize="18sp"
                android:textStyle="bold"
                android:layout_marginHorizontal="20dp"
                android:layout_marginTop="32dp"
                android:layout_marginBottom="16dp" />

            <TextView
                android:id="@+id/tvDescription"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:textColor="#475569"
                android:textSize="15sp"
                android:layout_marginHorizontal="20dp"
                android:lineSpacingExtra="4dp" />
                
        </LinearLayout>
    </ScrollView>

    <!-- Bottom Bar -->
    <LinearLayout
        android:id="@+id/bottomBar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="#FFFFFF"
        android:padding="16dp"
        android:elevation="8dp"
        app:layout_constraintBottom_toBottomOf="parent">

        <Button
            android:id="@+id/btnAction"
            android:layout_width="match_parent"
            android:layout_height="56dp"
            android:text="Register Now"
            android:textAllCaps="false"
            android:textSize="16sp"
            android:textStyle="bold"
            android:textColor="#FFFFFF"
            android:backgroundTint="#5B54E3"
            app:cornerRadius="12dp" />
    </LinearLayout>

</androidx.constraintlayout.widget.ConstraintLayout>
"""

kt_content = """package com.simats.zyntrapass

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
            if (isRegistered) {
                btnAction.isEnabled = false
                btnAction.text = "Approved & Registered"
                btnAction.setBackgroundColor(Color.parseColor("#E2E8F0"))
                btnAction.setTextColor(Color.parseColor("#64748B"))
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
"""

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_event_detail.xml', 'w', encoding='utf-8') as f:
    f.write(xml_content)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/EventDetailActivity.kt', 'w', encoding='utf-8') as f:
    f.write(kt_content)

print("Created EventDetailActivity")
