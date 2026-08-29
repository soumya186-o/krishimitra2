# TRAINING.md — Machine Learning Pipeline & Model Retraining

This guide explains how to generate datasets, train, evaluate, quantize, and export models for KrishiMitra.

---

## 1. Overview of On-Device ML Models

1. **Lightweight NLP Intent & Retrieval Engine**:
   * **Location**: `ml_pipeline/train_nlp.py`
   * **Output**: `ml_pipeline/output/mobile_nlp_intent_model.json` & `mobile_knowledge_index.json`
   * **Size**: ~212 KB
   * **Held-out Accuracy**: 98.95%
   * **Execution**: Runs in Kotlin on low-end Android CPU in < 3 ms without heavy external ML runtimes.

2. **Crop Disease Vision Model (MobileAgriNet)**:
   * **Location**: `ml_pipeline/train_disease.py`
   * **Architecture**: 5-Stage Depthwise-Separable Mobile CNN with Adaptive Pooling
   * **Resolution**: 224 x 224 x 3
   * **Output**: `crop_disease_model_quantized.onnx` & `crop_disease_model.onnx`
   * **Quantized Size**: 38.9 KB
   * **Latency**: 2.2 ms average on CPU
   * **Execution**: Runs via Microsoft ONNX Runtime Mobile (`com.microsoft.onnxruntime:onnxruntime-android`).

---

## 2. Step-by-Step Retraining Workflow

### Step 1: Prepare & Generate Question Variations
Aggregates verified facts from `data/verified_crops.json`, `data/verified_diseases.json`, `data/verified_schemes.json`, and `data/verified_loans.json`. Generates 1,400+ realistic farmer questions across Hindi, English, and Hinglish.
```bash
python ml_pipeline/prepare_dataset.py
```
*Output*: `data/generated_training_questions.json`

### Step 2: Train NLP Intent & Retrieval Model
Splits the dataset into an 80% training set and 20% held-out test set, fits an N-gram TF-IDF vectorizer + multiclass regularized model, evaluates precision/recall/F1, and exports the model parameters to mobile JSON format.
```bash
python ml_pipeline/train_nlp.py
```
*Output*:
* `ml_pipeline/output/mobile_nlp_intent_model.json`
* `ml_pipeline/output/mobile_knowledge_index.json`

### Step 3: Train Crop Disease Vision Model
Trains the MobileAgriNet convolutional network on the 12 Indian agricultural classes using CUDA GPU acceleration (NVIDIA RTX 4060) or CPU.
```bash
python ml_pipeline/train_disease.py
```
*Output*:
* `ml_pipeline/output/crop_disease_model.pth`
* `ml_pipeline/output/crop_disease_model.onnx`
* `ml_pipeline/output/disease_labels.txt`

### Step 4: Quantize & Benchmark
Performs post-training dynamic INT8/UINT8 weight quantization on the ONNX model, measures latency over 50 inference iterations, and generates `BENCHMARK_REPORT.md`.
```bash
python ml_pipeline/export_quantize.py
```
*Output*:
* `ml_pipeline/output/crop_disease_model_quantized.onnx`
* `BENCHMARK_REPORT.md`

### Step 5: Deploy Assets to Android Application
Creates the pre-seeded SQLite database `krishi_knowledge.db` (1.16 MB) and deploys all trained models and vocabularies directly to `android/app/src/main/assets/`.
```bash
python ml_pipeline/generate_android_assets.py
```

---

## 3. Adding New Crops or Diseases

1. Add the crop entry to `data/verified_crops.json` with official ICAR parameters.
2. Add any associated disease classes to `data/verified_diseases.json`.
3. Re-run the 5 pipeline commands listed above.
4. Recompile the Android debug APK:
   ```bash
   cd android && .\gradlew.bat assembleDebug
   ```
The updated knowledge base and models will be instantly embedded into the new APK.
