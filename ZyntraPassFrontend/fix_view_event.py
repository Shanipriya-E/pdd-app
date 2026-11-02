import os
import re

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a click listener for btnView to show a dialog
btn_view_logic = """
            val btnView = view.findViewById<Button>(R.id.btnView)
            btnView.setOnClickListener {
                val desc = ev.optString("description", "No description provided.")
                val sd = ev.optString("start_date", "TBA")
                val ed = ev.optString("end_date", "TBA")
                val st = ev.optString("start_time", "")
                val et = ev.optString("end_time", "")
                val venue = ev.optString("venue_name", "Online")
                val address = ev.optString("address", "")
                
                val details = StringBuilder()
                details.append("Description:\\n$desc\\n\\n")
                details.append("Schedule:\\n$sd $st - $ed $et\\n\\n")
                details.append("Location:\\n$venue\\n$address")
                
                androidx.appcompat.app.AlertDialog.Builder(this@AttendeeDiscoverActivity)
                    .setTitle(ev.optString("title", "Event Details"))
                    .setMessage(details.toString())
                    .setPositiveButton("Close", null)
                    .show()
            }
"""

if "btnView.setOnClickListener" not in content:
    content = content.replace('val btnRegister = view.findViewById<Button>(R.id.btnRegister)', btn_view_logic + '\n            val btnRegister = view.findViewById<Button>(R.id.btnRegister)')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added view event dialog")
else:
    print("Already added")
