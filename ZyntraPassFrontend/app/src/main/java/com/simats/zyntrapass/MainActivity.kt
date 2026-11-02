package com.simats.zyntrapass

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val btnCreateAccount = findViewById<Button>(R.id.btnCreateAccount)
        val btnSignIn = findViewById<Button>(R.id.btnSignIn)
        val btnExploreEvents = findViewById<Button>(R.id.btnExploreEvents)
        val btnOrganizeEvent = findViewById<Button>(R.id.btnOrganizeEvent)

        // Sign In goes to LoginActivity
        btnSignIn.setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
        }

        // Create Account goes to RoleSelectionActivity -> then Signup
        btnCreateAccount.setOnClickListener {
            startActivity(Intent(this, RoleSelectionActivity::class.java))
        }

        btnExploreEvents.setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
        }

        btnOrganizeEvent.setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
        }
    }
}