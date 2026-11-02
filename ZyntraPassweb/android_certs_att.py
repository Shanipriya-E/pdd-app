import os

app_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main"
java_dir = os.path.join(app_dir, r"java\com\simats\zyntrapass")
res_dir = os.path.join(app_dir, r"res\layout")

kt_att = '''package com.simats.zyntrapass

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL

class AttendeeCertificatesActivity : AppCompatActivity() {

    private lateinit var container: LinearLayout
    private lateinit var currentBitmap: Bitmap

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_attendee_certificates)

        container = findViewById(R.id.llCertificatesContainer)

        val btnBack = findViewById<Button>(R.id.btnBack)
        btnBack.setOnClickListener { finish() }

        loadCertificates()
    }

    private fun loadCertificates() {
        val attendeeId = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).getString("user_id", "") ?: ""
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // In a real app we join, but let's do a simple fetch
                val certRes = SupabaseApi.get("rest/v1/certificates?attendee_id=eq.\&select=*,events(title,certificate_template_url)")
                if (certRes != null) {
                    val array = JSONArray(certRes)
                    withContext(Dispatchers.Main) {
                        if (array.length() == 0) {
                            Toast.makeText(this@AttendeeCertificatesActivity, "No certificates found", Toast.LENGTH_SHORT).show()
                        }
                        for (i in 0 until array.length()) {
                            val obj = array.getJSONObject(i)
                            val eventsObj = obj.getJSONObject("events")
                            val title = eventsObj.getString("title")
                            val url = eventsObj.optString("certificate_template_url", "")
                            
                            addCertificateCard(title, url)
                        }
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    Toast.makeText(this@AttendeeCertificatesActivity, "Error loading certs", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun addCertificateCard(title: String, url: String) {
        val tv = TextView(this)
        tv.text = title
        tv.textSize = 18f
        tv.setPadding(16, 16, 16, 16)
        
        val img = ImageView(this)
        img.layoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            600
        )
        
        container.addView(tv)
        container.addView(img)
        
        if (url.isNotEmpty()) {
            CoroutineScope(Dispatchers.IO).launch {
                try {
                    val connection = URL(url).openConnection() as HttpURLConnection
                    connection.doInput = true
                    connection.connect()
                    val input: InputStream = connection.inputStream
                    val bitmap = BitmapFactory.decodeStream(input)
                    
                    val userName = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).getString("user_name", "Attendee") ?: "Attendee"
                    
                    // Draw on canvas
                    val mutableBitmap = bitmap.copy(Bitmap.Config.ARGB_8888, true)
                    val canvas = Canvas(mutableBitmap)
                    val paint = Paint(Paint.ANTI_ALIAS_FLAG)
                    paint.color = Color.BLACK
                    paint.textSize = (mutableBitmap.height * 0.08).toFloat()
                    paint.textAlign = Paint.Align.CENTER
                    
                    canvas.drawText(userName, (mutableBitmap.width / 2).toFloat(), (mutableBitmap.height / 2).toFloat(), paint)
                    
                    withContext(Dispatchers.Main) {
                        img.setImageBitmap(mutableBitmap)
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }
}
'''

with open(os.path.join(java_dir, 'AttendeeCertificatesActivity.kt'), 'w', encoding='utf-8') as f:
    f.write(kt_att)

xml_att = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#f7f9fc">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:background="@android:color/white"
        android:elevation="4dp"
        android:padding="16dp">

        <Button
            android:id="@+id/btnBack"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Back"
            android:backgroundTint="#e2e8f0"
            android:textColor="#0d162a"/>

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="My Certificates"
            android:textSize="20sp"
            android:textStyle="bold"
            android:textColor="#0d162a"
            android:layout_marginStart="16dp"
            android:layout_gravity="center_vertical"/>
    </LinearLayout>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        <LinearLayout
            android:id="@+id/llCertificatesContainer"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp" />
    </ScrollView>
</LinearLayout>
'''

with open(os.path.join(res_dir, 'activity_attendee_certificates.xml'), 'w', encoding='utf-8') as f:
    f.write(xml_att)

print("Updated Android Attendee implementation")
