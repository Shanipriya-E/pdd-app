import os
import shutil
import re

base_path = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/'

# 1. Layouts
shutil.copyfile(base_path + 'res/layout/activity_attendee_discover.xml', base_path + 'res/layout/activity_attendee_events.xml')
shutil.copyfile(base_path + 'res/layout/activity_attendee_discover.xml', base_path + 'res/layout/activity_attendee_attendance.xml')

# Edit activity_attendee_events.xml
with open(base_path + 'res/layout/activity_attendee_events.xml', 'r', encoding='utf-8') as f:
    ev_xml = f.read()
ev_xml = ev_xml.replace('activity_attendee_discover', 'activity_attendee_events')
ev_xml = ev_xml.replace('Discover events', 'My Events')
ev_xml = ev_xml.replace('Summits, bootcamps, workshops, competitions and cultural fests across every organisation.', 'Events you have registered for or volunteered for.')
with open(base_path + 'res/layout/activity_attendee_events.xml', 'w', encoding='utf-8') as f:
    f.write(ev_xml)

# Edit activity_attendee_attendance.xml
with open(base_path + 'res/layout/activity_attendee_attendance.xml', 'r', encoding='utf-8') as f:
    att_xml = f.read()
att_xml = att_xml.replace('activity_attendee_discover', 'activity_attendee_attendance')
att_xml = att_xml.replace('Discover events', 'Attendance History')
att_xml = att_xml.replace('Summits, bootcamps, workshops, competitions and cultural fests across every organisation.', 'Your verified check-in records for all sessions.')
with open(base_path + 'res/layout/activity_attendee_attendance.xml', 'w', encoding='utf-8') as f:
    f.write(att_xml)

# 2. Activities
shutil.copyfile(base_path + 'java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt', base_path + 'java/com/simats/zyntrapass/AttendeeEventsActivity.kt')
shutil.copyfile(base_path + 'java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt', base_path + 'java/com/simats/zyntrapass/AttendeeAttendanceActivity.kt')

# Edit AttendeeEventsActivity.kt
with open(base_path + 'java/com/simats/zyntrapass/AttendeeEventsActivity.kt', 'r', encoding='utf-8') as f:
    ev_kt = f.read()
ev_kt = ev_kt.replace('class AttendeeDiscoverActivity', 'class AttendeeEventsActivity')
ev_kt = ev_kt.replace('R.layout.activity_attendee_discover', 'R.layout.activity_attendee_events')
ev_kt = ev_kt.replace('this@AttendeeDiscoverActivity', 'this@AttendeeEventsActivity')
# Only show registered events
ev_kt = ev_kt.replace('val isRegistered = registrationsMap.containsKey(eventId)', 'val isRegistered = registrationsMap.containsKey(eventId)\n            if (!isRegistered) continue // ONLY SHOW MY EVENTS')
with open(base_path + 'java/com/simats/zyntrapass/AttendeeEventsActivity.kt', 'w', encoding='utf-8') as f:
    f.write(ev_kt)
    
print("Created layout and activities for Events and Attendance")
