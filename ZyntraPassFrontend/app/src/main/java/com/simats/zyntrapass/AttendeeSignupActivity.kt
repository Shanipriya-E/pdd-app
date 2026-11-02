package com.simats.zyntrapass

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
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
import org.json.JSONObject

class AttendeeSignupActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_attendee_signup)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainAttendeeSignup)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val etFullName = findViewById<EditText>(R.id.etFullName)
        

        findViewById<Button>(R.id.btnSubmitSignup).setOnClickListener {
            handleSignup()
        }

        findViewById<TextView>(R.id.tvSignIn).setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
            finishAffinity()
        }
    }

    private fun handleSignup() {
        val name = findViewById<EditText>(R.id.etFullName).text.toString().trim()
        val email = findViewById<EditText>(R.id.etEmail).text.toString().trim()
        val phone = findViewById<EditText>(R.id.etPhone).text.toString().trim()
        val pass = findViewById<EditText>(R.id.etPassword).text.toString()
        val confirmPass = findViewById<EditText>(R.id.etConfirmPassword).text.toString()
        val inst = findViewById<EditText>(R.id.etInstitution).text.toString().trim()
        val city = findViewById<EditText>(R.id.etCity).text.toString().trim()
        val nativePlace = findViewById<EditText>(R.id.etNative).text.toString().trim()

        if (name.isEmpty() || email.isEmpty() || pass.isEmpty() || inst.isEmpty()) {
            Toast.makeText(this, "Please fill required fields", Toast.LENGTH_SHORT).show()
            return
        }

        if (pass != confirmPass) {
            Toast.makeText(this, "Passwords do not match", Toast.LENGTH_SHORT).show()
            return
        }
        if (pass.length < 8) {
            Toast.makeText(this, "Password must be at least 8 characters", Toast.LENGTH_SHORT).show()
            return
        }

        val btnSubmit = findViewById<Button>(R.id.btnSubmitSignup)
        btnSubmit.isEnabled = false
        btnSubmit.text = "Creating account..."

        val profileData = JSONObject().apply {
            put("full_name", name)
            put("phone_number", phone)
            put("institution", inst)
            put("area_city", city)
            put("native_place", nativePlace)
        }

        CoroutineScope(Dispatchers.Main).launch {
            val success = SupabaseApi.signUpAttendee(email, pass, profileData)
            if (success) {
                Toast.makeText(this@AttendeeSignupActivity, "Account created! Please sign in.", Toast.LENGTH_LONG).show()
                startActivity(Intent(this@AttendeeSignupActivity, LoginActivity::class.java))
                finishAffinity()
            } else {
                Toast.makeText(this@AttendeeSignupActivity, "Signup failed", Toast.LENGTH_LONG).show()
                btnSubmit.isEnabled = true
                btnSubmit.text = "Create account"
            }
        }
    }
}
