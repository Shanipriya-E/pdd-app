# Supabase Android Setup Instructions

To use the Supabase Kotlin SDK in your Android Studio project, follow these steps:

### 1. Add Dependencies
Open your app-level `build.gradle.kts` (or `build.gradle`) file and add the following dependencies:

```kotlin
dependencies {
    // Supabase Kotlin SDK
    implementation("io.github.jan-tennert.supabase:postgrest-kt:2.4.3")
    implementation("io.github.jan-tennert.supabase:gotrue-kt:2.4.3")
    
    // Ktor Client for network requests (required by Supabase)
    implementation("io.ktor:ktor-client-android:2.3.11")
}
```

### 2. Enable Internet Permission
Open your `AndroidManifest.xml` (located in `app/src/main/AndroidManifest.xml`) and add this line right above the `<application>` tag:

```xml
<uses-permission android:name="android.permission.INTERNET"/>
```

### 3. Use the Client
You can now use the `SupabaseService.client` defined in `SupabaseService.kt` to interact with your database or authenticate users from anywhere in your app!
