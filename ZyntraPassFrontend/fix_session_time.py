import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/CreateEventActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate addSessionView()
search_str = """        fun addSessionView() {
            val sessionView = layoutInflater.inflate(R.layout.item_session_form, sessionsContainer, false)"""

replace_str = """        fun addSessionView() {
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
            }"""

if search_str in content and "etSessionStart" not in content:
    content = content.replace(search_str, replace_str)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added TimePickerDialog to session form.")
else:
    print("Could not find addSessionView or it was already added.")
