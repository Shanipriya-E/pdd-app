import os

SIDEBAR_KOTLIN = '''
    // ── Sidebar helper ──────────────────────────────────────────────────
    private fun setupSidebar() {
        val sidebar = findViewById<android.view.View>(R.id.sidebarPanel)
        val dim     = findViewById<android.view.View>(R.id.sidebarDim)
        val btnMenu = findViewById<android.view.View>(R.id.btnMenu)

        fun openSidebar() {
            sidebar.visibility = android.view.View.VISIBLE
            dim.visibility     = android.view.View.VISIBLE
            sidebar.animate().translationX(0f).setDuration(250).start()
            dim.animate().alpha(1f).setDuration(250).start()
        }
        fun closeSidebar() {
            sidebar.animate().translationX(-sidebar.width.toFloat()).setDuration(200).withEndAction {
                sidebar.visibility = android.view.View.GONE
            }.start()
            dim.animate().alpha(0f).setDuration(200).withEndAction {
                dim.visibility = android.view.View.GONE
            }.start()
        }

        // Load name into sidebar avatar
        val currentUserId = SupabaseApi.currentUserId
        if (currentUserId != null) {
            kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
                val profiles = SupabaseApi.fetchProfilesByIds(listOf(currentUserId))
                if (profiles != null && profiles.length() > 0) {
                    val name = profiles.getJSONObject(0).optString("full_name", "User")
                    val email = profiles.getJSONObject(0).optString("email", SupabaseApi.currentUserEmail ?: "")
                    val initials = name.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.joinToString("").take(2).ifEmpty { "U" }
                    findViewById<android.widget.TextView>(R.id.sidebarAvatar)?.text = initials
                    findViewById<android.widget.TextView>(R.id.sidebarName)?.text = name
                }
            }
        }

        btnMenu?.setOnClickListener { openSidebar() }
        dim?.setOnClickListener   { closeSidebar() }

        sidebar?.alpha = 1f
        sidebar?.translationX = -1500f   // start offscreen

        findViewById<android.view.View>(R.id.sidebarNavDashboard)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeDashboardActivity) {
                startActivity(android.content.Intent(this, AttendeeDashboardActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavDiscover)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeDiscoverActivity) {
                startActivity(android.content.Intent(this, AttendeeDiscoverActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavMyEvents)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeEventsActivity) {
                startActivity(android.content.Intent(this, AttendeeEventsActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavAttendance)?.setOnClickListener {
            closeSidebar()
            if (this !is AttendeeAttendanceActivity) {
                startActivity(android.content.Intent(this, AttendeeAttendanceActivity::class.java)); finish()
            }
        }
        findViewById<android.view.View>(R.id.sidebarNavCerts)?.setOnClickListener {
            closeSidebar()
            startActivity(android.content.Intent(this, AttendeeCertificatesActivity::class.java)); finish()
        }
        findViewById<android.view.View>(R.id.sidebarNavSettings)?.setOnClickListener {
            closeSidebar()
            startActivity(android.content.Intent(this, SettingsActivity::class.java)); finish()
        }
        findViewById<android.view.View>(R.id.sidebarNavLogout)?.setOnClickListener {
            SupabaseApi.currentUserId = null
            SupabaseApi.currentUserRole = null
            SupabaseApi.currentUserToken = null
            startActivity(android.content.Intent(this, LoginActivity::class.java).apply { 
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK 
            })
        }
    }
    // ────────────────────────────────────────────────────────────────────
'''

activities = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDashboardActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeEventsActivity.kt',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeAttendanceActivity.kt',
]

for filepath in activities:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'setupSidebar()' in content:
        print(f"Sidebar already wired in {filepath}")
        continue

    # 1. Add import for JSONObject if missing
    if 'import org.json.JSONObject' not in content:
        content = content.replace('import kotlinx.coroutines.launch', 'import kotlinx.coroutines.launch\nimport org.json.JSONObject')

    # 2. Add setupSidebar() call in onCreate after setupBottomNav()
    content = content.replace('setupBottomNav()', 'setupBottomNav()\n        setupSidebar()')

    # 3. Inject setupSidebar function before the closing brace of the class
    # Find last }
    idx = content.rfind('\n}')
    if idx != -1:
        content = content[:idx] + '\n' + SIDEBAR_KOTLIN + '\n}\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wired sidebar in {filepath}")

print("Done!")
