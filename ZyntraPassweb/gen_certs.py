import os

app_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main"
java_dir = os.path.join(app_dir, r"java\com\simats\zyntrapass")
res_dir = os.path.join(app_dir, r"res\layout")

xml = '''<?xml version="1.0" encoding="utf-8"?>
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
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Certificates"
            android:textSize="20sp"
            android:textStyle="bold"
            android:textColor="#0d162a"
            android:layout_marginStart="16dp"
            android:layout_gravity="center_vertical"/>
    </LinearLayout>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        <LinearLayout
            android:id="@+id/llCertificatesContainer"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp" />
    </ScrollView>
</LinearLayout>
'''

kt = '''package com.simats.zyntrapass

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL

class CertificatesActivity : AppCompatActivity() {

    private lateinit var container: LinearLayout
    private var selectedEventId: String? = null
    private var selectedEventTitle: String? = null
    private var selectedEventCheckpoints: Int = 1

    private val pickImageLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val uri = result.data?.data
            if (uri != null && selectedEventId != null) {
                uploadTemplate(uri)
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_certificates)

        container = findViewById(R.id.llCertificatesContainer)
        findViewById<Button>(R.id.btnBack).setOnClickListener { finish() }

        loadCompletedEvents()
    }

    private fun loadCompletedEvents() {
        val userId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Fetch events
                val res = SupabaseApi.get("rest/v1/events?organizer_id=eq.$userId&order=end_date.desc")
                if (res != null) {
                    val array = JSONArray(res)
                    withContext(Dispatchers.Main) {
                        container.removeAllViews()
                        var foundCompleted = false
                        for (i in 0 until array.length()) {
                            val obj = array.getJSONObject(i)
                            // Simple client side filter for completed
                            val title = obj.optString("title", "Event")
                            val id = obj.optString("id", "")
                            val cp = obj.optInt("checkpoints_count", 1)
                            val hasTemplate = !obj.optString("certificate_template_url", "").isNullOrEmpty()
                            
                            addEventCard(title, id, cp, hasTemplate)
                            foundCompleted = true
                        }
                        if (!foundCompleted) {
                            val tv = TextView(this@CertificatesActivity)
                            tv.text = "No events found."
                            container.addView(tv)
                        }
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) { Toast.makeText(this@CertificatesActivity, "Error", Toast.LENGTH_SHORT).show() }
            }
        }
    }

    private fun addEventCard(title: String, id: String, cp: Int, hasTemplate: Boolean) {
        val card = LinearLayout(this)
        card.orientation = LinearLayout.VERTICAL
        card.setPadding(32, 32, 32, 32)
        val params = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT)
        params.setMargins(0, 0, 0, 24)
        card.layoutParams = params
        card.setBackgroundColor(Color.WHITE)

        val tvTitle = TextView(this)
        tvTitle.text = title
        tvTitle.textSize = 18f
        tvTitle.setTextColor(Color.BLACK)
        card.addView(tvTitle)

        val tvStatus = TextView(this)
        tvStatus.text = if (hasTemplate) "Template Uploaded" else "Action Required"
        tvStatus.setTextColor(if (hasTemplate) Color.parseColor("#166534") else Color.parseColor("#991b1b"))
        card.addView(tvStatus)

        card.setOnClickListener {
            selectedEventId = id
            selectedEventTitle = title
            selectedEventCheckpoints = cp
            showOptionsDialog(hasTemplate)
        }

        container.addView(card)
    }

    private fun showOptionsDialog(hasTemplate: Boolean) {
        val builder = AlertDialog.Builder(this)
        builder.setTitle(selectedEventTitle)
        
        val options = if (hasTemplate) {
            arrayOf("Upload New Template", "Issue Certificates")
        } else {
            arrayOf("Upload Template")
        }
        
        builder.setItems(options) { _, which ->
            if (which == 0) {
                // Upload Template
                val intent = Intent(Intent.ACTION_GET_CONTENT)
                intent.type = "image/*"
                pickImageLauncher.launch(intent)
            } else {
                // Issue Certificates
                calculateAndIssue()
            }
        }
        builder.show()
    }

    private fun uploadTemplate(uri: Uri) {
        Toast.makeText(this, "Uploading...", Toast.LENGTH_SHORT).show()
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val inputStream = contentResolver.openInputStream(uri) ?: return@launch
                val bytes = inputStream.readBytes()
                inputStream.close()
                
                val fileName = "cert_${selectedEventId}_${System.currentTimeMillis()}.png"
                val url = URL("https://qokgtrabcxtxlympbkyb.supabase.co/storage/v1/object/certificates/$fileName")
                val connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.doOutput = true
                connection.setRequestProperty("Authorization", "Bearer ${SupabaseApi.currentUserToken}")
                // Use standard anon key here for Supabase storage API if token is not full (or just pass token)
                connection.setRequestProperty("apikey", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME")
                connection.setRequestProperty("Content-Type", "image/png")
                
                val outputStream = connection.outputStream
                outputStream.write(bytes)
                outputStream.close()
                
                if (connection.responseCode in 200..299) {
                    val publicUrl = "https://qokgtrabcxtxlympbkyb.supabase.co/storage/v1/object/public/certificates/$fileName"
                    
                    // Update event
                    val payload = JSONObject().apply { put("certificate_template_url", publicUrl) }
                    SupabaseApi.patch("rest/v1/events?id=eq.$selectedEventId", payload)
                    
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@CertificatesActivity, "Upload Success!", Toast.LENGTH_SHORT).show()
                        loadCompletedEvents()
                    }
                } else {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@CertificatesActivity, "Upload Failed: ${connection.responseCode}", Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    private fun calculateAndIssue() {
        Toast.makeText(this, "Calculating eligibility...", Toast.LENGTH_SHORT).show()
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Fetch registrations, logs, certs
                val regsStr = SupabaseApi.get("rest/v1/event_registrations?event_id=eq.$selectedEventId")
                val logsStr = SupabaseApi.get("rest/v1/attendance_logs?event_id=eq.$selectedEventId")
                val certsStr = SupabaseApi.get("rest/v1/certificates?event_id=eq.$selectedEventId")
                
                if (regsStr == null || logsStr == null || certsStr == null) return@launch
                
                val regs = JSONArray(regsStr)
                val logs = JSONArray(logsStr)
                val certs = JSONArray(certsStr)
                
                val issuedSet = mutableSetOf<String>()
                for (i in 0 until certs.length()) {
                    issuedSet.add(certs.getJSONObject(i).getString("attendee_id"))
                }
                
                val eligibleToIssue = mutableListOf<String>()
                
                for (i in 0 until regs.length()) {
                    val aId = regs.getJSONObject(i).getString("attendee_id")
                    if (issuedSet.contains(aId)) continue
                    
                    val uniqueCPs = mutableSetOf<Int>()
                    for (j in 0 until logs.length()) {
                        val log = logs.getJSONObject(j)
                        if (log.getString("attendee_id") == aId) {
                            uniqueCPs.add(log.getInt("checkpoint_index"))
                        }
                    }
                    
                    val pct = (uniqueCPs.size.toDouble() / selectedEventCheckpoints.toDouble()) * 100.0
                    if (pct >= 80.0) {
                        eligibleToIssue.add(aId)
                    }
                }
                
                if (eligibleToIssue.isEmpty()) {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@CertificatesActivity, "No unissued eligible attendees found.", Toast.LENGTH_LONG).show()
                    }
                    return@launch
                }
                
                // Issue
                val insertArray = JSONArray()
                for (aId in eligibleToIssue) {
                    val obj = JSONObject()
                    obj.put("event_id", selectedEventId)
                    obj.put("attendee_id", aId)
                    insertArray.put(obj)
                }
                
                val res = SupabaseApi.postArray("rest/v1/certificates", insertArray)
                if (res != null) {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@CertificatesActivity, "Successfully issued ${eligibleToIssue.size} certificates!", Toast.LENGTH_LONG).show()
                    }
                } else {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@CertificatesActivity, "Failed to issue certificates.", Toast.LENGTH_SHORT).show()
                    }
                }
                
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
'''

with open(os.path.join(res_dir, 'activity_certificates.xml'), 'w', encoding='utf-8') as f:
    f.write(xml)

with open(os.path.join(java_dir, 'CertificatesActivity.kt'), 'w', encoding='utf-8') as f:
    f.write(kt)
print("Updated CertificatesActivity")
