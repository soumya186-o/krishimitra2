# KrishiMitra (कृषिमित्र) — AI-Powered Smart Agriculture Assistant

> **"आपका डिजिटल कृषि साथी — Your Intelligent Farming Companion"**

KrishiMitra is a production-grade, offline-first Android application and accompanying backend/ML system specifically engineered for Indian farmers. It bridges the critical agricultural advisory gap for rural smallholders and marginal farmers operating budget Android smartphones with limited RAM, weak CPUs, and intermittent or absent internet connectivity.

---

## 🌟 Key Capabilities

* **🌱 On-Device Agriculture AI (100% Offline Primary)**:
  * Fast (< 3 ms) natural language intent classification and semantic retrieval over a verified database of 15 major Indian crops.
  * Responds directly in clear, conversational **Hindi** or **English**.
  * Zero hallucinations: never fabricates chemicals, dosages, or schemes.
* **🔬 Quantized Crop Disease Scanner (Offline Computer Vision)**:
  * Camera leaf viewfinder with edge-framing assistance.
  * Quantized on-device neural classifier (38.9 KB, 2.2 ms latency) targeting 12 Indian agricultural classes: *Rice Blast, Rice Brown Spot, Wheat Yellow Rust, Wheat Loose Smut, Cotton Blight, Potato Early/Late Blights, Tomato Blights, Healthy Leaf, Soil, and Blurred/Uncertain*.
  * Provides observed symptoms, organic/IPM remedies, verified ICAR chemical dosages, and prevention rules.
* **🎙️ Hold-to-Talk Voice Assistant**:
  * Farmer-friendly voice interaction: press and hold the mic to speak, release to send.
  * Bilingual speech recognition with automatic language mode (Auto, Hindi, English).
  * Natural Text-to-Speech playback of every AI response for low-literacy accessibility.
* **🌦️ Actionable Agricultural Weather**:
  * Live localized temperature, humidity, wind, and rain probabilities.
  * Actionable farmer-oriented advisories (e.g., *"कल भारी बारिश का अनुमान है, आज सिंचाई व कीटनाशक छिड़काव स्थगित रखें"*).
  * Manual district switcher with offline regional climatological baseline.
* **🏛️ Verified Government Schemes & Loans**:
  * Complete, non-fabricated criteria for PM-KISAN, PMFBY, KCC, Soil Health Card, PMKSY, SMAM, PKVY, and Animal Husbandry KCC.
  * Direct intent links to official government portals (`pmkisan.gov.in`, `pmfby.gov.in`, etc.).
* **🔄 Offline-First Hybrid Architecture**:
  * Pre-seeded Room SQLite database (`krishi_knowledge.db`, 1.16 MB) pre-packaged inside the APK.
  * Automatic network detection: transparently falls back to cloud AI (FastAPI / Gemini / OpenAI) only when online and local confidence is low.

---

## 📱 Repository Structure

```
├── android/                         # Complete Jetpack Compose Android Application
│   ├── app/src/main/
│   │   ├── java/com/krishimitra/app/ # Clean Architecture (UI, Domain, Data, ML, Voice)
│   │   ├── assets/                 # Pre-seeded SQLite DB, ONNX Vision Model, NLP vocab
│   │   └── res/                    # Full English & Hindi-first Localization (values & values-hi)
│   └── build.gradle.kts            # Modern Kotlin 2.0 & AGP 8.7+ configuration
├── backend/                        # Production-grade Python FastAPI service
│   ├── app/                        # REST APIs, SQLAlchemy models, AI provider abstraction
│   ├── tests/                      # Pytest automated test suite
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Backend environment configuration
├── data/                           # Verified ICAR, Ministry & Banking Seed Datasets
│   ├── verified_crops.json         # 15 Indian crops with agronomic parameters
│   ├── verified_diseases.json      # 12 disease classes with symptoms and treatments
│   ├── verified_schemes.json       # Central & State agricultural schemes
│   └── verified_loans.json         # Institutional farm loan terms
├── ml_pipeline/                    # Reproducible ML & Quantization Pipeline
│   ├── prepare_dataset.py          # Generates 1,400+ realistic farmer query variations
│   ├── train_nlp.py                # Trains intent model & exports mobile vocab
│   ├── train_disease.py            # MobileAgriNet CNN trainer (CUDA RTX 4060 / CPU)
│   ├── export_quantize.py          # INT8 / UINT8 mobile quantization & benchmarks
│   └── generate_android_assets.py  # Generates SQLite DB & deploys mobile assets
├── BENCHMARK_REPORT.md             # Model latency, RAM, and size benchmarks
├── README.md                       # Main project overview
├── SETUP.md                        # Quickstart setup instructions
├── TRAINING.md                     # Model training & updating instructions
├── ARCHITECTURE.md                 # Technical architecture deep dive
├── API.md                          # REST API documentation
├── DATA_SOURCES.md                 # Government & ICAR provenance attribution
├── TESTING.md                      # Comprehensive test plan & results
└── TROUBLESHOOTING.md              # Common setup questions and answers
```

---

## 🚀 Quickstart & Verification

### 1. Backend Service
```bash
python -m pip install -r backend/requirements.txt
python -m pytest backend/tests/test_api.py -v
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Visit API docs at `http://localhost:8000/docs`.

### 2. Retraining & Quantizing ML Models
```bash
python ml_pipeline/prepare_dataset.py
python ml_pipeline/train_nlp.py
python ml_pipeline/train_disease.py
python ml_pipeline/export_quantize.py
python ml_pipeline/generate_android_assets.py
```

### 3. Android APK Compilation
```bash
cd android
gradlew.bat assembleDebug
```
The compiled debug APK is located at:
`android/app/build/outputs/apk/debug/app-debug.apk`

---

## 👥 Contributors & SIH Attribution
Developed for the **Smart India Hackathon (SIH) Student Innovation Project** under the Agriculture, Food Tech & Rural Development theme.
