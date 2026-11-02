import os

app_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main"
java_dir = os.path.join(app_dir, r"java\com\simats\zyntrapass")
res_dir = os.path.join(app_dir, r"res\layout")

xml_dash = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#f7f9fc">
    
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:background="@android:color/white"
        android:elevation="4dp"
        android:padding="16dp">

        <TextView
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="wrap_content"
            android:text="Volunteer Dashboard"
            android:textSize="20sp"
            android:textStyle="bold"
            android:textColor="#0d162a"
            android:layout_gravity="center_vertical"/>
            
        <TextView
            android:id="@+id/btnLogout"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Logout &#128682;"
            android:textColor="#ef4444"
            android:textStyle="bold"
            android:layout_gravity="center_vertical"
            android:padding="8dp"/>
    </LinearLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="24dp">
        
        <TextView android:id="@+id/tvEventName" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Loading Event..." android:textSize="22sp" android:textStyle="bold" android:textColor="#0d162a" android:layout_marginBottom="8dp" />
        <TextView android:id="@+id/tvEventDate" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Date/Time" android:textSize="16sp" android:textColor="#64748b" android:layout_marginBottom="8dp" />
        <TextView android:id="@+id/tvEventVenue" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Venue" android:textSize="16sp" android:textColor="#64748b" android:layout_marginBottom="32dp" />

        <Button
            android:id="@+id/btnScan"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:text="Scan QR"
            android:backgroundTint="#5b54e3"
            android:layout_marginBottom="16dp"/>
            
        <Button
            android:id="@+id/btnParticipants"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:text="Participants"
            android:backgroundTint="#e2e8f0"
            android:textColor="#0d162a"/>
    </LinearLayout>
</LinearLayout>
'''

kt_dash = '''package com.simats.zyntrapass

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray

class VolunteerDashboardActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_volunteer_dashboard)
        
        findViewById<TextView>(R.id.btnLogout).setOnClickListener {
            getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).edit().clear().apply()
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }
        
        findViewById<Button>(R.id.btnScan).setOnClickListener {
            startActivity(Intent(this, VolunteerScanActivity::class.java))
        }
        
        findViewById<Button>(R.id.btnParticipants).setOnClickListener {
            startActivity(Intent(this, VolunteerParticipantsActivity::class.java))
        }
        
        loadEventDetails()
    }
    
    private fun loadEventDetails() {
        val prefs = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE)
        val eventId = prefs.getString("event_id", "") ?: ""
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val res = SupabaseApi.get("rest/v1/events?id=eq.$eventId&select=title,start_date,start_time,venue")
                if (res != null) {
                    val array = JSONArray(res)
                    if (array.length() > 0) {
                        val obj = array.getJSONObject(0)
                        withContext(Dispatchers.Main) {
                            findViewById<TextView>(R.id.tvEventName).text = obj.optString("title", "Event")
                            findViewById<TextView>(R.id.tvEventDate).text = "${obj.optString("start_date", "")} | ${obj.optString("start_time", "")}"
                            findViewById<TextView>(R.id.tvEventVenue).text = obj.optString("venue", "TBA")
                        }
                    }
                }
            } catch (e: Exception) {}
        }
    }
}
'''

with open(os.path.join(res_dir, 'activity_volunteer_dashboard.xml'), 'w', encoding='utf-8') as f: f.write(xml_dash)
with open(os.path.join(java_dir, 'VolunteerDashboardActivity.kt'), 'w', encoding='utf-8') as f: f.write(kt_dash)

print("Generated VolunteerDashboardActivity")
