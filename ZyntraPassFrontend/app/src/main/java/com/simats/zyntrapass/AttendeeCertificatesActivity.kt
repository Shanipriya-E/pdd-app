package com.simats.zyntrapass

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
                val certRes = SupabaseApi.get("rest/v1/certificates?attendee_id=eq.&select=*,events(title,certificate_template_url)")
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
