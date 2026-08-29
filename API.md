# API.md — KrishiMitra Backend REST API Documentation

Base URL: `http://<HOST>:8000/api/v1`

Interactive Swagger Documentation: `http://localhost:8000/docs`

---

## 1. System Health
* **Endpoint**: `GET /health`
* **Response**:
```json
{
  "status": "healthy",
  "app": "KrishiMitra Backend",
  "version": "1.0.0",
  "environment": "development",
  "ai_fallback_provider": "local"
}
```

---

## 2. Agricultural Crops
* **Endpoint**: `GET /crops`
  * **Query Parameters**:
    * `category` (optional): Filter by category (e.g. `Cereals`, `Pulses`)
    * `search` (optional): Query in Hindi or English (e.g. `धान`, `Wheat`)
* **Endpoint**: `GET /crops/{crop_id}`
* **Response**:
```json
{
  "id": "rice",
  "name_en": "Rice / Paddy",
  "name_hi": "धान / चावल",
  "scientific_name": "Oryza sativa",
  "category": "Cereals",
  "category_hi": "अनाज",
  "soil": "Clayey loam, silty clay with high water retention capacity.",
  "soil_hi": "चिकनी दोमट या मटियार मिट्टी जिसमें जल धारण क्षमता अधिक हो।",
  "soil_ph": "5.5 - 6.5",
  "climate": "Hot and humid tropical / subtropical climate.",
  "climate_hi": "गर्म और आर्द्र उष्णकटिबंधीय जलवायु।",
  "temperature": "20°C - 35°C",
  "sowing_season": "Kharif (June - July)",
  "sowing_season_hi": "खरीफ (जून - जुलाई)",
  "irrigation": "Submerged conditions (2-5 cm standing water) during vegetative stage; drain before harvest.",
  "irrigation_hi": "वानस्पतिक अवस्था में 2-5 सेमी खड़ा पानी; कटाई से 10-15 दिन पहले पानी निकालें।",
  "fertilizer": "NPK ratio 120:60:40 kg/ha; Zinc Sulphate 25 kg/ha in zinc-deficient soils.",
  "fertilizer_hi": "एनपीके अनुपात 120:60:40 किग्रा/हेक्टेयर; जिंक की कमी में 25 किग्रा/हे जिंक सल्फेट।",
  "harvesting": "100 - 150 days after sowing when grains turn golden brown.",
  "harvesting_hi": "बुवाई के 100-150 दिन बाद जब बालियां सुनहरी भूरी हो जाएं।",
  "pests": "Stem borer, Brown planthopper, Leaf folder.",
  "pests_hi": "तना छेदक, भूरा फुदका, पत्ती लपेटक कीट।",
  "diseases": "Blast (Magnaporthe oryzae), Brown spot, Bacterial leaf blight.",
  "diseases_hi": "झुलसा (ब्लास्ट), भूरा धब्बा, जीवाणु झुलसा।",
  "cultivation_tips": "Use SRI (System of Rice Intensification) method for higher yield with 40% less water.",
  "cultivation_tips_hi": "कम पानी में अधिक पैदावार के लिए श्री (SRI) विधि का उपयोग करें।",
  "source": "ICAR - National Rice Research Institute (NRRI), Cuttack",
  "source_url": "https://icar-nrri.gov.in"
}
```

---

## 3. Crop Diseases
* **Endpoint**: `GET /diseases`
  * **Query Parameters**: `crop` (optional): Filter by crop name
