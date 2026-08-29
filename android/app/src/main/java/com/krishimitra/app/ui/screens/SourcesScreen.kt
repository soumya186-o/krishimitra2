package com.krishimitra.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.krishimitra.app.R
import com.krishimitra.app.ui.theme.*

@Composable
fun SourcesScreen() {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(BackgroundLight)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item {
            Card(
                shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "परियोजना परिचय एवं उद्देश्य",
                        style = MaterialTheme.typography.titleLarge.copy(
                            fontWeight = FontWeight.Bold,
                            color = GreenPrimary
                        )
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "कृषिमित्र (KrishiMitra) भारतीय किसानों के लिए विशेष रूप से विकसित एक स्मार्ट, विश्वसनीय और पूर्णतः ऑफ़लाइन-सक्षम कृषि सहायक है। इसका मुख्य उद्देश्य छोटे और सीमांत किसानों को बिना इंटरनेट के भी प्रमाणित वैज्ञानिक खेती, रोग निदान और सरकारी योजनाओं की सटीक जानकारी प्रदान करना है।",
                        style = MaterialTheme.typography.bodyMedium.copy(lineHeight = 22.sp)
                    )
                }
            }
        }

        item {
            Card(
                shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "प्रमाणित सरकारी एवं वैज्ञानिक स्रोत (Attribution)",
                        style = MaterialTheme.typography.titleMedium.copy(
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                    )
                    Spacer(modifier = Modifier.height(10.dp))

                    SourceItem(
                        org = "भाकृअनुप (ICAR) एवं केंद्रीय कृषि अनुसंधान संस्थान",
                        details = "फसल पद्धतियां, उपयुक्त मिट्टी, बीज दर, एनपीके उर्वरक मात्रा, कीट व रोग प्रबंधन।"
                    )
                    SourceItem(
                        org = "कृषि एवं किसान कल्याण मंत्रालय, भारत सरकार",
                        details = "पीएम किसान (PM-KISAN), प्रधानमंत्री फसल बीमा योजना (PMFBY), मृदा स्वास्थ्य कार्ड योजना (SHC)।"
                    )
                    SourceItem(
                        org = "नाबार्ड (NABARD) एवं भारतीय रिज़र्व बैंक (RBI)",
                        details = "किसान क्रेडिट कार्ड (KCC) दिशा-निर्देश, रियायती कृषि ब्याज दरें एवं ऋण पात्रता मानदंड।"
                    )
                    SourceItem(
                        org = "ओपन-मेटियो (Open-Meteo) एवं क्षेत्रीय मौसम मॉडल",
                        details = "उच्च परिशुद्धता कृषि मौसम पूर्वानुमान एवं सामयिक वर्षा व तापमान चेतावनी।"
                    )
                }
            }
        }

        item {
            Card(
                shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF3E0)),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.Top) {
                    Icon(
                        imageVector = Icons.Default.Shield,
                        contentDescription = null,
                        tint = WarningOrange,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Column {
                        Text(
                            text = "कृषि सुरक्षा एवं सत्यनिष्ठा नीति",
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFFE65100),
                            fontSize = 14.sp
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "कृषिमित्र कभी भी मनगढ़ंत कीटनाशक, गैर-प्रमाणित खुराक या काल्पनिक सरकारी योजनाएं नहीं बताता। किसी भी गंभीर फसल समस्या में स्थानीय कृषि विज्ञान केंद्र (KVK) अथवा किसान कॉल सेंटर (1800-180-1551) से परामर्श अवश्य लें।",
                            color = Color(0xFF5D4037),
                            fontSize = 12.sp,
                            lineHeight = 18.sp
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun SourceItem(org: String, details: String) {
    Column(modifier = Modifier.padding(vertical = 6.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(
                imageVector = Icons.Default.CheckCircle,
                contentDescription = null,
                tint = GreenPrimary,
                modifier = Modifier.size(16.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = org,
                style = MaterialTheme.typography.labelMedium.copy(
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary
                )
            )
        }
        Text(
            text = details,
            style = MaterialTheme.typography.bodySmall.copy(
                color = TextSecondary,
                lineHeight = 18.sp
            ),
            modifier = Modifier.padding(start = 22.dp)
        )
    }
}
