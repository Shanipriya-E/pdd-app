import os

app_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main"
java_dir = os.path.join(app_dir, r"java\com\simats\zyntrapass")
res_dir = os.path.join(app_dir, r"res\layout")

# VolunteerParticipantsActivity
xml_participants = '''<?xml version="1.0" encoding="utf-8"?>
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

        <Button
            android:id="@+id/btnBack"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Back"
            android:backgroundTint="#e2e8f0"
            android:textColor="#0d162a"/>

        <TextView
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="wrap_content"
            android:text="Participants Stats"
            android:textSize="20sp"
            android:textStyle="bold"
            android:textColor="#0d162a"
            android:layout_marginStart="16dp"
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
        
        <TextView android:id="@+id/tvTotal" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Registered: 0" android:textSize="18sp" android:padding="16dp" android:background="#ffffff" android:layout_marginBottom="12dp" />
        <TextView android:id="@+id/tvApproved" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Approved: 0" android:textSize="18sp" android:padding="16dp" android:background="#ffffff" android:layout_marginBottom="12dp" />
        <TextView android:id="@+id/tvPending" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Pending: 0" android:textSize="18sp" android:padding="16dp" android:background="#ffffff" android:layout_marginBottom="12dp" />
        <TextView android:id="@+id/tvRejected" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Rejected: 0" android:textSize="18sp" android:padding="16dp" android:background="#ffffff" />
    </LinearLayout>
</LinearLayout>
'''

kt_participants = '''package com.simats.zyntrapass

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
import org.json.JSONObject

class VolunteerParticipantsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_volunteer_participants)
        
        findViewById<Button>(R.id.btnBack).setOnClickListener { finish() }
        findViewById<TextView>(R.id.btnLogout).setOnClickListener {
            getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).edit().clear().apply()
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }
        
        loadStats()
    }
    
    private fun loadStats() {
        val prefs = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE)
        val eventId = prefs.getString("event_id", "") ?: ""
        val code = prefs.getString("volunteer_code", "") ?: ""
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Fetch stats directly via query
                val res = SupabaseApi.get("rest/v1/event_registrations?event_id=eq.$eventId&select=status")
                if (res != null) {
                    val array = JSONArray(res)
                    var approved = 0
                    var pending = 0
                    var rejected = 0
                    for (i in 0 until array.length()) {
                        val status = array.getJSONObject(i).optString("status", "")
                        when(status) {
                            "approved" -> approved++
                            "pending" -> pending++
                            "rejected" -> rejected++
                        }
                    }
                    val total = array.length()
                    
                    withContext(Dispatchers.Main) {
                        findViewById<TextView>(R.id.tvTotal).text = "Registered: $total"
                        findViewById<TextView>(R.id.tvApproved).text = "Approved: $approved"
                        findViewById<TextView>(R.id.tvPending).text = "Pending: $pending"
                        findViewById<TextView>(R.id.tvRejected).text = "Rejected: $rejected"
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) { Toast.makeText(this@VolunteerParticipantsActivity, "Error loading stats", Toast.LENGTH_SHORT).show() }
            }
        }
    }
}
'''

with open(os.path.join(res_dir, 'activity_volunteer_participants.xml'), 'w', encoding='utf-8') as f: f.write(xml_participants)
with open(os.path.join(java_dir, 'VolunteerParticipantsActivity.kt'), 'w', encoding='utf-8') as f: f.write(kt_participants)

# VolunteerScanActivity
xml_scan = '''<?xml version="1.0" encoding="utf-8"?>
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

        <Button
            android:id="@+id/btnBack"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Back"
            android:backgroundTint="#e2e8f0"
            android:textColor="#0d162a"/>

        <TextView
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="wrap_content"
            android:text="Scan QR"
            android:textSize="20sp"
            android:textStyle="bold"
            android:textColor="#0d162a"
            android:layout_marginStart="16dp"
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

    <com.journeyapps.barcodescanner.DecoratedBarcodeView
        android:id="@+id/barcodeScannerView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"/>
</LinearLayout>
'''

kt_scan = '''package com.simats.zyntrapass

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.journeyapps.barcodescanner.DecoratedBarcodeView
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject

class VolunteerScanActivity : AppCompatActivity() {

    private lateinit var barcodeView: DecoratedBarcodeView
    private var isProcessing = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_volunteer_scan)
        
        findViewById<Button>(R.id.btnBack).setOnClickListener { finish() }
        findViewById<TextView>(R.id.btnLogout).setOnClickListener {
            getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).edit().clear().apply()
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }
        
        barcodeView = findViewById(R.id.barcodeScannerView)
        barcodeView.setStatusText("Scan QR Code to verify attendance")
        
        barcodeView.decodeContinuous { result ->
            if (!isProcessing) {
                val text = result.text
                if (!text.isNullOrEmpty()) {
                    isProcessing = true
                    barcodeView.pause()
                    handleScanResult(text)
                }
            }
        }
    }
    
    override fun onResume() {
        super.onResume()
        barcodeView.resume()
        isProcessing = false
    }

    override fun onPause() {
        super.onPause()
        barcodeView.pause()
    }
    
    private fun handleScanResult(jsonString: String) {
        val prefs = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE)
        val eventId = prefs.getString("event_id", "") ?: ""
        val code = prefs.getString("volunteer_code", "") ?: ""
        
        try {
            val obj = JSONObject(jsonString)
            val scannedEventId = obj.optString("event_id", "")
            val attendeeId = obj.optString("attendee_id", "")
            
            if (scannedEventId != eventId) {
                Toast.makeText(this, "Error: Ticket is for a different event!", Toast.LENGTH_LONG).show()
                resumeScanning()
                return
            }
            
            // Mark attendance via RPC
            CoroutineScope(Dispatchers.IO).launch {
                try {
                    val payload = JSONObject()
                    payload.put("v_code", code)
                    payload.put("e_id", eventId)
                    payload.put("a_id", attendeeId)
                    
                    val res = SupabaseApi.postRpc("volunteer_scan_qr", payload)
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@VolunteerScanActivity, "Scan successful!", Toast.LENGTH_LONG).show()
                        resumeScanning()
                    }
                } catch(e: Exception) {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@VolunteerScanActivity, "Scan failed or already verified.", Toast.LENGTH_LONG).show()
                        resumeScanning()
                    }
                }
            }
        } catch (e: Exception) {
            Toast.makeText(this, "Invalid QR Format", Toast.LENGTH_SHORT).show()
            resumeScanning()
        }
    }
    
    private fun resumeScanning() {
        barcodeView.postDelayed({
            isProcessing = false
            barcodeView.resume()
        }, 2000)
    }
}
'''

with open(os.path.join(res_dir, 'activity_volunteer_scan.xml'), 'w', encoding='utf-8') as f: f.write(xml_scan)
with open(os.path.join(java_dir, 'VolunteerScanActivity.kt'), 'w', encoding='utf-8') as f: f.write(kt_scan)

print("Generated volunteer scan and participant files")
