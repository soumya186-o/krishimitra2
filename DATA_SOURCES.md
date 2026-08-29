# DATA_SOURCES.md — Agricultural Data Provenance & Verification

KrishiMitra enforces strict provenance attribution. Factual recommendations, scheme terms, and disease controls are sourced directly from verified Indian agricultural institutions and government portals.

---

## 1. Indian Council of Agricultural Research (ICAR) Institutes

| Crop / Domain | Institutional Source | Official Portal | Parameters Verified |
| :--- | :--- | :--- | :--- |
| **Rice / Paddy** | ICAR - National Rice Research Institute (NRRI), Cuttack | `https://icar-nrri.gov.in` | Soil pH, water submerged depth, NPK (120:60:40), SRI technique, blast control |
| **Wheat** | ICAR - Indian Institute of Wheat and Barley Research (IIWBR), Karnal | `https://iiwbr.icar.gov.in` | Sowing season, 6 critical irrigation stages (CRI 21 days), yellow rust resistance (DBW 187/303) |
| **Maize** | ICAR - Indian Institute of Maize Research (IIMR), Ludhiana | `https://iimr.icar.gov.in` | Fall Armyworm pheromone trap thresholds, silking & tasseling water requirements |
| **Cotton** | ICAR - Central Institute for Cotton Research (CICR), Nagpur | `https://cicr.icar.gov.in` | Vertisol soil, Bt cotton NPK & potash, pink bollworm crop rotation guidelines |
| **Sugarcane** | ICAR - Indian Institute of Sugarcane Research (IISR), Lucknow | `https://iisr.icar.gov.in` | Trench planting, drip fertigation, red rot prevention, Brix 18-20% maturity |
| **Mustard** | ICAR - Directorate of Rapeseed-Mustard Research (DRMR), Bharatpur | `https://drmr.icar.gov.in` | October early sowing, Sulphur (20-30 kg/ha) for oil content, aphid IPM |
| **Soybean** | ICAR - Indian Institute of Soybean Research (IISR), Indore | `https://iisrindore.icar.gov.in` | Broad Bed Furrow (BBF) drainage, Rhizobium seed treatment, girdle beetle control |
| **Chickpea** | ICAR - Indian Institute of Pulses Research (IIPR), Kanpur | `https://iipr.icar.gov.in` | Terminal shoot nipping at 35 days, Helicoverpa IPM, wilt resistance |
| **Groundnut** | ICAR - Directorate of Groundnut Research (DGR), Junagadh | `https://dgr.icar.gov.in` | Gypsum application at pegging stage, tikka disease management |
| **Potato** | ICAR - Central Potato Research Institute (CPRI), Shimla | `https://cpri.icar.gov.in` | Earthing up at 30 days, tuberization temperature (<20°C night), late blight spray schedules |
| **Tomato** | ICAR - Indian Institute of Vegetable Research (IIVR), Varanasi | `https://iivr.icar.gov.in` | Staking, blossom end rot calcium management, early blight fungicides |
| **Onion** | ICAR - Directorate of Onion and Garlic Research (DOGR), Pune | `https://dogr.icar.gov.in` | Neck-fall maturity, 15-day pre-harvest irrigation withdrawal, shade curing |
| **Chilli** | ICAR - Indian Institute of Spices Research (IISR), Kozhikode | `https://spices.res.in` | Murda disease complex (thrips/mites) neem oil schedule, anthracnose remedies |
| **Mango** | ICAR - Central Institute for Subtropical Horticulture (CISH), Lucknow | `https://cish.icar.gov.in` | Polythene trunk banding for mealybugs, pre-bloom irrigation cessation |
| **Banana** | ICAR - National Research Centre for Banana (NRCB), Tiruchirappalli | `https://nrcb.icar.gov.in` | Grand Naine tissue-culture fertigation, Sigatoka leaf spot control |

---

## 2. Ministry of Agriculture & Farmers Welfare Schemes

* **PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)**:
  * Official Portal: `https://pmkisan.gov.in`
  * Terms: ₹6,000 annual direct income support via DBT in three ₹2,000 tranches. Mandatory Aadhaar e-KYC.
* **PMFBY (Pradhan Mantri Fasal Bima Yojana)**:
  * Official Portal: `https://pmfby.gov.in`
  * Terms: 2% Kharif premium, 1.5% Rabi premium, 5% commercial/horticultural crop premium. 72-hour localized disaster intimation.
* **Kisan Credit Card (KCC)**:
  * Official Source: RBI Master Circular FIDD.CO.FSD.BC.No.6/05.05.010/2018-19 & NABARD
  * Terms: Concessional 4% effective interest rate (with 3% prompt repayment subvention) up to ₹3,00,000. Collateral-free up to ₹1,60,000.
* **Soil Health Card Scheme**:
  * Official Portal: `https://soilhealth.dac.gov.in`
  * Parameters: 12 macro, secondary, and micronutrients tested with customized fertilizer dose.
* **PMKSY (Per Drop More Crop)**:
  * Official Portal: `https://pmksy.gov.in`
  * Terms: 55% subsidy for small/marginal farmers, 45% for other farmers on micro-irrigation systems.
* **SMAM (Sub-Mission on Agricultural Mechanization)**:
  * Official Portal: `https://agrimachinery.nic.in`
  * Terms: 40-50% subsidy on individual implements; up to 80% on Custom Hiring Centres.

---

## 3. Meteorological Sources

* **Open-Meteo Agricultural API**:
  * High-resolution European Centre for Medium-Range Weather Forecasts (ECMWF) and India Meteorological Department (IMD) regional grid models.
  * Free, non-commercial open API.

---

## 4. Integrity and Zero Hallucination Policy

Agricultural chemical dosages (e.g. fungicides, insecticides) carry safety risks. KrishiMitra strictly adheres to:
1. **No Generative Chemical Invention**: Chemical active ingredients (e.g. *Tricyclazole 75% WP*, *Propiconazole 25% EC*, *Mancozeb 75% WP*) are displayed with exact ICAR dosages directly from verified tables.
2. **Prioritization of Organic & IPM Methods**: Organic biocontrol agents (*Trichoderma viride*, *Pseudomonas fluorescens*, Neem leaf extracts) are highlighted alongside chemical controls.
3. **Safety Disclaimers**: In severe infestations or ambiguous symptoms, farmers are guided to consult their local Krishi Vigyan Kendra (KVK) or the toll-free Kisan Call Centre (1800-180-1551).
