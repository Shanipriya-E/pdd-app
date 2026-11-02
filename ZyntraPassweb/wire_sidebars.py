import os

java_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\java\com\simats\zyntrapass"

# Organizer
org_file = os.path.join(java_dir, 'OrganizerDashboardActivity.kt')
with open(org_file, 'r', encoding='utf-8') as f:
    kt = f.read()

if 'navSidebarCertificates' not in kt:
    inject = '''        findViewById<TextView>(R.id.navSidebarCertificates)?.setOnClickListener {
            startActivity(Intent(this, CertificatesActivity::class.java))
        }\n'''
    kt = kt.replace('findViewById<TextView>(R.id.navSidebarSettings)', inject + '        findViewById<TextView>(R.id.navSidebarSettings)')
    with open(org_file, 'w', encoding='utf-8') as f:
        f.write(kt)

# Attendee
att_file = os.path.join(java_dir, 'AttendeeDashboardActivity.kt')
with open(att_file, 'r', encoding='utf-8') as f:
    kt = f.read()

if 'navSidebarCertificates' not in kt:
    inject = '''        findViewById<TextView>(R.id.navSidebarCertificates)?.setOnClickListener {
            startActivity(Intent(this, AttendeeCertificatesActivity::class.java))
        }\n'''
    kt = kt.replace('findViewById<TextView>(R.id.navSidebarSettings)', inject + '        findViewById<TextView>(R.id.navSidebarSettings)')
    with open(att_file, 'w', encoding='utf-8') as f:
        f.write(kt)

print("Kotlin sidebars wired")
