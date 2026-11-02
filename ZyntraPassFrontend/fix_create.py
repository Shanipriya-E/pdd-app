import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/CreateEventActivity.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for date/time picker
if "import android.app.DatePickerDialog" not in content:
    content = content.replace('import android.os.Bundle', 'import android.os.Bundle\nimport android.app.DatePickerDialog\nimport android.app.TimePickerDialog\nimport java.util.Calendar')

# Add bottom nav listeners
bottom_nav = """
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
"""
if "R.id.navDashboard" not in content:
    content = content.replace('// Setup Spinner', bottom_nav + '\n        // Setup Spinner')

# Setup Date/Time pickers
date_time_logic = """
        val etStartDate = findViewById<EditText>(R.id.etStartDate)
        val etEndDate = findViewById<EditText>(R.id.etEndDate)
        val etStartTime = findViewById<EditText>(R.id.etStartTime)
        val etEndTime = findViewById<EditText>(R.id.etEndTime)

        etStartDate.isFocusable = false
        etStartDate.isClickable = true
        etStartDate.setOnClickListener {
            val c = Calendar.getInstance()
            DatePickerDialog(this, { _, y, m, d -> etStartDate.setText(String.format("%02d-%02d-%d", d, m + 1, y)) }, c.get(Calendar.YEAR), c.get(Calendar.MONTH), c.get(Calendar.DAY_OF_MONTH)).show()
        }
        etEndDate.isFocusable = false
        etEndDate.isClickable = true
        etEndDate.setOnClickListener {
            val c = Calendar.getInstance()
            DatePickerDialog(this, { _, y, m, d -> etEndDate.setText(String.format("%02d-%02d-%d", d, m + 1, y)) }, c.get(Calendar.YEAR), c.get(Calendar.MONTH), c.get(Calendar.DAY_OF_MONTH)).show()
        }
        etStartTime.isFocusable = false
        etStartTime.isClickable = true
        etStartTime.setOnClickListener {
            val c = Calendar.getInstance()
            TimePickerDialog(this, { _, h, m -> etStartTime.setText(String.format("%02d:%02d", h, m)) }, c.get(Calendar.HOUR_OF_DAY), c.get(Calendar.MINUTE), true).show()
        }
        etEndTime.isFocusable = false
        etEndTime.isClickable = true
        etEndTime.setOnClickListener {
            val c = Calendar.getInstance()
            TimePickerDialog(this, { _, h, m -> etEndTime.setText(String.format("%02d:%02d", h, m)) }, c.get(Calendar.HOUR_OF_DAY), c.get(Calendar.MINUTE), true).show()
        }
"""
if "TimePickerDialog" not in content:
    content = content.replace('findViewById<TextView>(R.id.btnBackStep2).setOnClickListener {', date_time_logic + '\n        findViewById<TextView>(R.id.btnBackStep2).setOnClickListener {')

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/CreateEventActivity.kt', 'w', encoding='utf-8') as f:
    f.write(content)
