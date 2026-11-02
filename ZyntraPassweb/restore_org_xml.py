import os
xml = '''<?xml version="1.0" encoding="utf-8"?>
<androidx.drawerlayout.widget.DrawerLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/drawerLayout"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#f7f9fc">

    <!-- Main Content -->
    <androidx.constraintlayout.widget.ConstraintLayout
        android:id="@+id/mainDashboard"
        android:layout_width="match_parent"
        android:layout_height="match_parent">

        <LinearLayout
            android:id="@+id/topBar"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:padding="16dp"
            app:layout_constraintTop_toTopOf="parent">
            
            <ImageView
                android:id="@+id/btnMenu"
                android:layout_width="32dp"
                android:layout_height="32dp"
                android:src="@android:drawable/ic_menu_sort_by_size"
                android:background="?selectableItemBackgroundBorderless"/>
        </LinearLayout>
        
        <TextView
            android:id="@+id/tvAvatar"
            android:layout_width="60dp"
            android:layout_height="60dp"
            android:background="#5B54E3"
            android:textColor="#FFFFFF"
            android:textSize="24sp"
            android:textStyle="bold"
            android:gravity="center"
            android:layout_marginTop="24dp"
            app:layout_constraintTop_toBottomOf="@id/topBar"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintEnd_toEndOf="parent"/>

        <TextView
            android:id="@+id/tvGreeting"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Greeting"
            android:textSize="24sp"
            android:textColor="#0d162a"
            android:textStyle="bold"
            android:layout_marginTop="16dp"
            app:layout_constraintTop_toBottomOf="@id/tvAvatar"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintEnd_toEndOf="parent"/>

        <TextView
            android:id="@+id/tvGreetingSub"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Sub"
            android:textSize="14sp"
            android:textColor="#64748b"
            app:layout_constraintTop_toBottomOf="@id/tvGreeting"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintEnd_toEndOf="parent"/>

        <Button
            android:id="@+id/btnCreateEvent"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Create New Event"
            android:backgroundTint="#5b54e3"
            android:layout_marginTop="32dp"
            app:layout_constraintTop_toBottomOf="@id/tvGreetingSub"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintEnd_toEndOf="parent"/>

        <LinearLayout
            android:id="@+id/bottomNav"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:padding="16dp"
            android:background="@android:color/white"
            android:elevation="8dp"
            app:layout_constraintBottom_toBottomOf="parent">
            
            <Button android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="Home"/>
            <Button android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="Events"/>
            <Button android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="Participants"/>
        </LinearLayout>

    </androidx.constraintlayout.widget.ConstraintLayout>

    <!-- Sidebar -->
    <LinearLayout
        android:layout_width="280dp"
        android:layout_height="match_parent"
        android:layout_gravity="start"
        android:background="#0d162a"
        android:orientation="vertical">
        
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="24dp">
            <TextView android:id="@+id/tvSidebarAvatar" android:layout_width="48dp" android:layout_height="48dp" android:background="#5B54E3" android:textColor="#FFFFFF" android:textSize="20sp" android:gravity="center" android:textStyle="bold" />
            <TextView android:id="@+id/tvSidebarName" android:layout_width="match_parent" android:layout_height="wrap_content" android:textColor="#FFFFFF" android:textSize="18sp" android:textStyle="bold" android:layout_marginTop="8dp"/>
            <TextView android:id="@+id/tvSidebarEmail" android:layout_width="match_parent" android:layout_height="wrap_content" android:textColor="#A8B2D1" android:textSize="12sp" />
        </LinearLayout>
        
        <ScrollView android:layout_width="match_parent" android:layout_height="0dp" android:layout_weight="1">
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical">
                <TextView android:id="@+id/navSidebarVolunteers" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Volunteers" android:textColor="#E2E8F0" android:padding="16dp" android:textSize="14sp" android:textStyle="bold" />
                <TextView android:id="@+id/navSidebarCertificates" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Certificates" android:textColor="#E2E8F0" android:padding="16dp" android:textSize="14sp" android:textStyle="bold" />
                <TextView android:id="@+id/navSidebarSettings" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Settings" android:textColor="#E2E8F0" android:padding="16dp" android:textSize="14sp" android:textStyle="bold" />
            </LinearLayout>
        </ScrollView>
        
        <TextView android:id="@+id/btnSidebarLogout" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Logout" android:textColor="#A8B2D1" android:padding="24dp" android:textSize="14sp" android:textStyle="bold" />
    </LinearLayout>

</androidx.drawerlayout.widget.DrawerLayout>
'''
path = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main\res\layout\activity_organizer_dashboard.xml"
with open(path, 'w', encoding='utf-8') as f:
    f.write(xml)
print("Restored activity_organizer_dashboard.xml")
