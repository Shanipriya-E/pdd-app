package com.simats.zyntrapass

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
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
import org.json.JSONObject

class SettingsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_settings)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainSettings)) { v, insets ->
            val sb = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(sb.left, sb.top, sb.right, 0)
            insets
        }

        setupBottomNav()
        setupTabs()
        setupForms()
        
        loadProfile()
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

    private fun setupTabs() {
        val tabAccount = findViewById<LinearLayout>(R.id.tabAccount)
        val tabSecurity = findViewById<LinearLayout>(R.id.tabSecurity)
        val tabNotifications = findViewById<LinearLayout>(R.id.tabNotifications)
        val tabPrivacy = findViewById<LinearLayout>(R.id.tabPrivacy)

        tabAccount.setOnClickListener { switchTab("account") }
        tabSecurity.setOnClickListener { switchTab("security") }
        tabNotifications.setOnClickListener { switchTab("notifications") }
        tabPrivacy.setOnClickListener { switchTab("privacy") }
    }

    private fun switchTab(tab: String) {
        val tabs = listOf(
            Triple("account", findViewById<TextView>(R.id.tvTabAccount), findViewById<View>(R.id.indAccount)),
            Triple("security", findViewById<TextView>(R.id.tvTabSecurity), findViewById<View>(R.id.indSecurity)),
            Triple("notifications", findViewById<TextView>(R.id.tvTabNotifications), findViewById<View>(R.id.indNotifications)),
            Triple("privacy", findViewById<TextView>(R.id.tvTabPrivacy), findViewById<View>(R.id.indPrivacy))
        )

        tabs.forEach { t ->
            if (t.first == tab) {
                t.second.setTextColor(Color.parseColor("#3B35A8"))
                t.third.setBackgroundColor(Color.parseColor("#3B35A8"))
            } else {
                t.second.setTextColor(Color.parseColor("#475569"))
                t.third.setBackgroundColor(Color.TRANSPARENT)
            }
        }

        findViewById<View>(R.id.contentAccount).visibility = if (tab == "account") View.VISIBLE else View.GONE
        findViewById<View>(R.id.contentSecurity).visibility = if (tab == "security") View.VISIBLE else View.GONE
        
        val contentOther = findViewById<View>(R.id.contentOther)
        if (tab == "notifications" || tab == "privacy") {
            contentOther.visibility = View.VISIBLE
            findViewById<TextView>(R.id.tvOtherTitle).text = tab.replaceFirstChar { it.uppercase() }
        } else {
            contentOther.visibility = View.GONE
        }
    }

    private fun loadProfile() {
        val userId = SupabaseApi.currentUserId ?: return
        
        CoroutineScope(Dispatchers.Main).launch {
            val profiles = SupabaseApi.fetchProfilesByIds(listOf(userId))
            if (profiles != null && profiles.length() > 0) {
                val p = profiles.getJSONObject(0)
                
                findViewById<EditText>(R.id.etFullName).setText(p.optString("full_name", ""))
                findViewById<EditText>(R.id.etEmail).setText(SupabaseApi.currentUserEmail ?: "")
                findViewById<EditText>(R.id.etPhone).setText(p.optString("phone", ""))
                findViewById<EditText>(R.id.etInstitution).setText(p.optString("institution", ""))
                findViewById<EditText>(R.id.etCity).setText(p.optString("area_city", ""))
                findViewById<EditText>(R.id.etNative).setText(p.optString("native_place", ""))
                
                val name = p.optString("full_name", "User")
                val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2)
                findViewById<TextView>(R.id.tvUserAvatar).text = initials
            }
        }
    }

    private fun setupForms() {
        val btnSaveProfile = findViewById<Button>(R.id.btnSaveProfile)
        btnSaveProfile.setOnClickListener {
            val updates = JSONObject().apply {
                put("full_name", findViewById<EditText>(R.id.etFullName).text.toString())
                put("phone", findViewById<EditText>(R.id.etPhone).text.toString())
                put("institution", findViewById<EditText>(R.id.etInstitution).text.toString())
                put("area_city", findViewById<EditText>(R.id.etCity).text.toString())
                put("native_place", findViewById<EditText>(R.id.etNative).text.toString())
            }
            
            btnSaveProfile.isEnabled = false
            btnSaveProfile.text = "Saving..."
            
            CoroutineScope(Dispatchers.Main).launch {
                val success = SupabaseApi.updateProfile(updates)
                if (success) {
                    Toast.makeText(this@SettingsActivity, "Profile updated", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this@SettingsActivity, "Failed to update profile", Toast.LENGTH_SHORT).show()
                }
                btnSaveProfile.isEnabled = true
                btnSaveProfile.text = "Save changes"
            }
        }

        findViewById<Button>(R.id.btnLogout).setOnClickListener {
            SupabaseApi.currentUserId = null
            SupabaseApi.currentUserToken = null
            startActivity(Intent(this, MainActivity::class.java))
            finishAffinity()
        }

        val btnUpdatePassword = findViewById<Button>(R.id.btnUpdatePassword)
        btnUpdatePassword.setOnClickListener {
            val newPass = findViewById<EditText>(R.id.etNewPass).text.toString()
            val confirmPass = findViewById<EditText>(R.id.etConfirmPass).text.toString()
            
            if (newPass != confirmPass) {
                Toast.makeText(this, "Passwords do not match", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            
            if (newPass.length < 6) {
                Toast.makeText(this, "Password too short", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            
            btnUpdatePassword.isEnabled = false
            btnUpdatePassword.text = "Updating..."
            
            CoroutineScope(Dispatchers.Main).launch {
                val success = SupabaseApi.updatePassword(newPass)
                if (success) {
                    Toast.makeText(this@SettingsActivity, "Password updated", Toast.LENGTH_SHORT).show()
                    findViewById<EditText>(R.id.etCurrentPass).setText("")
                    findViewById<EditText>(R.id.etNewPass).setText("")
                    findViewById<EditText>(R.id.etConfirmPass).setText("")
                } else {
                    Toast.makeText(this@SettingsActivity, "Failed to update password", Toast.LENGTH_SHORT).show()
                }
                btnUpdatePassword.isEnabled = true
                btnUpdatePassword.text = "Update password"
            }
        }
    }
}
