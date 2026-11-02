package com.simats.zyntrapass

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import com.google.android.material.snackbar.Snackbar
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject

class OrganizerSignupActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_organizer_signup)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainSignup)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val etFullName = findViewById<EditText>(R.id.etFullName)
        val etEmail = findViewById<EditText>(R.id.etEmail)
        val etPhone = findViewById<EditText>(R.id.etPhone)
        val etInstitution = findViewById<EditText>(R.id.etInstitution)
        val etAreaCity = findViewById<EditText>(R.id.etAreaCity)
        val etNativePlace = findViewById<EditText>(R.id.etNativePlace)
        val etSecretKey = findViewById<EditText>(R.id.etSecretKey)
        val etPassword = findViewById<EditText>(R.id.etPassword)
        val etConfirmPassword = findViewById<EditText>(R.id.etConfirmPassword)
        val btnSubmitSignup = findViewById<Button>(R.id.btnSubmitSignup)
        

        btnSubmitSignup.setOnClickListener {
            val fullName = etFullName.text.toString().trim()
            val email = etEmail.text.toString().trim()
            val phone = etPhone.text.toString().trim()
            val institution = etInstitution.text.toString().trim()
            val areaCity = etAreaCity.text.toString().trim()
            val nativePlace = etNativePlace.text.toString().trim()
            val secretKey = etSecretKey.text.toString().trim()
            val password = etPassword.text.toString()
            val confirmPassword = etConfirmPassword.text.toString()

            if (fullName.isEmpty() || email.isEmpty() || password.isEmpty() || secretKey.isEmpty()) {
                Snackbar.make(btnSubmitSignup, "Please fill in all required fields", Snackbar.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            if (password != confirmPassword) {
                Snackbar.make(btnSubmitSignup, "Passwords do not match", Snackbar.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            btnSubmitSignup.text = "Submitting..."
            btnSubmitSignup.isEnabled = false

            val profileData = JSONObject().apply {
                put("full_name", fullName)
                put("phone_number", phone)
                put("institution", institution)
                put("area_city", areaCity)
                put("native_place", nativePlace)
                put("secret_key", secretKey) // In production, don't store plain text
            }

            CoroutineScope(Dispatchers.IO).launch {
                val success = SupabaseApi.signUpOrganizer(email, password, profileData)
                withContext(Dispatchers.Main) {
                    if (success) {
                        Snackbar.make(btnSubmitSignup, "Account created! Please log in.", Snackbar.LENGTH_LONG).show()
                        finish() // Go back to login screen
                    } else {
                        Snackbar.make(btnSubmitSignup, "Registration failed", Snackbar.LENGTH_SHORT).show()
                        btnSubmitSignup.text = "Create account"
                        btnSubmitSignup.isEnabled = true
                    }
                }
            }
        }

        findViewById<TextView>(R.id.tvSignIn).setOnClickListener {
            finish() // Go back to login
        }
    }
}
