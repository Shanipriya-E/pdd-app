import os

# We need to add a sidebar overlay to each activity XML and wire it in the Kotlin file.
# The cleanest approach for Android: add an overlay FrameLayout (sidebar panel) to each XML
# and wire the btnMenu to toggle it. We'll do it for all 4 Attendee screens:
# - activity_attendee_dashboard.xml
# - activity_attendee_discover.xml
# - activity_attendee_events.xml
# - activity_attendee_attendance.xml
#
# The sidebar will slide in as an overlay on top of everything, covering the whole screen.

SIDEBAR_OVERLAY = """
    <!-- Dim Overlay: tap to close sidebar -->
    <View
        android:id="@+id/sidebarDim"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:background="#80000000"
        android:visibility="gone"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

    <!-- Sidebar Panel -->
    <LinearLayout
        android:id="@+id/sidebarPanel"
        android:layout_width="280dp"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:background="#1A2340"
        android:visibility="gone"
        android:translationX="-700dp"
        android:elevation="16dp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent">

        <!-- Header -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:padding="20dp"
            android:gravity="center_vertical"
            android:background="#1E2D55"
            android:layout_marginBottom="8dp">
            <TextView
                android:id="@+id/sidebarAvatar"
                android:layout_width="48dp"
                android:layout_height="48dp"
                android:background="@drawable/bg_primary_button"
                android:backgroundTint="#5B54E3"
                android:text="U"
                android:textColor="#FFFFFF"
                android:textSize="18sp"
                android:textStyle="bold"
                android:gravity="center" />
            <LinearLayout
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:orientation="vertical"
                android:layout_marginStart="12dp">
                <TextView
                    android:id="@+id/sidebarName"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="ZyntraPass"
                    android:textColor="#FFFFFF"
                    android:textStyle="bold"
                    android:textSize="16sp" />
                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Attendee workspace"
                    android:textColor="#94A3B8"
                    android:textSize="12sp" />
            </LinearLayout>
        </LinearLayout>

        <!-- Nav Items -->
        <LinearLayout android:id="@+id/sidebarNavDashboard" android:layout_width="match_parent" android:layout_height="56dp" android:gravity="center_vertical" android:paddingHorizontal="20dp" android:orientation="horizontal">
            <TextView android:layout_width="24dp" android:layout_height="24dp" android:text="⊞" android:textColor="#FFFFFF" android:textSize="18sp" android:gravity="center" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Dashboard" android:textColor="#FFFFFF" android:textSize="15sp" android:layout_marginStart="16dp" android:textStyle="bold" />
        </LinearLayout>
        <LinearLayout android:id="@+id/sidebarNavDiscover" android:layout_width="match_parent" android:layout_height="56dp" android:gravity="center_vertical" android:paddingHorizontal="20dp" android:orientation="horizontal">
            <TextView android:layout_width="24dp" android:layout_height="24dp" android:text="🧭" android:textColor="#94A3B8" android:textSize="18sp" android:gravity="center" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Discover" android:textColor="#94A3B8" android:textSize="15sp" android:layout_marginStart="16dp" android:textStyle="bold" />
        </LinearLayout>
        <LinearLayout android:id="@+id/sidebarNavMyEvents" android:layout_width="match_parent" android:layout_height="56dp" android:gravity="center_vertical" android:paddingHorizontal="20dp" android:orientation="horizontal">
            <TextView android:layout_width="24dp" android:layout_height="24dp" android:text="📅" android:textColor="#94A3B8" android:textSize="18sp" android:gravity="center" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="My Events" android:textColor="#94A3B8" android:textSize="15sp" android:layout_marginStart="16dp" android:textStyle="bold" />
        </LinearLayout>
        <LinearLayout android:id="@+id/sidebarNavAttendance" android:layout_width="match_parent" android:layout_height="56dp" android:gravity="center_vertical" android:paddingHorizontal="20dp" android:orientation="horizontal">
            <TextView android:layout_width="24dp" android:layout_height="24dp" android:text="🎟️" android:textColor="#94A3B8" android:textSize="18sp" android:gravity="center" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Attendance" android:textColor="#94A3B8" android:textSize="15sp" android:layout_marginStart="16dp" android:textStyle="bold" />
        </LinearLayout>
        <LinearLayout android:id="@+id/sidebarNavCerts" android:layout_width="match_parent" android:layout_height="56dp" android:gravity="center_vertical" android:paddingHorizontal="20dp" android:orientation="horizontal">
            <TextView android:layout_width="24dp" android:layout_height="24dp" android:text="🏅" android:textColor="#94A3B8" android:textSize="18sp" android:gravity="center" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Certificates" android:textColor="#94A3B8" android:textSize="15sp" android:layout_marginStart="16dp" android:textStyle="bold" />
        </LinearLayout>
        <LinearLayout android:id="@+id/sidebarNavSettings" android:layout_width="match_parent" android:layout_height="56dp" android:gravity="center_vertical" android:paddingHorizontal="20dp" android:orientation="horizontal">
            <TextView android:layout_width="24dp" android:layout_height="24dp" android:text="⚙️" android:textColor="#94A3B8" android:textSize="18sp" android:gravity="center" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Settings" android:textColor="#94A3B8" android:textSize="15sp" android:layout_marginStart="16dp" android:textStyle="bold" />
        </LinearLayout>

        <View android:layout_width="match_parent" android:layout_height="1dp" android:background="#2D3F5E" android:layout_marginVertical="8dp" />

        <LinearLayout android:id="@+id/sidebarNavLogout" android:layout_width="match_parent" android:layout_height="56dp" android:gravity="center_vertical" android:paddingHorizontal="20dp" android:orientation="horizontal">
            <TextView android:layout_width="24dp" android:layout_height="24dp" android:text="🚪" android:textColor="#EF4444" android:textSize="18sp" android:gravity="center" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Logout" android:textColor="#EF4444" android:textSize="15sp" android:layout_marginStart="16dp" android:textStyle="bold" />
        </LinearLayout>
    </LinearLayout>
"""

layouts = [
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_dashboard.xml',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_discover.xml',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_events.xml',
    'c:/Users/Vishnu/zyntraPassForntend/app/src/main/res/layout/activity_attendee_attendance.xml',
]

for layout_path in layouts:
    with open(layout_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if sidebar already added
    if 'sidebarPanel' in content:
        print(f"Sidebar already in {layout_path}")
        continue

    # Insert the sidebar overlay BEFORE the closing tag of the root ConstraintLayout
    content = content.rsplit('</androidx.constraintlayout.widget.ConstraintLayout>', 1)
    if len(content) == 2:
        content = content[0] + SIDEBAR_OVERLAY + '\n</androidx.constraintlayout.widget.ConstraintLayout>\n'
        with open(layout_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added sidebar to {layout_path}")
    else:
        print(f"FAILED to add sidebar to {layout_path} - root tag not found")

print("Done!")
