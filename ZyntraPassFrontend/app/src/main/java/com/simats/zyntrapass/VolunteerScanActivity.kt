package com.simats.zyntrapass

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.journeyapps.barcodescanner.DecoratedBarcodeView
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject

class VolunteerScanActivity : AppCompatActivity() {

    private lateinit var barcodeView: DecoratedBarcodeView
    private lateinit var tvStatus: TextView
    private lateinit var layoutStatus: LinearLayout
    private lateinit var btnScanAnother: Button
    private var isProcessing = false

    companion object {
        private const val CAMERA_PERMISSION_CODE = 1001
        private const val QR_EXPIRY_MS = 120_000L // 2 minutes, same as web
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_volunteer_scan)

        barcodeView = findViewById(R.id.barcodeScannerView)
        tvStatus = findViewById(R.id.tvScanStatus)
        layoutStatus = findViewById(R.id.layoutScanStatus)
        btnScanAnother = findViewById(R.id.btnScanAnother)

        barcodeView.setStatusText("Align the attendee's QR code within the frame")

        findViewById<Button>(R.id.btnBack).setOnClickListener { finish() }
        findViewById<TextView>(R.id.btnLogout).setOnClickListener {
            getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE).edit().clear().apply()
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }

        btnScanAnother.setOnClickListener {
            layoutStatus.visibility = View.GONE
            btnScanAnother.visibility = View.GONE
            resumeScanning()
        }

        // Check and request camera permission at runtime
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            == PackageManager.PERMISSION_GRANTED
        ) {
            startScanner()
        } else {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.CAMERA),
                CAMERA_PERMISSION_CODE
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == CAMERA_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startScanner()
            } else {
                Toast.makeText(this, "Camera permission is required for QR scanning", Toast.LENGTH_LONG).show()
                finish()
            }
        }
    }

    private fun startScanner() {
        barcodeView.decodeContinuous { result ->
            if (!isProcessing) {
                val text = result.text
                if (!text.isNullOrEmpty()) {
                    isProcessing = true
                    barcodeView.pause()
                    handleScanResult(text)
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            == PackageManager.PERMISSION_GRANTED
        ) {
            barcodeView.resume()
        }
    }

    override fun onPause() {
        super.onPause()
        barcodeView.pause()
    }

    private fun handleScanResult(jsonString: String) {
        val prefs = getSharedPreferences("ZyntraPassPrefs", Context.MODE_PRIVATE)
        val eventId = prefs.getString("event_id", "") ?: ""
        val volunteerCode = prefs.getString("volunteer_code", "") ?: ""

        try {
            val payload = JSONObject(jsonString)

            val scannedEventId = payload.optString("event_id", "")
            val attendeeId = payload.optString("attendee_id", "")
            val timestamp = payload.optLong("timestamp", 0L)

            // 1. Validate QR has required fields
            if (scannedEventId.isEmpty() || attendeeId.isEmpty() || timestamp == 0L) {
                showStatus("❌ Invalid QR Format. Please try again.", false)
                return
            }

            // 2. Check event matches
            if (scannedEventId != eventId) {
                showStatus("❌ This QR is for a different event!", false)
                return
            }

            // 3. Check QR expiry — web floors timestamp to window (e.g. 60s), allow 2 full windows
            val now = System.currentTimeMillis()
            // If timestamp > now it's invalid; if more than 2 min old it's expired
            if (timestamp > now + 5000 || now - timestamp > QR_EXPIRY_MS) {
                showStatus("⏰ QR Code Expired! Ask the attendee to refresh their QR code.", false)
                return
            }

            // 4. Call Supabase RPC to mark attendance
            CoroutineScope(Dispatchers.IO).launch {
                try {
                    val rpcPayload = JSONObject().apply {
                        put("v_code", volunteerCode)
                        put("e_id", eventId)
                        put("a_id", attendeeId)
                    }

                    val res = SupabaseApi.postRpc("volunteer_scan_qr", rpcPayload)

                    withContext(Dispatchers.Main) {
                        if (res != null) {
                            // Try to parse response for more details
                            val resText = try {
                                val resObj = JSONObject(res)
                                val status = resObj.optString("status", "")
                                if (status == "already_scanned") "Already scanned today" else ""
                            } catch (e: Exception) { "" }

                            showStatus(
                                "✅ Attendee Successfully Verified!" + if (resText.isNotEmpty()) "\n($resText)" else "",
                                true
                            )
                        } else {
                            showStatus("❌ Verification failed. Already scanned or server error.", false)
                        }
                    }
                } catch (e: Exception) {
                    withContext(Dispatchers.Main) {
                        showStatus("❌ Network Error: ${e.message}", false)
                    }
                }
            }

        } catch (e: Exception) {
            showStatus("❌ Invalid QR Format. Please try again.", false)
        }
    }

    private fun showStatus(message: String, isSuccess: Boolean) {
        runOnUiThread {
            layoutStatus.visibility = View.VISIBLE
            layoutStatus.setBackgroundColor(
                if (isSuccess) Color.parseColor("#DCFCE7") else Color.parseColor("#FEE2E2")
            )
            tvStatus.text = message
            tvStatus.setTextColor(
                if (isSuccess) Color.parseColor("#166534") else Color.parseColor("#991B1B")
            )
            btnScanAnother.visibility = View.VISIBLE
        }
    }

    private fun resumeScanning() {
        isProcessing = false
        barcodeView.resume()
    }
}
