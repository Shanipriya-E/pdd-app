import os

filepath = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\java\com\simats\zyntrapass\LoginActivity.kt"

kt = '''package com.simats.zyntrapass

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray

class LoginActivity : AppCompatActivity() {

    private var selectedRole = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainLogin)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val btnAttendee = findViewById<Button>(R.id.btnRoleAttendee)
        val btnOrganizer = findViewById<Button>(R.id.btnRoleOrganizer)
        val btnVolunteer = findViewById<Button>(R.id.btnRoleVolunteer)
        
        val etEmail = findViewById<EditText>(R.id.etEmail)
        val etPassword = findViewById<EditText>(R.id.etPassword)
        val etSecretKey = findViewById<EditText>(R.id.etSecretKey)
        val etVolunteerCode = findViewById<EditText>(R.id.etVolunteerCode)
        
        val btnLogin = findViewById<Button>(R.id.btnLogin)
        val tvCreateAccount = findViewById<TextView>(R.id.tvCreateAccount)

        fun updateUI() {
            btnAttendee.setBackgroundResource(if (selectedRole == "attendee") R.drawable.bg_primary_button else R.drawable.bg_outlined_button)
            btnOrganizer.setBackgroundResource(if (selectedRole == "organizer") R.drawable.bg_primary_button else R.drawable.bg_outlined_button)
            btnVolunteer.setBackgroundResource(if (selectedRole == "volunteer") R.drawable.bg_primary_button else R.drawable.bg_outlined_button)

            if (selectedRole == "volunteer") {
                etEmail.visibility = View.GONE
                etPassword.visibility = View.GONE
                etSecretKey.visibility = View.GONE
                etVolunteerCode.visibility = View.VISIBLE
            } else if (selectedRole == "organizer") {
                etEmail.visibility = View.VISIBLE
                etPassword.visibility = View.VISIBLE
                etSecretKey.visibility = View.VISIBLE
                etVolunteerCode.visibility = View.GONE
            } else {
                etEmail.visibility = View.VISIBLE
                etPassword.visibility = View.VISIBLE
                etSecretKey.visibility = View.GONE
                etVolunteerCode.visibility = View.GONE
            }
        }

        btnAttendee.setOnClickListener {
            selectedRole = "attendee"
            updateUI()
        }

        btnOrganizer.setOnClickListener {
            selectedRole = "organizer"
            updateUI()
        }

        btnVolunteer.setOnClickListener {
            selectedRole = "volunteer"
            updateUI()
        }

        tvCreateAccount.setOnClickListener {
            startActivity(Intent(this, AttendeeSignupActivity::class.java))
        }

        btnLogin.setOnClickListener {
            if (selectedRole.isEmpty()) {
                Toast.makeText(this, "Please select a role first", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            
            btnLogin.text = "Logging in..."
            btnLogin.isEnabled = false
            
            if (selectedRole == "volunteer") {
                val code = etVolunteerCode.text.toString().trim()
                if (code.isEmpty()) {
                    Toast.makeText(this, "Enter Volunteer Code", Toast.LENGTH_SHORT).show()
                    btnLogin.text = "Login"
                    btnLogin.isEnabled = true
                    return@setOnClickListener
                }
                
                CoroutineScope(Dispatchers.IO).launch {
                    try {
                        val res = SupabaseApi.get("rest/v1/volunteers?secret_code=eq.$code&status=eq.approved&select=*,profiles(*)")
                        if (res != null) {
                            val array = JSONArray(res)
                            if (array.length() > 0) {
                                val vol = array.getJSONObject(0)
                                val prefs = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE)
                                prefs.edit()
                                    .putString("volunteer_code", code)
                                    .putString("event_id", vol.getString("event_id"))
                                    .apply()
                                
                                withContext(Dispatchers.Main) {
                                    startActivity(Intent(this@LoginActivity, VolunteerDashboardActivity::class.java))
                                    finish()
                                }
                            } else {
                                withContext(Dispatchers.Main) {
                                    Toast.makeText(this@LoginActivity, "Invalid or unapproved code", Toast.LENGTH_SHORT).show()
                                    btnLogin.text = "Login"
                                    btnLogin.isEnabled = true
                                }
                            }
                        }
                    } catch (e: Exception) {
                        withContext(Dispatchers.Main) {
                            Toast.makeText(this@LoginActivity, "Error", Toast.LENGTH_SHORT).show()
                            btnLogin.text = "Login"
                            btnLogin.isEnabled = true
                        }
                    }
                }
            } else {
                val email = etEmail.text.toString()
                val pass = etPassword.text.toString()
                
                if (email.isEmpty() || pass.isEmpty()) {
                    Toast.makeText(this, "Enter email and password", Toast.LENGTH_SHORT).show()
                    btnLogin.text = "Login"
                    btnLogin.isEnabled = true
                    return@setOnClickListener
                }
                
                CoroutineScope(Dispatchers.Main).launch {
                    val success = SupabaseApi.login(email, pass)
                    if (success) {
                        val profileLoaded = SupabaseApi.fetchProfile()
                        if (profileLoaded && SupabaseApi.currentUserRole == selectedRole) {
                            if (selectedRole == "attendee") {
                                startActivity(Intent(this@LoginActivity, AttendeeDashboardActivity::class.java))
                            } else {
                                startActivity(Intent(this@LoginActivity, OrganizerDashboardActivity::class.java))
                            }
                            finish()
                        } else {
                            Toast.makeText(this@LoginActivity, "Role mismatch or profile error", Toast.LENGTH_SHORT).show()
                            btnLogin.text = "Login"
                            btnLogin.isEnabled = true
                        }
                    } else {
                        Toast.makeText(this@LoginActivity, "Invalid credentials", Toast.LENGTH_SHORT).show()
                        btnLogin.text = "Login"
                        btnLogin.isEnabled = true
                    }
                }
            }
        }
    }
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(kt)

print("Fixed LoginActivity.kt")
