"""
generate_android_assets.py
Generates the pre-seeded Room SQLite database and copies all mobile ML models,
labels, and knowledge indices into android/app/src/main/assets/.
"""

import os
import json
import sqlite3
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
ML_OUTPUT_DIR = os.path.join(ROOT_DIR, "ml_pipeline", "output")
ANDROID_ASSETS_DIR = os.path.join(ROOT_DIR, "android", "app", "src", "main", "assets")

def create_preseeded_sqlite_db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Room master table is created automatically by Room, but standard tables must match entity schema
    cur.execute("""
    CREATE TABLE IF NOT EXISTS crops (
        id TEXT PRIMARY KEY NOT NULL,
        name_en TEXT NOT NULL,
        name_hi TEXT NOT NULL,
        scientific_name TEXT,
        category TEXT,
        category_hi TEXT,
        soil TEXT,
        soil_hi TEXT,
        soil_ph TEXT,
        climate TEXT,
        climate_hi TEXT,
        temperature TEXT,
        sowing_season TEXT,
        sowing_season_hi TEXT,
        irrigation TEXT,
        irrigation_hi TEXT,
        fertilizer TEXT,
        fertilizer_hi TEXT,
        harvesting TEXT,
        harvesting_hi TEXT,
        pests TEXT,
        pests_hi TEXT,
        diseases TEXT,
        diseases_hi TEXT,
        cultivation_tips TEXT,
        cultivation_tips_hi TEXT,
        source TEXT,
        source_url TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS diseases (
        id TEXT PRIMARY KEY NOT NULL,
        crop TEXT NOT NULL,
        crop_hi TEXT NOT NULL,
        disease_name_en TEXT NOT NULL,
        disease_name_hi TEXT NOT NULL,
        pathogen TEXT,
        symptoms_en TEXT,
        symptoms_hi TEXT,
        causes_en TEXT,
        causes_hi TEXT,
        treatment_organic_en TEXT,
        treatment_organic_hi TEXT,
        treatment_chemical_en TEXT,
        treatment_chemical_hi TEXT,
        prevention_en TEXT,
        prevention_hi TEXT,
        confidence_threshold REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS schemes (
        id TEXT PRIMARY KEY NOT NULL,
        name_en TEXT NOT NULL,
        name_hi TEXT NOT NULL,
        category TEXT,
        category_hi TEXT,
        ministry TEXT,
        benefits_en TEXT,
        benefits_hi TEXT,
        eligibility_en TEXT,
        eligibility_hi TEXT,
        application_process_en TEXT,
        application_process_hi TEXT,
        official_url TEXT,
        source TEXT,
        last_verified TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id TEXT PRIMARY KEY NOT NULL,
        bank_name TEXT NOT NULL,
        bank_name_hi TEXT NOT NULL,
        loan_type TEXT NOT NULL,
        loan_type_hi TEXT NOT NULL,
        purpose_en TEXT,
        purpose_hi TEXT,
        interest_rate TEXT,
        interest_rate_hi TEXT,
        max_limit TEXT,
        max_limit_hi TEXT,
        eligibility_en TEXT,
        eligibility_hi TEXT,
        documents_required TEXT,
        documents_required_hi TEXT,
        official_url TEXT,
        source TEXT,
        last_verified TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        intent TEXT NOT NULL,
        crop_id TEXT,
        language TEXT,
        question TEXT,
        answer_en TEXT,
        answer_hi TEXT,
        source TEXT
    )
    """)

    # Seed Crops
    with open(os.path.join(DATA_DIR, "verified_crops.json"), "r", encoding="utf-8") as f:
        crops = json.load(f)
    for c in crops:
        cur.execute("""
        INSERT INTO crops VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["id"], c["name_en"], c["name_hi"], c.get("scientific_name"),
            c.get("category"), c.get("category_hi"), c.get("soil"), c.get("soil_hi"),
            c.get("soil_ph"), c.get("climate"), c.get("climate_hi"), c.get("temperature"),
            c.get("sowing_season"), c.get("sowing_season_hi"), c.get("irrigation"), c.get("irrigation_hi"),
            c.get("fertilizer"), c.get("fertilizer_hi"), c.get("harvesting"), c.get("harvesting_hi"),
            c.get("pests"), c.get("pests_hi"), c.get("diseases"), c.get("diseases_hi"),
            c.get("cultivation_tips"), c.get("cultivation_tips_hi"), c.get("source"), c.get("source_url")
        ))

    # Seed Diseases
    with open(os.path.join(DATA_DIR, "verified_diseases.json"), "r", encoding="utf-8") as f:
        diseases = json.load(f)
    for d in diseases:
        cur.execute("""
        INSERT INTO diseases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d["id"], d["crop"], d["crop_hi"], d["disease_name_en"], d["disease_name_hi"],
            d.get("pathogen"), d.get("symptoms_en"), d.get("symptoms_hi"),
            d.get("causes_en"), d.get("causes_hi"), d.get("treatment_organic_en"), d.get("treatment_organic_hi"),
            d.get("treatment_chemical_en"), d.get("treatment_chemical_hi"),
            d.get("prevention_en"), d.get("prevention_hi"), d.get("confidence_threshold", 0.70)
        ))

    # Seed Schemes
    with open(os.path.join(DATA_DIR, "verified_schemes.json"), "r", encoding="utf-8") as f:
        schemes = json.load(f)
    for s in schemes:
        cur.execute("""
        INSERT INTO schemes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["id"], s["name_en"], s["name_hi"], s.get("category"), s.get("category_hi"),
            s.get("ministry"), s.get("benefits_en"), s.get("benefits_hi"),
            s.get("eligibility_en"), s.get("eligibility_hi"),
            s.get("application_process_en"), s.get("application_process_hi"),
            s.get("official_url"), s.get("source"), s.get("last_verified")
        ))

    # Seed Loans
    with open(os.path.join(DATA_DIR, "verified_loans.json"), "r", encoding="utf-8") as f:
        loans = json.load(f)
    for l in loans:
        cur.execute("""
        INSERT INTO loans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            l["id"], l["bank_name"], l["bank_name_hi"], l["loan_type"], l["loan_type_hi"],
            l.get("purpose_en"), l.get("purpose_hi"), l.get("interest_rate"), l.get("interest_rate_hi"),
            l.get("max_limit"), l.get("max_limit_hi"), l.get("eligibility_en"), l.get("eligibility_hi"),
            l.get("documents_required"), l.get("documents_required_hi"),
            l.get("official_url"), l.get("source"), l.get("last_verified")
        ))

    # Seed Facts
    with open(os.path.join(DATA_DIR, "generated_training_questions.json"), "r", encoding="utf-8") as f:
        facts = json.load(f)
    for fact in facts:
        cur.execute("""
        INSERT INTO knowledge_facts (intent, crop_id, language, question, answer_en, answer_hi, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            fact["intent"], fact.get("crop_id"), fact.get("lang"),
            fact["question"], fact["answer_en"], fact["answer_hi"], fact["source"]
        ))

    conn.commit()
    conn.close()
    print(f"Created pre-seeded SQLite database at: {db_path} ({os.path.getsize(db_path) / 1024:.1f} KB)")

def deploy_assets():
    os.makedirs(ANDROID_ASSETS_DIR, exist_ok=True)
    db_path = os.path.join(ANDROID_ASSETS_DIR, "krishi_knowledge.db")
    create_preseeded_sqlite_db(db_path)

    # Copy files to assets
    files_to_copy = [
        ("crop_disease_model.onnx", os.path.join(ML_OUTPUT_DIR, "crop_disease_model.onnx")),
        ("crop_disease_model_quantized.onnx", os.path.join(ML_OUTPUT_DIR, "crop_disease_model_quantized.onnx")),
        ("disease_labels.txt", os.path.join(ML_OUTPUT_DIR, "disease_labels.txt")),
        ("mobile_nlp_intent_model.json", os.path.join(ML_OUTPUT_DIR, "mobile_nlp_intent_model.json")),
        ("mobile_knowledge_index.json", os.path.join(ML_OUTPUT_DIR, "mobile_knowledge_index.json"))
    ]

    for dest_name, src_path in files_to_copy:
        if os.path.exists(src_path):
            shutil.copyfile(src_path, os.path.join(ANDROID_ASSETS_DIR, dest_name))
            print(f"Copied {dest_name} to Android assets.")
        else:
            print(f"Warning: {src_path} not found!")

if __name__ == "__main__":
    deploy_assets()
