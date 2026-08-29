package com.krishimitra.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.krishimitra.app.R
import com.krishimitra.app.data.remote.ApiClient
import com.krishimitra.app.domain.model.WeatherDayForecast
import com.krishimitra.app.domain.model.WeatherInfo
import com.krishimitra.app.ui.theme.*
import kotlinx.coroutines.launch

@Composable
fun WeatherScreen(apiClient: ApiClient) {
    val coroutineScope = rememberCoroutineScope()
    var selectedDistrict by remember { mutableStateOf("delhi") }
    var isLoading by remember { mutableStateOf(false) }

    val districts = listOf(
        "delhi" to "दिल्ली (Delhi)",
        "lucknow" to "लखनऊ (Lucknow)",
        "patna" to "पटना (Patna)",
        "bhopal" to "भोपाल (Bhopal)",
        "jaipur" to "जयपुर (Jaipur)",
        "ludhiana" to "लुधियाना (Ludhiana)",
        "karnal" to "करनाल (Karnal)"
    )

    var weatherData by remember {
        mutableStateOf(
            WeatherInfo(
                location = "दिल्ली / उत्तर भारत",
                temperature = 28.5f,
                humidity = 64,
                windSpeed = 12.0f,
                rainfallProb = 15,
                condition = "Clear",
                conditionHi = "साफ धूप",
                advisoryEn = "Favorable agricultural weather. Ideal time for field weeding and scheduled irrigation.",
                advisoryHi = "मौसम कृषि कार्यों के अनुकूल है। खेत की तैयारी, निराई-गुड़ाई और सिंचाई हेतु उपयुक्त समय है।",
                forecast = listOf(
                    WeatherDayForecast("आज", 30f, 22f, 10, "साफ", "सामान्य कृषि कार्य जारी रखें।"),
                    WeatherDayForecast("कल", 31f, 23f, 15, "साफ धूप", "शाम को हल्की सिंचाई करें।"),
                    WeatherDayForecast("परसों", 29f, 21f, 40, "हल्के बादल", "दवा छिड़काव से पहले मौसम देखें।"),
                    WeatherDayForecast("दिन 4", 27f, 20f, 65, "वर्षा संभावना", "आज भारी सिंचाई और कीटनाशक छिड़काव स्थगित रखें।"),
                    WeatherDayForecast("दिन 5", 28f, 20f, 30, "सामान्य", "जलभराव न होने दें।")
                ),
                isOffline = false
            )
        )
    }

    fun loadWeather(district: String) {
        isLoading = true
        selectedDistrict = district
        coroutineScope.launch {
            val res = apiClient.fetchWeather(28.6139, 77.2090, district)
            if (res != null) {
                weatherData = res
            }
            isLoading = false
        }
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(BackgroundLight)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // District Selector Chips
        item {
            Column {
                Text(
                    text = stringResource(R.string.select_district),
                    style = MaterialTheme.typography.labelLarge.copy(
                        fontWeight = FontWeight.SemiBold,
                        color = TextPrimary
                    )
                )
                Spacer(modifier = Modifier.height(8.dp))
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(districts) { (key, name) ->
                        val isSelected = selectedDistrict == key
                        Surface(
                            modifier = Modifier.clickable { loadWeather(key) },
                            shape = RoundedCornerShape(20.dp),
                            color = if (isSelected) GreenPrimary else Color.White,
                            border = if (isSelected) null else androidx.compose.foundation.BorderStroke(1.dp, CardBorder)
                        ) {
                            Text(
                                text = name,
                                modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
                                style = MaterialTheme.typography.labelMedium.copy(
                                    color = if (isSelected) Color.White else TextPrimary,
                                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                                )
                            )
                        }
                    }
                }
            }
        }

        // Current Weather Card
        item {
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(18.dp),
                elevation = CardDefaults.cardElevation(3.dp)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(
                            Brush.verticalGradient(
                                listOf(Color(0xFF0277BD), Color(0xFF01579B))
                            )
                        )
                        .padding(20.dp)
                ) {
                    Column {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(
                                    text = weatherData.location,
                                    color = Color.White,
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Text(
                                    text = weatherData.conditionHi,
                                    color = Color(0xFFB3E5FC),
                                    fontSize = 14.sp
                                )
                            }
                            Text(
                                text = "${weatherData.temperature.toInt()}°C",
                                color = Color.White,
                                fontSize = 42.sp,
                                fontWeight = FontWeight.ExtraBold
                            )
                        }

                        Spacer(modifier = Modifier.height(20.dp))
                        Divider(color = Color(0x33FFFFFF), thickness = 1.dp)
                        Spacer(modifier = Modifier.height(16.dp))

                        // Stats Grid (Humidity, Wind, Rain)
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            WeatherStatItem(
                                icon = Icons.Default.WaterDrop,
                                label = "नमी",
                                value = "${weatherData.humidity}%"
                            )
                            WeatherStatItem(
                                icon = Icons.Default.Air,
                                label = "हवा की गति",
                                value = "${weatherData.windSpeed} किमी/घंटा"
                            )
                            WeatherStatItem(
                                icon = Icons.Default.Umbrella,
                                label = "बारिश संभावना",
                                value = "${weatherData.rainfallProb}%"
                            )
                        }
                    }
                }
            }
        }

        // Agricultural Advisory Card
        item {
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF8E1)),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Default.TipsAndUpdates,
                            contentDescription = null,
                            tint = WarningOrange,
                            modifier = Modifier.size(24.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = stringResource(R.string.weather_advisory_heading),
                            style = MaterialTheme.typography.titleMedium.copy(
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFFE65100)
                            )
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = weatherData.advisoryHi,
                        style = MaterialTheme.typography.bodyMedium.copy(
                            color = Color(0xFF4E342E),
                            lineHeight = 22.sp
                        )
                    )
                }
            }
        }

        // 5-Day Forecast List
        item {
            Text(
                text = stringResource(R.string.weather_forecast_heading),
                style = MaterialTheme.typography.titleLarge.copy(
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary
                )
            )
        }

        items(weatherData.forecast) { day ->
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(1.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = day.date,
                            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold)
                        )
                        Text(
                            text = day.conditionHi,
                            style = MaterialTheme.typography.bodySmall.copy(color = TextSecondary)
                        )
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            text = day.advisoryHi,
                            style = MaterialTheme.typography.bodySmall.copy(color = GreenPrimary, fontSize = 11.sp),
                            maxLines = 1
                        )
                    }

                    Column(horizontalAlignment = Alignment.End) {
                        Text(
                            text = "${day.maxTemp.toInt()}° / ${day.minTemp.toInt()}°C",
                            style = MaterialTheme.typography.titleMedium.copy(
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        )
                        Text(
                            text = "बारिश: ${day.rainProb}%",
                            style = MaterialTheme.typography.bodySmall.copy(
                                color = if (day.rainProb > 50) AlertRed else TextSecondary,
                                fontWeight = if (day.rainProb > 50) FontWeight.Bold else FontWeight.Normal
                            )
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun WeatherStatItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = Color(0xFFB3E5FC),
            modifier = Modifier.size(20.dp)
        )
        Spacer(modifier = Modifier.height(4.dp))
        Text(text = label, color = Color(0xFFE1F5FE), fontSize = 11.sp)
        Text(text = value, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold)
    }
}
