# TESTING.md — Comprehensive Test Plan & Verification Results

This document provides testing procedures, automated test commands, and manual verification protocols for KrishiMitra.

---

## 1. Automated Test Execution

### A. Backend API & Hybrid Provider Tests
The backend test suite verifies:
* `/health`: System health and configuration
* `/crops`: Retrieval and query filters
* `/schemes`: Government schemes listing
* `/loans`: Institutional credit schemes
* `/weather`: Live weather API and offline fallback
* `/ai/query`: Hindi and English verified knowledge routing
* `/sync`: Full database synchronization schema

**Run Command**:
```bash
python -m pytest backend/tests/test_api.py -v
```
**Result**:
* 9/9 Tests Passed (100% pass rate) in 1.94 seconds.

### B. Machine Learning Intent & Vision Model Tests
* **NLP Model**: Evaluated on a 20% held-out test split (285 test queries).
  * Overall Intent Accuracy: **98.95%**
  * Precision: 0.99
  * Recall: 0.99
  * F1-Score: 0.99
* **Crop Disease Model (MobileAgriNet)**:
  * Evaluated on held-out leaf validation set across 12 classes
  * Validation Accuracy: **83.33%**
  * Inference Latency: **2.23 ms** average on CPU
  * Quantized Model Size: **38.96 KB**

### C. Android Unit Tests
The Android test suite in `android/app/src/test/java/com/krishimitra/app/NLPAndModelUnitTest.kt` verifies:
* Crop alias detection in Hindi and English
* Agricultural intent keyword heuristics
* Confidence threshold boundaries (Certainty ≥ 0.70, Uncertainty < 0.50)

**Run Command**:
```bash
cd android
.\gradlew.bat testDebugUnitTest
```

---

## 2. Manual End-to-End Testing Protocols

### Protocol 1: Offline Knowledge Retrieval & Airplane Mode Test
1. Disconnect WiFi and cellular data (enable Airplane mode).
2. Launch KrishiMitra. Verify the persistent top status badge reads `ऑफ़लाइन (Offline)`.
3. Open the **Ask AI Assistant** tab.
4. Type or hold-to-talk: *"धान के लिए कौन सी मिट्टी अच्छी है?"*
5. **Expected Result**: Immediate verified response:
   *"धान के लिए चिकनी दोमट या मटियार मिट्टी जिसमें जल धारण क्षमता अधिक हो। (उपयुक्त पीएच मान: 5.5 - 6.5)"*
   Response latency < 5 ms with source badge: *भाकृअनुप (ICAR) राष्ट्रीय चावल अनुसंधान संस्थान*.
6. Tap the Speaker icon to verify local bilingual Text-to-Speech synthesis.

### Protocol 2: Camera Crop Disease Detection & Uncertainty Guardrail
1. Open the **Scan Leaf** tab.
2. Frame a leaf inside the green alignment box.
3. Test 1 (Blight/Blast Leaf): Tap **Analyze Leaf**.
   * **Expected Result**: Displays *धान का झुलसा रोग (Rice Blast)* or *अगेती झुलसा*, 80%+ confidence, observed symptoms, organic remedy (Pseudomonas / Neem), and verified chemical remedy (Tricyclazole 75% WP @ 0.6g/L).
4. Test 2 (Blurred / Low-Light Photo): Capture an out-of-focus background.
   * **Expected Result**: Displays warning card: *"छवि की गुणवत्ता अपर्याप्त है। कृपया साफ रोशनी में दोबारा फोटो लें।"* Prevents hallucination or forced chemical recommendation.

### Protocol 3: Agricultural Weather & Practical Advisory
1. Open the **Weather** tab.
2. Select **Lucknow** from the horizontal district selector.
3. **Expected Result**: Displays current temperature, humidity, wind speed, rain probability, and actionable advice (e.g. *"मौसम कृषि कार्यों के अनुकूल है"*) followed by the 5-day forecast.

### Protocol 4: Government Schemes & Loan Verification
1. Open **Schemes** and search *"फसल बीमा"*.
2. Verify **PMFBY** card appears with verified premium breakdown (2% Kharif, 1.5% Rabi).
3. Tap **Open Official Portal**; verify it prompts browser opening to `https://pmfby.gov.in`.
4. Open **Loans** and verify **KCC Crop Loan** with 4% effective interest rate.
