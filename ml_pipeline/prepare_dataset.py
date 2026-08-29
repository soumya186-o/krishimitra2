"""
prepare_dataset.py
Generates realistic farmer query variations across Hindi, English, and Hinglish
from verified ICAR, Ministry of Agriculture, and banking source facts.
Never hallucinates facts: questions map strictly to verified answers.
"""

import json
import os
import random

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

def generate_crop_questions(crops):
    dataset = []

    # Intent templates
    templates = {
        "soil": {
            "en": [
                "What soil is suitable for {crop_en}?",
                "Which type of soil is best for {crop_en}?",
                "What kind of soil do I need for growing {crop_en}?",
                "Tell me the suitable soil and pH for {crop_en}."
            ],
            "hi": [
                "{crop_hi} के लिए कौन सी मिट्टी अच्छी है?",
                "{crop_hi} की खेती के लिए उपयुक्त मिट्टी कौन सी है?",
                "{crop_hi} बोने के लिए कैसी जमीन चाहिए?",
                "{crop_hi} के लिए मिट्टी का पीएच कितना होना चाहिए?"
            ],
            "hinglish": [
                "{crop_en} ke liye kaunsi mitti achhi hai?",
                "{crop_en} cultivation ke liye soil kaisa hona chahiye?",
                "{crop_en} kheti ke liye best mitti kaun si hai?"
            ]
        },
        "irrigation": {
            "en": [
                "How much irrigation does {crop_en} need?",
                "When should I water {crop_en}?",
                "What are the critical irrigation stages for {crop_en}?",
                "Watering schedule for {crop_en} cultivation."
            ],
            "hi": [
                "{crop_hi} में कितनी सिंचाई की आवश्यकता होती है?",
                "{crop_hi} को पानी कब-कब देना चाहिए?",
                "{crop_hi} की सिंचाई के मुख्य समय कौन से हैं?",
                "{crop_hi} में पानी कब लगाएं?"
            ],
            "hinglish": [
                "{crop_en} me kitni sinchai karni chahiye?",
                "{crop_en} ko pani kab kab dena chahiye?",
                "{crop_en} irrigation requirement kitni hai?"
            ]
        },
        "fertilizer": {
            "en": [
                "What fertilizer and NPK dose is recommended for {crop_en}?",
                "How much urea and DAP should I apply to {crop_en}?",
                "Nutrient management for {crop_en}.",
                "Best fertilizer schedule for {crop_en} crop."
            ],
            "hi": [
                "{crop_hi} में कौन सी खाद और कितनी मात्रा में डालनी चाहिए?",
                "{crop_hi} के लिए एनपीके की अनुशंसित मात्रा क्या है?",
                "{crop_hi} में यूरिया और डीएपी कब दें?",
                "{crop_hi} की फसल में खाद प्रबंधन कैसे करें?"
            ],
            "hinglish": [
                "{crop_en} me kaunsi khad dalni chahiye?",
                "{crop_en} ke liye NPK ratio kitna hona chahiye?",
                "{crop_en} me urea kitna dale?"
            ]
        },
        "sowing": {
            "en": [
                "What is the best sowing time for {crop_en}?",
                "When to sow {crop_en}?",
                "Which season is suitable for {crop_en} cultivation?",
                "Ideal planting month for {crop_en}."
            ],
            "hi": [
                "{crop_hi} की बुवाई का सही समय क्या है?",
                "{crop_hi} कब बोई जाती है?",
                "{crop_hi} की खेती किस मौसम में करनी चाहिए?",
                "{crop_hi} लगाने का सबसे अच्छा महीना कौन सा है?"
            ],
            "hinglish": [
                "{crop_en} ki buwai kab karni chahiye?",
                "{crop_en} sowing time kaun sa best hai?",
                "{crop_en} kab lagaye?"
            ]
        },
        "pests_diseases": {
            "en": [
                "What are common pests and diseases in {crop_en}?",
                "How to protect {crop_en} from insects and disease?",
                "Major disease problems in {crop_en} crop.",
                "Pest control in {crop_en}."
            ],
            "hi": [
                "{crop_hi} में कौन-कौन से मुख्य रोग और कीट लगते हैं?",
                "{crop_hi} को कीड़ों और बीमारियों से कैसे बचाएं?",
                "{crop_hi} के प्रमुख कीट और उनका रोकथाम क्या है?",
                "{crop_hi} की पत्तियों पर बीमारी का इलाज बताइए।"
            ],
            "hinglish": [
                "{crop_en} me lagne wale keede aur bimari kaun si hai?",
                "{crop_en} me pest control kaise kare?",
                "{crop_en} ke rogon se bachav kaise kare?"
            ]
        },
        "harvesting": {
            "en": [
                "When should I harvest {crop_en}?",
                "How many days does {crop_en} take to mature?",
                "Maturity signs and harvesting of {crop_en}.",
                "Duration of {crop_en} crop."
            ],
            "hi": [
                "{crop_hi} की कटाई कब करनी चाहिए?",
                "{crop_hi} कितने दिनों में पककर तैयार होती है?",
                "{crop_hi} की फसल पकने की क्या पहचान है?",
                "{crop_hi} की तुड़ाई कब करें?"
            ],
            "hinglish": [
                "{crop_en} ki katai kab kare?",
                "{crop_en} kitne din me taiyar hoti hai?",
                "{crop_en} harvest kab karna chahiye?"
            ]
        },
        "cultivation_tips": {
            "en": [
                "How to get high yield in {crop_en}?",
                "Cultivation techniques and tips for {crop_en}.",
                "Best farming practices for {crop_en}.",
                "Special tips for growing {crop_en}."
            ],
            "hi": [
                "{crop_hi} से अधिक पैदावार कैसे प्राप्त करें?",
                "{crop_hi} की उन्नत खेती के तरीके क्या हैं?",
                "{crop_hi} की खेती के विशेष सुझाव दीजिए।",
                "{crop_hi} का उत्पादन कैसे बढ़ाएं?"
            ],
            "hinglish": [
                "{crop_en} ki unnat kheti kaise kare?",
                "{crop_en} me jyada paidawar kaise paye?",
                "{crop_en} farming tips bataye."
            ]
        }
    }

    for crop in crops:
        c_en = crop["name_en"].split("/")[0].strip()
        c_hi = crop["name_hi"].split("/")[0].strip()

        # Soil
        ans_en = f"{crop['soil']} (Optimal pH: {crop['soil_ph']})"
        ans_hi = f"{crop['soil_hi']} (उपयुक्त पीएच मान: {crop['soil_ph']})"
        for q in templates["soil"]["en"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "en", "intent": "soil", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["soil"]["hi"]:
            dataset.append({"question": q.format(crop_hi=c_hi), "lang": "hi", "intent": "soil", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["soil"]["hinglish"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "hinglish", "intent": "soil", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})

        # Irrigation
        ans_en = crop["irrigation"]
        ans_hi = crop["irrigation_hi"]
        for q in templates["irrigation"]["en"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "en", "intent": "irrigation", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["irrigation"]["hi"]:
            dataset.append({"question": q.format(crop_hi=c_hi), "lang": "hi", "intent": "irrigation", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["irrigation"]["hinglish"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "hinglish", "intent": "irrigation", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})

        # Fertilizer
        ans_en = crop["fertilizer"]
        ans_hi = crop["fertilizer_hi"]
        for q in templates["fertilizer"]["en"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "en", "intent": "fertilizer", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["fertilizer"]["hi"]:
            dataset.append({"question": q.format(crop_hi=c_hi), "lang": "hi", "intent": "fertilizer", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["fertilizer"]["hinglish"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "hinglish", "intent": "fertilizer", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})

        # Sowing
        ans_en = f"Season: {crop['sowing_season']}. Optimal Temperature: {crop['temperature']}."
        ans_hi = f"मौसम: {crop['sowing_season_hi']}। अनुकूल तापमान: {crop['temperature']}।"
        for q in templates["sowing"]["en"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "en", "intent": "sowing", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["sowing"]["hi"]:
            dataset.append({"question": q.format(crop_hi=c_hi), "lang": "hi", "intent": "sowing", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["sowing"]["hinglish"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "hinglish", "intent": "sowing", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})

        # Pests & Diseases
        ans_en = f"Common Pests: {crop['pests']}. Common Diseases: {crop['diseases']}."
        ans_hi = f"प्रमुख कीट: {crop['pests_hi']}। प्रमुख रोग: {crop['diseases_hi']}।"
        for q in templates["pests_diseases"]["en"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "en", "intent": "pests_diseases", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["pests_diseases"]["hi"]:
            dataset.append({"question": q.format(crop_hi=c_hi), "lang": "hi", "intent": "pests_diseases", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["pests_diseases"]["hinglish"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "hinglish", "intent": "pests_diseases", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})

        # Harvesting
        ans_en = crop["harvesting"]
        ans_hi = crop["harvesting_hi"]
        for q in templates["harvesting"]["en"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "en", "intent": "harvesting", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["harvesting"]["hi"]:
            dataset.append({"question": q.format(crop_hi=c_hi), "lang": "hi", "intent": "harvesting", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["harvesting"]["hinglish"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "hinglish", "intent": "harvesting", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})

        # Cultivation Tips
        ans_en = crop["cultivation_tips"]
        ans_hi = crop["cultivation_tips_hi"]
        for q in templates["cultivation_tips"]["en"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "en", "intent": "cultivation", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["cultivation_tips"]["hi"]:
            dataset.append({"question": q.format(crop_hi=c_hi), "lang": "hi", "intent": "cultivation", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})
        for q in templates["cultivation_tips"]["hinglish"]:
            dataset.append({"question": q.format(crop_en=c_en), "lang": "hinglish", "intent": "cultivation", "crop_id": crop["id"], "answer_en": ans_en, "answer_hi": ans_hi, "source": crop["source"]})

    return dataset

def generate_scheme_questions(schemes):
    dataset = []
    for s in schemes:
        ans_en = f"{s['name_en']}: {s['benefits_en']} Eligibility: {s['eligibility_en']} Apply at: {s['official_url']}"
        ans_hi = f"{s['name_hi']}: {s['benefits_hi']} पात्रता: {s['eligibility_hi']} आवेदन: {s['official_url']}"

        s_name = s['name_en'].split("(")[0].strip()
        s_hi = s['name_hi'].split("(")[0].strip()

        queries_en = [
            f"What is {s_name}?",
            f"What are the benefits of {s_name}?",
            f"How to apply for {s_name}?",
            f"Who is eligible for {s_name}?",
            f"Tell me about {s['name_en']}."
        ]
        queries_hi = [
            f"{s_hi} क्या है?",
            f"{s_hi} के क्या लाभ हैं?",
            f"{s_hi} में आवेदन कैसे करें?",
            f"{s_hi} के लिए कौन पात्र है?",
            f"{s['name_hi']} की जानकारी दीजिए।"
        ]
        queries_hinglish = [
            f"{s_name} scheme ke bare me bataye?",
            f"{s_name} me apply kaise kare?",
            f"{s_name} ka labh kaise milega?"
        ]

        for q in queries_en:
            dataset.append({"question": q, "lang": "en", "intent": "schemes", "crop_id": None, "answer_en": ans_en, "answer_hi": ans_hi, "source": s["source"]})
        for q in queries_hi:
            dataset.append({"question": q, "lang": "hi", "intent": "schemes", "crop_id": None, "answer_en": ans_en, "answer_hi": ans_hi, "source": s["source"]})
        for q in queries_hinglish:
            dataset.append({"question": q, "lang": "hinglish", "intent": "schemes", "crop_id": None, "answer_en": ans_en, "answer_hi": ans_hi, "source": s["source"]})

    return dataset

def generate_loan_questions(loans):
    dataset = []
    for l in loans:
        ans_en = f"{l['loan_type']} ({l['bank_name']}): Interest rate: {l['interest_rate']}. Max limit: {l['max_limit']}. Purpose: {l['purpose_en']}"
        ans_hi = f"{l['loan_type_hi']} ({l['bank_name_hi']}): ब्याज दर: {l['interest_rate_hi']}। अधिकतम सीमा: {l['max_limit_hi']}। उद्देश्य: {l['purpose_hi']}"

        l_name = l['loan_type']
        l_hi = l['loan_type_hi']

        queries_en = [
            f"What is {l_name}?",
            f"What is the interest rate for {l_name}?",
            f"How to get agricultural loan {l_name}?",
            f"Eligibility for {l_name}."
        ]
        queries_hi = [
            f"{l_hi} क्या है?",
            f"{l_hi} की ब्याज दर क्या है?",
            f"{l_hi} कैसे प्राप्त करें?",
            f"{l_hi} के लिए कौन से दस्तावेज चाहिए?"
        ]
        queries_hinglish = [
            f"{l_name} loan kaise milega?",
            f"{l_name} ka interest rate kitna hai?",
            f"{l_name} ke liye eligibility kya hai?"
        ]

        for q in queries_en:
            dataset.append({"question": q, "lang": "en", "intent": "loans", "crop_id": None, "answer_en": ans_en, "answer_hi": ans_hi, "source": l["source"]})
        for q in queries_hi:
            dataset.append({"question": q, "lang": "hi", "intent": "loans", "crop_id": None, "answer_en": ans_en, "answer_hi": ans_hi, "source": l["source"]})
        for q in queries_hinglish:
            dataset.append({"question": q, "lang": "hinglish", "intent": "loans", "crop_id": None, "answer_en": ans_en, "answer_hi": ans_hi, "source": l["source"]})

    return dataset

def generate_disease_questions(diseases):
    dataset = []
    for d in diseases:
        if d["id"] in ["soil_or_background", "uncertain_quality"]:
            continue
        ans_en = f"Disease: {d['disease_name_en']} in {d['crop']}. Symptoms: {d['symptoms_en']}. Organic treatment: {d['treatment_organic_en']}. Chemical treatment: {d['treatment_chemical_en']}."
        ans_hi = f"रोग: {d['disease_name_hi']} ({d['crop_hi']})। लक्षण: {d['symptoms_hi']}। जैविक उपचार: {d['treatment_organic_hi']}। रासायनिक उपचार: {d['treatment_chemical_hi']}।"

        d_en = d['disease_name_en']
        d_hi = d['disease_name_hi']

        queries_en = [
            f"What is {d_en} in {d['crop']}?",
            f"How to control {d_en} in {d['crop']}?",
            f"Symptoms and cure of {d_en}.",
            f"Treatment for {d_en} disease."
        ]
        queries_hi = [
            f"{d['crop_hi']} में {d_hi} के क्या लक्षण हैं?",
            f"{d_hi} का उपचार क्या है?",
            f"{d['crop_hi']} में {d_hi} की रोकथाम कैसे करें?",
            f"{d_hi} के लिए कौन सी दवा छिड़कें?"
        ]
        queries_hinglish = [
            f"{d['crop']} me {d_en} ki dawai bataye?",
            f"{d_en} bimari ka ilaj kya hai?",
            f"{d_en} disease control kaise kare?"
        ]

        for q in queries_en:
            dataset.append({"question": q, "lang": "en", "intent": "disease", "crop_id": d["crop"].lower(), "answer_en": ans_en, "answer_hi": ans_hi, "source": "ICAR Plant Pathology Guidelines"})
        for q in queries_hi:
            dataset.append({"question": q, "lang": "hi", "intent": "disease", "crop_id": d["crop"].lower(), "answer_en": ans_en, "answer_hi": ans_hi, "source": "ICAR Plant Pathology Guidelines"})
        for q in queries_hinglish:
            dataset.append({"question": q, "lang": "hinglish", "intent": "disease", "crop_id": d["crop"].lower(), "answer_en": ans_en, "answer_hi": ans_hi, "source": "ICAR Plant Pathology Guidelines"})

    return dataset

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    crops = load_json("verified_crops.json")
    schemes = load_json("verified_schemes.json")
    loans = load_json("verified_loans.json")
    diseases = load_json("verified_diseases.json")

    print(f"Loaded {len(crops)} crops, {len(schemes)} schemes, {len(loans)} loans, {len(diseases)} diseases.")

    crop_qs = generate_crop_questions(crops)
    scheme_qs = generate_scheme_questions(schemes)
    loan_qs = generate_loan_questions(loans)
    disease_qs = generate_disease_questions(diseases)

    all_data = crop_qs + scheme_qs + loan_qs + disease_qs
    random.seed(42)
    random.shuffle(all_data)

    output_file = os.path.join(DATA_DIR, "generated_training_questions.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(all_data)} question-answer pairs.")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
