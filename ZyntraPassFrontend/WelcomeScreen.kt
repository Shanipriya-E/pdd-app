import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview

@Composable
fun WelcomeScreen() {
    // Gradient Background
    val backgroundBrush = Brush.linearGradient(
        colors = listOf(
            Color(0xFF1C3C75), // Top gradient color
            Color(0xFF0D162A), // Middle
            Color(0xFF070914)  // Bottom
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundBrush)
            .padding(24.dp)
    ) {
        // Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 16.dp, bottom = 60.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "ZyntraPass",
                color = Color.White,
                fontSize = 20.sp,
                fontWeight = FontWeight.ExtraBold
            )
            
            Button(
                onClick = { /* TODO: Create Account */ },
                colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
            ) {
                Text(
                    text = "Create account",
                    color = Color(0xFF0D162A),
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 14.sp
                )
            }
        }

        // Main Content
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = "One Platform.\nEvery Event. Every\nCertificate.",
                color = Color.White,
                fontSize = 40.sp,
                fontWeight = FontWeight.ExtraBold,
                lineHeight = 44.sp,
                modifier = Modifier.padding(bottom = 24.dp)
            )

            Text(
                text = "Discover events, register instantly, track attendance, connect with people who share your interests, and keep every certificate in one place.",
                color = Color(0xFFA8B2D1),
                fontSize = 16.sp,
                lineHeight = 24.sp,
                modifier = Modifier.padding(bottom = 40.dp)
            )

            // Action Buttons
            Button(
                onClick = { /* TODO: Explore Events */ },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5B54E3)),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .padding(bottom = 16.dp)
                    .height(50.dp)
            ) {
                Text("Explore Events", fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
            }

            OutlinedButton(
                onClick = { /* TODO: Organize Event */ },
                colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.White),
                border = null,
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .height(50.dp)
                    .background(Color(0x0DFFFFFF), RoundedCornerShape(12.dp))
                    .border(1.dp, Color(0xFF3C4260), RoundedCornerShape(12.dp))
            ) {
                Text("Organize an Event", fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
            }
        }

        // Footer / Stats
        Divider(color = Color(0x1AFFFFFF), thickness = 1.dp, modifier = Modifier.padding(bottom = 32.dp))
        
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 32.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            StatItem("1,842", "Events hosted")
            StatItem("96.4%", "Verified\nattendance")
            StatItem("74k", "Certificates\nissued")
        }
    }
}

@Composable
fun StatItem(value: String, label: String) {
    Column {
        Text(
            text = value,
            color = Color.White,
            fontSize = 24.sp,
            fontWeight = FontWeight.ExtraBold,
            modifier = Modifier.padding(bottom = 4.dp)
        )
        Text(
            text = label,
            color = Color(0xFFA8B2D1),
            fontSize = 13.sp,
            lineHeight = 18.sp
        )
    }
}

@Preview(showBackground = true)
@Composable
fun WelcomeScreenPreview() {
    WelcomeScreen()
}