* **Endpoint**: `GET /diseases/{disease_id}`
* **Response**:
```json
{
  "id": "rice_blast",
  "crop": "Rice",
  "crop_hi": "धान",
  "disease_name_en": "Rice Blast",
  "disease_name_hi": "धान का झुलसा रोग (ब्लास्ट)",
  "pathogen": "Magnaporthe oryzae (Fungus)",
  "symptoms_en": "Spindle-shaped spots with gray centers and brown borders...",
  "symptoms_hi": "पत्तियों पर आंख या नाव के आकार के धब्बे...",
  "treatment_organic_en": "Spray Pseudomonas fluorescens @ 10g/L...",
  "treatment_organic_hi": "स्यूडोमोनास फ्लोरेसेन्स 10 ग्राम/लीटर का छिड़काव...",
  "treatment_chemical_en": "Spray Tricyclazole 75% WP @ 0.6g/L...",
  "treatment_chemical_hi": "ट्राइसाइक्लाजोल 75% डब्लूपी @ 0.6 ग्राम/लीटर पानी में घोलकर छिड़कें...",
  "prevention_en": "Treat seeds with Carbendazim 2g/kg seed...",
  "prevention_hi": "कार्बेंडाजिम 2 ग्राम प्रति किग्रा बीज से बीजोपचार करें...",
  "confidence_threshold": 0.70
}
```

---

## 4. Government Schemes
* **Endpoint**: `GET /schemes`
* **Endpoint**: `GET /schemes/{scheme_id}`
* **Response**: Returns verified schemes including PM-KISAN, PMFBY, KCC, Soil Health Card, PMKSY, SMAM, PKVY, and PM-KMY.

---

## 5. Agricultural Loans
* **Endpoint**: `GET /loans`
* **Response**: Returns verified institutional loans including KCC Crop Loan, SBI Multi-Purpose Agri Gold Loan, NABARD AC&ABC, PNB Kisan Tatkal, and Dairy KCC.

---

## 6. Weather & Agricultural Advisory
* **Endpoint**: `GET /weather`
  * **Query Parameters**:
    * `lat` (float, default 28.6139)
    * `lon` (float, default 77.2090)
    * `district` (string, optional: `delhi`, `lucknow`, `patna`, `bhopal`, `jaipur`, `ludhiana`, `karnal`)
* **Response**:
```json
{
  "location": "Lucknow, Uttar Pradesh",
  "latitude": 26.8467,
  "longitude": 80.9462,
  "current_temperature": 29.2,
  "humidity": 68,
  "wind_speed": 11.4,
  "precipitation": 0.0,
  "weather_condition": "Clear",
  "weather_condition_hi": "साफ धूप",
  "agri_advisory": "Favorable agricultural weather. Ideal time for field weeding...",
  "agri_advisory_hi": "मौसम कृषि कार्यों के अनुकूल है...",
  "forecast": [
    {
      "date": "2026-08-30",
      "max_temp": 32.0,
      "min_temp": 24.5,
      "precipitation_prob": 20,
      "condition": "Clear",
      "condition_hi": "साफ",
      "advisory": "...",
      "advisory_hi": "..."
    }
  ],
  "source": "Open-Meteo Agricultural API (India Region)"
}
```

---

## 7. AI Query (Hybrid Fallback Gateway)
* **Endpoint**: `POST /ai/query`
* **Request Body**:
```json
{
  "query": "गेहूं के लिए कौन सी मिट्टी अच्छी है?",
  "language": "hi",
  "crop": "wheat"
}
```
* **Response**:
```json
{
  "answer": "अच्छी जल निकासी वाली उपजाऊ दोमट या मटियार दोमट मिट्टी। (उपयुक्त पीएच मान: 6.0 - 7.5)",
  "answer_hi": "अच्छी जल निकासी वाली उपजाऊ दोमट या मटियार दोमट मिट्टी। (उपयुक्त पीएच मान: 6.0 - 7.5)",
  "detected_intent": "soil",
  "confidence": 0.95,
  "is_verified_fact": true,
  "source": "ICAR - Indian Institute of Wheat and Barley Research (IIWBR), Karnal",
  "provider": "LocalVerifiedAI"
}
```

---

## 8. Mobile Database Synchronization
* **Endpoint**: `GET /sync`
* **Response**: Complete payload containing crops, diseases, schemes, and loans for mobile cache synchronization.
