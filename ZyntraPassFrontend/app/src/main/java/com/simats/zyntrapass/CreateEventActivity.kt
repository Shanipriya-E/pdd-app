package com.simats.zyntrapass

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.app.DatePickerDialog
import android.app.TimePickerDialog
import java.util.Calendar
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.launch

class CreateEventActivity : AppCompatActivity() {

    private var currentUploadButton: android.widget.TextView? = null
    private val pickImageLauncher = registerForActivityResult(androidx.activity.result.contract.ActivityResultContracts.GetContent()) { uri: android.net.Uri? ->
        if (uri != null) {
            currentUploadButton?.text = "Photo Selected"
            currentUploadButton?.setBackgroundResource(R.drawable.bg_primary_button) // A nice background
            currentUploadButton?.setTextColor(android.graphics.Color.parseColor("#FFFFFF"))
        }
    }


    private var selectedImageUri: Uri? = null

    private val selectImageLauncher = registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
        uri?.let {
            selectedImageUri = it
            findViewById<ImageView>(R.id.ivBannerPreview).apply {
                setImageURI(it)
                visibility = View.VISIBLE
            }
            findViewById<LinearLayout>(R.id.uploadPlaceholder).visibility = View.GONE
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_create_event)
        setupBottomNav()

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainCreateEvent)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.ime())
            v.setPadding(0, systemBars.top, 0, systemBars.bottom)
            insets
        }

        // Setup Avatar
        val name = SupabaseApi.currentUserName ?: "Organizer"
        val initials = name.split(" ").mapNotNull { it.firstOrNull()?.toString() }.joinToString("").take(2).uppercase()
        findViewById<TextView>(R.id.tvAvatar).text = initials

        
        findViewById<android.view.View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navEvents)?.setOnClickListener {
            startActivity(Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navParticipants)?.setOnClickListener {
            startActivity(Intent(this, ParticipantsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navLive)?.setOnClickListener {
            startActivity(Intent(this, LiveAttendanceActivity::class.java))
            finish()
        }

        // Setup Spinner
        val spinner = findViewById<Spinner>(R.id.spinnerCategory)
        val categories = arrayOf("Summit", "Workshop", "Conference", "Meetup", "Hackathon")
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, categories)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinner.adapter = adapter

        // Setup Image Picker
        findViewById<LinearLayout>(R.id.uploadBox).setOnClickListener {
            selectImageLauncher.launch("image/*")
        }

        findViewById<TextView>(R.id.btnBack).setOnClickListener {
            finish()
        }

        findViewById<Button>(R.id.btnContinue).setOnClickListener {
            val title = findViewById<EditText>(R.id.etEventName).text.toString()
            if (title.isEmpty()) {
                Toast.makeText(this, "Please enter an event name", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Transition to Step 2
            findViewById<LinearLayout>(R.id.cardStep1).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep2).visibility = View.VISIBLE
        }

        
        val etStartDate = findViewById<android.widget.EditText>(R.id.etStartDate)
        val etEndDate = findViewById<android.widget.EditText>(R.id.etEndDate)
        val etStartTime = findViewById<android.widget.EditText>(R.id.etStartTime)
        val etEndTime = findViewById<android.widget.EditText>(R.id.etEndTime)

        etStartDate.isFocusable = false
        etStartDate.isClickable = true
        etStartDate.setOnClickListener {
            val c = java.util.Calendar.getInstance()
            android.app.DatePickerDialog(this, { _, y, m, d -> etStartDate.setText(String.format("%d-%02d-%02d", y, m + 1, d)) }, c.get(java.util.Calendar.YEAR), c.get(java.util.Calendar.MONTH), c.get(java.util.Calendar.DAY_OF_MONTH)).show()
        }
        etEndDate.isFocusable = false
        etEndDate.isClickable = true
        etEndDate.setOnClickListener {
            val c = java.util.Calendar.getInstance()
            android.app.DatePickerDialog(this, { _, y, m, d -> etEndDate.setText(String.format("%d-%02d-%02d", y, m + 1, d)) }, c.get(java.util.Calendar.YEAR), c.get(java.util.Calendar.MONTH), c.get(java.util.Calendar.DAY_OF_MONTH)).show()
        }
        etStartTime.isFocusable = false
        etStartTime.isClickable = true
        etStartTime.setOnClickListener {
            val c = java.util.Calendar.getInstance()
            android.app.TimePickerDialog(this, { _, h, m -> etStartTime.setText(String.format("%02d:%02d", h, m)) }, c.get(java.util.Calendar.HOUR_OF_DAY), c.get(java.util.Calendar.MINUTE), true).show()
        }
        etEndTime.isFocusable = false
        etEndTime.isClickable = true
        etEndTime.setOnClickListener {
            val c = java.util.Calendar.getInstance()
            android.app.TimePickerDialog(this, { _, h, m -> etEndTime.setText(String.format("%02d:%02d", h, m)) }, c.get(java.util.Calendar.HOUR_OF_DAY), c.get(java.util.Calendar.MINUTE), true).show()
        }

        findViewById<TextView>(R.id.btnBackStep2).setOnClickListener {
            findViewById<LinearLayout>(R.id.cardStep2).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep1).visibility = View.VISIBLE
        }

        findViewById<Button>(R.id.btnContinueStep2).setOnClickListener {
            val startDate = findViewById<EditText>(R.id.etStartDate).text.toString()
            val endDate = findViewById<EditText>(R.id.etEndDate).text.toString()
            val startTime = findViewById<EditText>(R.id.etStartTime).text.toString()
            val endTime = findViewById<EditText>(R.id.etEndTime).text.toString()

            if (startDate.isEmpty() || endDate.isEmpty() || startTime.isEmpty() || endTime.isEmpty()) {
                Toast.makeText(this, "Please fill out all date and time fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Transition to Step 3
            findViewById<LinearLayout>(R.id.cardStep2).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep3).visibility = View.VISIBLE
        }

        // Step 3 Logic
        val updateGeofenceText = {
            val lat = findViewById<EditText>(R.id.etLat).text.toString().ifEmpty { "13.0108" }
            val lng = findViewById<EditText>(R.id.etLng).text.toString().ifEmpty { "74.7943" }
            val radius = findViewById<EditText>(R.id.etRadius).text.toString().ifEmpty { "100" }
            findViewById<TextView>(R.id.tvGeofence).text = "$radius m geofence · $lat, $lng"
        }

        val textWatcher = object : android.text.TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: android.text.Editable?) { updateGeofenceText() }
        }
        findViewById<EditText>(R.id.etLat).addTextChangedListener(textWatcher)
        findViewById<EditText>(R.id.etLng).addTextChangedListener(textWatcher)
        findViewById<EditText>(R.id.etRadius).addTextChangedListener(textWatcher)

        findViewById<TextView>(R.id.btnBackStep3).setOnClickListener {
            findViewById<LinearLayout>(R.id.cardStep3).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep2).visibility = View.VISIBLE
        }

        findViewById<Button>(R.id.btnContinueStep3).setOnClickListener {
            val venue = findViewById<EditText>(R.id.etVenue).text.toString()
            val lat = findViewById<EditText>(R.id.etLat).text.toString()
            val lng = findViewById<EditText>(R.id.etLng).text.toString()
            val radius = findViewById<EditText>(R.id.etRadius).text.toString()

            if (venue.isEmpty() || lat.isEmpty() || lng.isEmpty() || radius.isEmpty()) {
                Toast.makeText(this, "Please fill out required location fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Transition to Step 4
            findViewById<LinearLayout>(R.id.cardStep3).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep4).visibility = View.VISIBLE
        }

        // Step 4 Logic
        val guestsContainer = findViewById<LinearLayout>(R.id.llGuestsContainer)
        
        fun updateRemoveButtons() {
            val childCount = guestsContainer.childCount
            for (i in 0 until childCount) {
                val view = guestsContainer.getChildAt(i)
                val btnRemove = view.findViewById<View>(R.id.btnRemoveGuest)
                btnRemove.visibility = if (childCount == 1) View.GONE else View.VISIBLE
            }
        }

        fun addGuestView() {
            val guestView = layoutInflater.inflate(R.layout.item_guest_form, guestsContainer, false)
            
            guestView.findViewById<View>(R.id.btnRemoveGuest).setOnClickListener {
                guestsContainer.removeView(guestView)
                updateRemoveButtons()
            }
            
            // Photo upload click handler would go here. For now it's just visual.
            guestView.findViewById<View>(R.id.btnUploadPhoto).setOnClickListener {
                
                currentUploadButton = guestView.findViewById<android.widget.TextView>(R.id.btnUploadPhoto)
                pickImageLauncher.launch("image/*")

            }

            guestsContainer.addView(guestView)
            updateRemoveButtons()
        }

        // Add first guest by default
        addGuestView()

        findViewById<View>(R.id.btnAddGuest).setOnClickListener {
            addGuestView()
        }

        findViewById<TextView>(R.id.btnBackStep4).setOnClickListener {
            findViewById<LinearLayout>(R.id.cardStep4).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep3).visibility = View.VISIBLE
        }

        findViewById<Button>(R.id.btnContinueStep4).setOnClickListener {
            var hasData = false
            for (i in 0 until guestsContainer.childCount) {
                val view = guestsContainer.getChildAt(i)
                val name = view.findViewById<EditText>(R.id.etGuestName).text.toString()
                if (name.isNotEmpty()) {
                    hasData = true
                    break
                }
            }

            if (!hasData) {
                Toast.makeText(this, "Please add at least one guest with a name", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Transition to Step 5
            findViewById<LinearLayout>(R.id.cardStep4).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep5).visibility = View.VISIBLE
        }

        // Step 5 Logic
        val sessionsContainer = findViewById<LinearLayout>(R.id.llSessionsContainer)
        
        fun updateRemoveSessionButtons() {
            val childCount = sessionsContainer.childCount
            for (i in 0 until childCount) {
                val view = sessionsContainer.getChildAt(i)
                val btnRemove = view.findViewById<View>(R.id.btnRemoveSession)
                btnRemove.visibility = if (childCount == 1) View.GONE else View.VISIBLE
            }
        }

        fun addSessionView() {
            val sessionView = layoutInflater.inflate(R.layout.item_session_form, sessionsContainer, false)
            
            val etStart = sessionView.findViewById<android.widget.EditText>(R.id.etSessionStart)
            val etEnd = sessionView.findViewById<android.widget.EditText>(R.id.etSessionEnd)
            
            etStart.setOnClickListener {
                val c = java.util.Calendar.getInstance()
                android.app.TimePickerDialog(this, { _, h, m -> etStart.setText(String.format("%02d:%02d", h, m)) }, c.get(java.util.Calendar.HOUR_OF_DAY), c.get(java.util.Calendar.MINUTE), true).show()
            }
            
            etEnd.setOnClickListener {
                val c = java.util.Calendar.getInstance()
                android.app.TimePickerDialog(this, { _, h, m -> etEnd.setText(String.format("%02d:%02d", h, m)) }, c.get(java.util.Calendar.HOUR_OF_DAY), c.get(java.util.Calendar.MINUTE), true).show()
            }
            
            sessionView.findViewById<View>(R.id.btnRemoveSession).setOnClickListener {
                sessionsContainer.removeView(sessionView)
                updateRemoveSessionButtons()
            }

            sessionsContainer.addView(sessionView)
            updateRemoveSessionButtons()
        }

        // Add first session by default
        addSessionView()

        findViewById<View>(R.id.btnAddSession).setOnClickListener {
            addSessionView()
        }

        findViewById<TextView>(R.id.btnBackStep5).setOnClickListener {
            findViewById<LinearLayout>(R.id.cardStep5).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep4).visibility = View.VISIBLE
        }

        findViewById<Button>(R.id.btnContinueStep5).setOnClickListener {
            var hasData = false
            for (i in 0 until sessionsContainer.childCount) {
                val view = sessionsContainer.getChildAt(i)
                val name = view.findViewById<EditText>(R.id.etSessionName).text.toString()
                if (name.isNotEmpty()) {
                    hasData = true
                    break
                }
            }

            if (!hasData) {
                Toast.makeText(this, "Please add at least one session with a name", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Transition to Step 6
            findViewById<LinearLayout>(R.id.cardStep5).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep6).visibility = View.VISIBLE
        }

        // Step 6 Logic
        val spinnerTiming = findViewById<android.widget.Spinner>(R.id.spinnerCheckpointTiming)
        val timingOptions = arrayOf("Every 30 minutes", "Every 60 minutes", "Entry, mid, session, exit", "Custom per session")
        val timingAdapter = android.widget.ArrayAdapter(this, android.R.layout.simple_spinner_item, timingOptions)
        timingAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerTiming.adapter = timingAdapter
        spinnerTiming.setSelection(1) // Default to Every 60 minutes

        findViewById<TextView>(R.id.btnBackStep6).setOnClickListener {
            findViewById<LinearLayout>(R.id.cardStep6).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep5).visibility = View.VISIBLE
        }

        findViewById<Button>(R.id.btnContinueStep6).setOnClickListener {
            val checkpointsCount = findViewById<EditText>(R.id.etCheckpointsCount).text.toString()
            val timing = spinnerTiming.selectedItem.toString()
            val minAttendance = findViewById<EditText>(R.id.etMinAttendance).text.toString()
            val qrRefresh = findViewById<EditText>(R.id.etQrRefresh).text.toString()

            if (checkpointsCount.isEmpty() || minAttendance.isEmpty() || qrRefresh.isEmpty()) {
                Toast.makeText(this, "Please fill out all attendance rules", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Transition to Step 7
            findViewById<LinearLayout>(R.id.cardStep6).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep7).visibility = View.VISIBLE
            
            // Populate Preview
            findViewById<TextView>(R.id.tvPreviewTitle).text = findViewById<EditText>(R.id.etEventName).text.toString().ifEmpty { "Untitled event" }
            findViewById<TextView>(R.id.tvPreviewCategory).text = findViewById<Spinner>(R.id.spinnerCategory).selectedItem.toString()
            findViewById<TextView>(R.id.tvPreviewDesc).text = findViewById<EditText>(R.id.etEventDescription).text.toString().ifEmpty { "No description added yet." }
            
            val startDate = findViewById<EditText>(R.id.etStartDate).text.toString()
            val startTime = findViewById<EditText>(R.id.etStartTime).text.toString()
            val endTime = findViewById<EditText>(R.id.etEndTime).text.toString()
            findViewById<TextView>(R.id.tvPreviewSchedule).text = "$startDate · $startTime–$endTime"
            
            findViewById<TextView>(R.id.tvPreviewVenue).text = findViewById<EditText>(R.id.etVenue).text.toString().ifEmpty { "—" }
            findViewById<TextView>(R.id.tvPreviewGeofence).text = "${findViewById<EditText>(R.id.etRadius).text.toString().ifEmpty { "0" }} m radius"
            
            val numGuests = findViewById<LinearLayout>(R.id.llGuestsContainer).childCount
            findViewById<TextView>(R.id.tvPreviewGuests).text = "$numGuests added"
            
            val numSessions = findViewById<LinearLayout>(R.id.llSessionsContainer).childCount
            findViewById<TextView>(R.id.tvPreviewSessions).text = "$numSessions added"
            
            findViewById<TextView>(R.id.tvPreviewRules).text = "${checkpointsCount.ifEmpty { "0" }} checkpoints · ${minAttendance.ifEmpty { "0" }}% minimum · ${qrRefresh.ifEmpty { "10" }}s QR"
        }

        findViewById<TextView>(R.id.btnBackStep7).setOnClickListener {
            findViewById<LinearLayout>(R.id.cardStep7).visibility = View.GONE
            findViewById<LinearLayout>(R.id.cardStep6).visibility = View.VISIBLE
        }

        findViewById<Button>(R.id.btnPublishEvent).setOnClickListener {
            val btnPublish = it as Button
            btnPublish.text = "Publishing..."
            btnPublish.isEnabled = false

            // Assemble Payload for the main Event table
            val payload = org.json.JSONObject()
            payload.put("title", findViewById<EditText>(R.id.etEventName).text.toString())
            payload.put("category", findViewById<Spinner>(R.id.spinnerCategory).selectedItem.toString())
            payload.put("description", findViewById<EditText>(R.id.etEventDescription).text.toString())
            payload.put("start_date", findViewById<EditText>(R.id.etStartDate).text.toString())
            payload.put("end_date", findViewById<EditText>(R.id.etEndDate).text.toString())
            payload.put("start_time", findViewById<EditText>(R.id.etStartTime).text.toString())
            payload.put("end_time", findViewById<EditText>(R.id.etEndTime).text.toString())
            payload.put("venue_name", findViewById<EditText>(R.id.etVenue).text.toString())
            payload.put("address", findViewById<EditText>(R.id.etAddress).text.toString())
            payload.put("latitude", findViewById<EditText>(R.id.etLat).text.toString().toDoubleOrNull() ?: 0.0)
            payload.put("longitude", findViewById<EditText>(R.id.etLng).text.toString().toDoubleOrNull() ?: 0.0)
            payload.put("attendance_radius_meters", findViewById<EditText>(R.id.etRadius).text.toString().toIntOrNull() ?: 0)
            payload.put("checkpoints_count", findViewById<EditText>(R.id.etCheckpointsCount).text.toString().toIntOrNull() ?: 0)
            payload.put("checkpoint_timing", findViewById<Spinner>(R.id.spinnerCheckpointTiming).selectedItem.toString())
            payload.put("min_attendance_percent", findViewById<EditText>(R.id.etMinAttendance).text.toString().toIntOrNull() ?: 0)
            payload.put("qr_refresh_interval_sec", findViewById<EditText>(R.id.etQrRefresh).text.toString().toIntOrNull() ?: 10)

            kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
                val success = SupabaseApi.createFullEvent(payload)
                if (success) {
                    Toast.makeText(this@CreateEventActivity, "Event successfully created and published!", Toast.LENGTH_LONG).show()
                    startActivity(Intent(this@CreateEventActivity, EventsActivity::class.java))
                    finish()
                } else {
                    Toast.makeText(this@CreateEventActivity, "Failed to publish event", Toast.LENGTH_SHORT).show()
                    btnPublish.text = "Create Event"
                    btnPublish.isEnabled = true
                }
            }
        }
    }

    private fun setupBottomNav() { 
        findViewById<android.view.View>(R.id.navDashboard)?.setOnClickListener {
            startActivity(android.content.Intent(this, OrganizerDashboardActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navEvents)?.setOnClickListener {
            startActivity(android.content.Intent(this, EventsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navParticipants)?.setOnClickListener {
            startActivity(android.content.Intent(this, ParticipantsActivity::class.java))
            finish()
        }
        findViewById<android.view.View>(R.id.navLive)?.setOnClickListener {
            startActivity(android.content.Intent(this, LiveAttendanceActivity::class.java))
            finish()
        }
 }

}