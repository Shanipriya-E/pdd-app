package com.simats.zyntrapass

import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import com.google.android.material.snackbar.Snackbar
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class RoleSelectionActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_role_selection)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainRole)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        findViewById<Button>(R.id.btnAttendee).setOnClickListener {
            handleRoleSelection("Attendee")
        }
        
        findViewById<Button>(R.id.btnOrganizer).setOnClickListener {
            handleRoleSelection("Organizer")
        }
    }

    private fun handleRoleSelection(role: String) {
        if (role == "Organizer") {
            startActivity(android.content.Intent(this, OrganizerSignupActivity::class.java))
        } else if (role == "Attendee") {
            startActivity(android.content.Intent(this, AttendeeSignupActivity::class.java))
        } else {
            Snackbar.make(findViewById(R.id.mainRole), "Signup for $role coming soon! Try Organizer.", Snackbar.LENGTH_SHORT).show()
        }
    }
}
