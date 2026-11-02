import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/CreateEventActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

date_time_logic = """
        val etStartDate = findViewById<android.widget.EditText>(R.id.etStartDate)
        val etEndDate = findViewById<android.widget.EditText>(R.id.etEndDate)
        val etStartTime = findViewById<android.widget.EditText>(R.id.etStartTime)
        val etEndTime = findViewById<android.widget.EditText>(R.id.etEndTime)

        etStartDate.isFocusable = false
        etStartDate.isClickable = true
        etStartDate.setOnClickListener {
            val c = java.util.Calendar.getInstance()
            android.app.DatePickerDialog(this, { _, y, m, d -> etStartDate.setText(String.format("%02d-%02d-%d", d, m + 1, y)) }, c.get(java.util.Calendar.YEAR), c.get(java.util.Calendar.MONTH), c.get(java.util.Calendar.DAY_OF_MONTH)).show()
        }
        etEndDate.isFocusable = false
        etEndDate.isClickable = true
        etEndDate.setOnClickListener {
            val c = java.util.Calendar.getInstance()
            android.app.DatePickerDialog(this, { _, y, m, d -> etEndDate.setText(String.format("%02d-%02d-%d", d, m + 1, y)) }, c.get(java.util.Calendar.YEAR), c.get(java.util.Calendar.MONTH), c.get(java.util.Calendar.DAY_OF_MONTH)).show()
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
"""

if "DatePickerDialog(this" not in content:
    content = content.replace('findViewById<TextView>(R.id.btnBackStep2).setOnClickListener {', date_time_logic + '\n        findViewById<TextView>(R.id.btnBackStep2).setOnClickListener {')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Injected body.")
else:
    print("Already there.")
