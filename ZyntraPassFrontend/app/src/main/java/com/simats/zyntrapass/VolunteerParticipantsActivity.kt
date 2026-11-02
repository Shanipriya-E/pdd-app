package com.simats.zyntrapass

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
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
        
        findViewById<View>(R.id.btnBack).setOnClickListener { finish() }
        findViewById<TextView>(R.id.btnLogout).setOnClickListener {
            getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).edit().clear().apply()
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }
        
        findViewById<View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(Intent(this, VolunteerDashboardActivity::class.java))
            finish()
        }
        
        findViewById<View>(R.id.navScan)?.setOnClickListener {
            startActivity(Intent(this, VolunteerScanActivity::class.java))
            finish()
        }
        
        loadStats()
    }
    
    private fun loadStats() {
        val prefs = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE)
        val eventId = prefs.getString("event_id", "") ?: ""
        val code = prefs.getString("volunteer_code", "") ?: ""
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Fetch stats via RPC just like the web app
                val payload = JSONObject().apply {
                    put("v_code", code)
                    put("e_id", eventId)
                }
                
                val res = SupabaseApi.postRpc("volunteer_get_event_stats", payload)
                if (res != null) {
                    val obj = JSONObject(res)
                    val attended = obj.optInt("attended", 0)
                    val approved = obj.optInt("approved", 0)
                    val totalRegistered = obj.optInt("total_registered", 0)
                    val rejected = obj.optInt("rejected", 0)
                    
                    withContext(Dispatchers.Main) {
                        findViewById<TextView>(R.id.tvTotal)?.text = attended.toString()
                        findViewById<TextView>(R.id.tvApproved)?.text = approved.toString()
                        findViewById<TextView>(R.id.tvPending)?.text = totalRegistered.toString() // ID is tvPending in XML but represents REGISTERED
                        findViewById<TextView>(R.id.tvRejected)?.text = rejected.toString()
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) { Toast.makeText(this@VolunteerParticipantsActivity, "Error loading stats", Toast.LENGTH_SHORT).show() }
            }
        }
    }
}
