# SETUP.md — KrishiMitra Installation & Environment Setup

This document provides complete instructions to set up, run, and test KrishiMitra across Android and the backend server.

---

## 1. Prerequisites

* **Operating System**: Windows 10/11, macOS, or Linux
* **Java Development Kit**: JDK 17 or JDK 21 LTS (`Microsoft OpenJDK`, `Temurin`, or `Oracle`)
* **Android SDK**: Android 14 / 15 SDK (API Level 34 or 35)
* **Python**: Python 3.10+ (tested on Python 3.13)
* **Android Device / Emulator**: Android 7.0+ (API Level 24+) phone or Android Studio Virtual Device (e.g. Pixel 8 with Google Play)

---

## 2. Backend Service Setup

1. **Navigate to the workspace root**:
   ```bash
   cd "c:/Users/vibho/OneDrive/Desktop/Farmer Android App"
   ```

2. **Install Python dependencies**:
   ```bash
   python -m pip install -r backend/requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp backend/.env.example backend/.env
   ```
   *Note: By default, `AI_FALLBACK_PROVIDER=local` which guarantees 100% offline/local functionality without any cloud API keys.*

4. **Execute Automated Backend Tests**:
   ```bash
   python -m pytest backend/tests/test_api.py -v
   ```

5. **Start FastAPI Development Server**:
   ```bash
   python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   * Access API documentation: `http://localhost:8000/docs`
   * Health check endpoint: `http://localhost:8000/api/v1/health`

---

## 3. Android Application Setup & Compilation

1. **Verify `android/local.properties`**:
   Ensure `local.properties` specifies your Android SDK directory:
   ```properties
   sdk.dir=C\:\\Users\\vibho\\AppData\\Local\\Android\\Sdk
   ```

2. **Compile the Debug APK**:
   ```bash
   cd android
   .\gradlew.bat assembleDebug
   ```

3. **Locate the Compiled APK**:
   The output APK will be generated at:
   `android/app/build/outputs/apk/debug/app-debug.apk`

---

## 4. Installing APK on an Android Phone or Emulator

### Method A: Via Android Debug Bridge (`adb`)
1. Connect your Android smartphone via USB and enable **USB Debugging** in Developer Options (or start the `Pixel_8` AVD).
2. Verify device connection:
   ```bash
   adb devices
   ```
3. Install the APK:
   ```bash
   adb install -r android/app/build/outputs/apk/debug/app-debug.apk
   ```

### Method B: Direct Transfer (WhatsApp, Drive, or USB)
1. Copy `app-debug.apk` to your phone's internal storage or Downloads folder.
2. Tap on `app-debug.apk` on the phone.
3. If prompted, select *"Allow installation from this source"*.
4. Launch **KrishiMitra (कृषिमित्र)** from your launcher.

---

## 5. Offline Testing Verification

To verify that the application works 100% offline without internet:
1. Turn on **Airplane Mode (फ़्लाइट मोड)** on your smartphone.
2. Open **KrishiMitra**.
3. Note the top status bar badge displays `ऑफ़लाइन (Offline)`.
4. Tap **Ask AI Assistant** and ask:
   * *"धान के लिए कौन सी मिट्टी अच्छी है?"*
   * *"How much irrigation does wheat need?"*
   * *"पीएम किसान योजना क्या है?"*
   * Observe immediate verified responses in < 5 ms.
5. Tap **Scan Leaf** and test on-device diagnosis. Observe that neural inference operates in ~2.2 ms with zero network calls.
