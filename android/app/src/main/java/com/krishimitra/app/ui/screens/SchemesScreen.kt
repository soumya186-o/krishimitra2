package com.krishimitra.app.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.krishimitra.app.R
import com.krishimitra.app.data.local.DatabaseHelper
import com.krishimitra.app.domain.model.Scheme
import com.krishimitra.app.ui.theme.*

@Composable
fun SchemesScreen(dbHelper: DatabaseHelper) {
    val context = LocalContext.current
    var searchQuery by remember { mutableStateOf("") }
    val allSchemes = remember { dbHelper.getAllSchemes() }

    val filteredSchemes = remember(searchQuery, allSchemes) {
        if (searchQuery.isBlank()) allSchemes
        else allSchemes.filter {
            it.nameHi.contains(searchQuery, ignoreCase = true) ||
            it.nameEn.contains(searchQuery, ignoreCase = true) ||
            (it.categoryHi?.contains(searchQuery, ignoreCase = true) == true)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(BackgroundLight)
            .padding(16.dp)
    ) {
        // Search bar
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 14.dp),
            placeholder = { Text("सरकारी योजना खोजें…", fontSize = 14.sp) },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
            shape = RoundedCornerShape(14.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = GreenPrimary,
                unfocusedBorderColor = CardBorder,
                focusedContainerColor = Color.White,
                unfocusedContainerColor = Color.White
            )
        )

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(14.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(filteredSchemes) { scheme ->
                SchemeCard(scheme = scheme, onOpenPortal = {
                    scheme.officialUrl?.let { url ->
                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                        context.startActivity(intent)
                    }
                })
            }
        }
    }
}

@Composable
fun SchemeCard(scheme: Scheme, onOpenPortal: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Category Badge
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    shape = RoundedCornerShape(6.dp),
                    color = Color(0xFFEDE7F6)
                ) {
                    Text(
                        text = scheme.categoryHi ?: "सरकारी योजना",
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = Color(0xFF512DA8),
                            fontWeight = FontWeight.Bold,
                            fontSize = 11.sp
                        )
                    )
                }

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.Verified,
                        contentDescription = null,
                        tint = GreenPrimary,
                        modifier = Modifier.size(13.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "सत्यापित",
                        color = GreenPrimary,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Scheme Name
            Text(
                text = scheme.nameHi,
                style = MaterialTheme.typography.titleMedium.copy(
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary
                )
            )
            Text(
                text = scheme.nameEn,
                style = MaterialTheme.typography.bodySmall.copy(
                    color = TextSecondary,
                    fontSize = 12.sp
                )
            )

            Spacer(modifier = Modifier.height(10.dp))
            Divider(color = Color(0xFFF0F0F0), thickness = 0.8.dp)
            Spacer(modifier = Modifier.height(10.dp))

            // Benefits
            Text(
                text = "योजना के लाभ:",
                style = MaterialTheme.typography.labelMedium.copy(
                    fontWeight = FontWeight.Bold,
                    color = GreenPrimary
                )
            )
            Text(
                text = scheme.benefitsHi ?: "",
                style = MaterialTheme.typography.bodyMedium.copy(
                    color = TextPrimary,
                    fontSize = 13.sp,
                    lineHeight = 19.sp
                )
            )

            Spacer(modifier = Modifier.height(8.dp))

            // Eligibility
            Text(
                text = "पात्रता:",
                style = MaterialTheme.typography.labelMedium.copy(
                    fontWeight = FontWeight.Bold,
                    color = AmberSecondary
                )
            )
            Text(
                text = scheme.eligibilityHi ?: "",
                style = MaterialTheme.typography.bodySmall.copy(
                    color = TextSecondary,
                    lineHeight = 18.sp
                )
            )

            Spacer(modifier = Modifier.height(12.dp))

            // Application Link Button
            Button(
                onClick = onOpenPortal,
                shape = RoundedCornerShape(10.dp),
                colors = ButtonDefaults.buttonColors(containerColor = GreenPrimary),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(
                    imageVector = Icons.Default.OpenInNew,
                    contentDescription = null,
                    modifier = Modifier.size(16.dp)
                )
                Spacer(modifier = Modifier.width(6.dp))
                Text("आधिकारिक पोर्टल पर आवेदन करें", fontSize = 13.sp)
            }
        }
    }
}
