# PROJECT_ANALYSIS.md — KrishiMitra (कृषिमित्र) AI Agriculture Assistant

## 1. Executive Summary & Environment Assessment

An exhaustive inspection of the host system and workspace was conducted prior to code implementation.

### System Diagnostics
* **Operating System**: Windows 11 (AMD64)
* **CPU**: Intel Core Ultra 7 155H
* **GPU**: NVIDIA GeForce RTX 4060 Laptop GPU (8GB GDDR6 VRAM, CUDA Driver 13.3, SMI 610.62)
* **System RAM**: 16 GB
* **Java Development Kit**: Microsoft OpenJDK 21.0.12.8 LTS (`C:\Program Files\Microsoft\jdk-21.0.12.8-hotspot\bin\javac.exe`)
* **Android SDK**: Present at `C:\Users\vibho\AppData\Local\Android\Sdk`
  * Platforms available: `android-37.0` (API 35/36/37 compatible)
  * Build Tools: `36.0.0`
  * Platform Tools: `adb.exe` operational
  * Emulator & AVD: `Pixel_8` AVD configured
  * Android Studio: Installed with plugins and JetBrains Runtime at `C:\Program Files\Android\Android Studio`
* **Gradle**: Gradle 9.5.0 binary and cache present at `C:\Users\vibho\.gradle\wrapper\dists`
* **Python Environment**:
  * Python 3.13.14 (Active in PATH) & Python 3.14
  * Pre-installed packages: `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `httpx`, `pillow`, `pytest`, `python-dotenv`
  * Machine learning packages ready for installation via standard wheels: `numpy`, `scikit-learn`, `scipy`, `onnx`, `onnxruntime`, `torch`, `torchvision`
* **Existing Project Files**: Workspace was initialized clean (`c:\Users\vibho\OneDrive\Desktop\Farmer Android App`).

---

## 2. Product Identity & Branding

* **Selected Brand Name**: **KrishiMitra (कृषिमित्र)**
* **Tagline**: "आपका डिजिटल कृषि साथी — Your Intelligent Farming Companion"
* **Target Audience**: Indian smallholder and marginal farmers, agricultural extension workers, and rural youth operating budget Android smartphones (2GB–4GB RAM, weak 4G/2G, intermittent connectivity).
* **Design Philosophy**: High-contrast, touch-friendly UI, Hindi-first bilingual architecture, zero unnecessary visual bloat, instant offline responsiveness (< 25ms NLP, < 75ms vision inference).

---

## 3. Detected Requirements vs. Architecture Matrix

| Requirement | Proposed Architecture Component | Offline / Online Strategy |
| :--- | :--- | :--- |
| **Agricultural Q&A** | Room DB + On-device NLP Intent Engine + TF-IDF Vectorizer | **100% Offline Primary**; FastAPI Cloud AI Fallback when online & low confidence |
| **Crop Disease Vision** | CameraX + Quantized MobileNetV2/V3 TFLite Model (12 Major Indian Crop Diseases) | **100% Offline** (On-device neural inference) |
| **Voice Assistant** | Hold-to-Talk + Android Native SpeechRecognizer + TTS Engine | **Hybrid**: Native offline STT/TTS with backend Whisper/TTS API fallback |
| **Government Schemes** | Room DB + Backend Sync API (`/schemes`) | **Offline Cached** with verified provenance (PM-KISAN, PMFBY, KCC, etc.) |
| **Agri Loans** | Room DB + Backend Sync API (`/loans`) | **Offline Cached** with verified criteria (KCC, NABARD, Gold Loans) |
| **Weather & Agri Advisory** | Open-Meteo / IMD Weather Service + Local Rule Advisory Engine | Cached offline with GPS & manual district selector |
| **Synchronization** | Differential REST Sync Engine (`/sync`) | Auto-detects connectivity; syncs latest schemes, crops, and advisory |

---

## 4. Key Subsystem Design

### Subsystem 1: Android Application (`android/`)
* **Language & UI**: Kotlin 2.1+, Jetpack Compose, Material 3, Accompanist, Navigation Compose.
* **Architecture**: Clean Architecture + MVVM (Model-View-ViewModel) with StateFlow.
* **Local Persistence**: Room SQLite Database preloaded with verified agricultural facts, crops, schemes, and loans from assets.
* **Hardware Interop**: CameraX with custom Leaf Viewfinder, Android SpeechRecognizer, TextToSpeech, FusedLocationProviderClient with manual district fallback.
* **Localization**: Complete string externalization in English (`values/strings.xml`) and Hindi (`values-hi/strings.xml`).

### Subsystem 2: Offline ML & NLP Pipeline (`ml_pipeline/`)
* **Intent & Retrieval Model**: Dual-stage lightweight pipeline:
  1. Agriculture domain intent & crop entity classifier (Cereals, Pulses, Soil, Irrigation, Pests, Schemes, Loans).
  2. N-gram TF-IDF cosine similarity search over local Room knowledge database.
  3. Latency: < 15ms on low-end ARM Cortex-A53 / A55 CPUs.
* **Crop Disease Vision Model**:
  1. 12 Indian agricultural classes: Rice Blast, Rice Brown Spot, Wheat Rust, Wheat Loose Smut, Cotton Bacterial Blight, Potato Early Blight, Potato Late Blight, Tomato Early Blight, Tomato Leaf Mold, Healthy Leaf, Soil/Background, Low Quality/Uncertain.
  2. Quantized to INT8/FP16 TFLite (< 4MB file size).
  3. Preprocessing: 224x224 normalization, fast TensorBuffer inference.

### Subsystem 3: Backend API Server (`backend/`)
* **Framework**: FastAPI (Python 3.13) with asynchronous endpoints.
* **Database**: SQLite / PostgreSQL with SQLAlchemy 2.0 ORM.
* **Cloud AI Fallback**: `AIProvider` interface with `LocalFallbackProvider`, `OpenAICompatibleProvider`, and `GeminiProvider` support.
* **Sync & Seed**: Endpoints for full data updates, schema versions, and knowledge attribution.

---

## 5. Phased Implementation Sequence

1. **Phase 1: Environment & Project Analysis** *(Completed)*
2. **Phase 2: Android Project Foundation & Gradle Configuration**
3. **Phase 3: Localization Architecture (Hindi & English)**
4. **Phase 4: Verified Agricultural Datasets & Generation Pipeline**
5. **Phase 5: Offline Room Database & Seed Loading**
6. **Phase 6: Lightweight NLP Intent & Retrieval Engine**
7. **Phase 7: Crop Disease Computer Vision Model Training & Quantization**
8. **Phase 8: CameraX & On-Device Vision Integration**
9. **Phase 9: Voice Assistant Pipeline (Hold-to-Talk)**
10. **Phase 10: Weather & Agri-Advisory Engine**
11. **Phase 11: Government Schemes & Loan Information Hub**
12. **Phase 12: Backend FastAPI Server & Cloud AI Fallback**
13. **Phase 13: Offline Data Synchronization**
14. **Phase 14: Comprehensive Verification, Testing & Debug APK Build**
15. **Phase 15: Documentation Suite & Delivery**
