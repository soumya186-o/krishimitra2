# TROUBLESHOOTING.md — Common Issues & Solutions

This document answers frequent development, installation, and runtime questions for KrishiMitra.

---

## 1. Android Build & Gradle Issues

### Error: `sdk.dir is missing in local.properties`
* **Solution**: Create or check `android/local.properties`:
  ```properties
  sdk.dir=C\:\\Users\\<YourUsername>\\AppData\\Local\\Android\\Sdk
  ```
  Ensure paths on Windows use escaped backslashes (`\\`) and colons (`\:`).

### Error: `Trailing char < > at index ...`
* **Cause**: In Windows command prompt (`cmd.exe`), `set VAR=path &&` introduces an invisible trailing whitespace into the variable.
* **Solution**: Do not pass `ANDROID_HOME` on the command line; use `android/local.properties` instead.

### Error: `OutOfMemoryError: Java heap space` during compilation
* **Solution**: Ensure `android/gradle.properties` contains adequate memory:
  ```properties
  org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
  ```

---

## 2. Model & Inference Issues

### Why is the camera saying *"छवि की गुणवत्ता अपर्याप्त है (Uncertain quality)"*?
* **Explanation**: This is a core safety feature against agricultural hallucination. If the photo is out of focus, motion-blurred, taken in pitch darkness, or pointed at soil/background, the model refuses to guess a disease.
* **Solution**: Position the phone 15-20 cm above the affected crop leaf in natural daylight and tap to focus before capturing.

### How does the offline AI work without internet?
* **Explanation**: The app embeds a pre-seeded SQLite database (`krishi_knowledge.db`) and a lightweight 1,200-token TF-IDF intent routing matrix directly in `assets/`. Queries are resolved locally in Kotlin in < 3 ms.

---

## 3. Backend & Network Issues

### Error: `Connection refused` when Android app calls `http://10.0.2.2:8000`
* **Cause**: The FastAPI backend server is not running on the host machine.
* **Solution**: In a terminal, run:
  ```bash
  python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
  ```
  * Note: `10.0.2.2` is the special alias used by the Android Emulator to reach the host's `localhost`.
  * For physical USB devices, run `adb reverse tcp:8000 tcp:8000`.

### Can I run KrishiMitra completely without starting the backend?
* **Yes!** The Android application is 100% offline-first. All core features (crop manuals, leaf disease scanner, NLP intent Q&A, government schemes, loans) execute directly on the phone from local assets. The backend server is strictly for weather synchronization and optional cloud AI fallback.

---

## 4. Audio & Voice Issues

### Speech recognition reports `ERROR_NO_MATCH` or fails to start
* **Solution**:
  1. Ensure Microphone permission is granted in Android Settings -> Apps -> KrishiMitra -> Permissions.
  2. Verify that Google Speech Recognition & Synthesis is enabled in Android system settings.
  3. Speak clearly into the microphone while keeping the button pressed.
