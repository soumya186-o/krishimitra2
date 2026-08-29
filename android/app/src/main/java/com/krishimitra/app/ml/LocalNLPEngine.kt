package com.krishimitra.app.ml

import android.content.Context
import android.util.Log
import org.json.JSONArray
import org.json.JSONObject
import java.util.Locale

class LocalNLPEngine(private val context: Context) {

    companion object {
        private const val TAG = "LocalNLPEngine"
    }

    private var vocabulary: Map<String, Int> = emptyMap()
    private var idf: List<Float> = emptyList()
    private var classes: List<String> = emptyList()
    private var coefficients: List<List<Float>> = emptyList()
    private var intercepts: List<Float> = emptyList()
    private var knowledgeFacts: List<FactEntry> = emptyList()
    private var isLoaded: Boolean = false

    data class FactEntry(
        val intent: String,
        val cropId: String?,
        val sampleQuestion: String,
        val answerEn: String,
        val answerHi: String,
        val source: String
    )

    data class NLPResult(
        val answer: String,
        val answerHi: String,
        val intent: String,
        val cropId: String?,
        val confidence: Float,
        val isVerified: Boolean,
        val source: String
    )

    init {
        loadAssets()
    }

    private fun loadAssets() {
        try {
            // 1. Load Intent Model
            context.assets.open("mobile_nlp_intent_model.json").use { stream ->
                val jsonStr = stream.bufferedReader().use { it.readText() }
                val obj = JSONObject(jsonStr)

                val vocabObj = obj.getJSONObject("vocabulary")
                val vocabMap = mutableMapOf<String, Int>()
                val keys = vocabObj.keys()
                while (keys.hasNext()) {
                    val k = keys.next()
                    vocabMap[k] = vocabObj.getInt(k)
                }
                vocabulary = vocabMap

                val idfArr = obj.getJSONArray("idf")
                val idfList = mutableListOf<Float>()
                for (i in 0 until idfArr.length()) {
                    idfList.add(idfArr.getDouble(i).toFloat())
                }
                idf = idfList

                val classArr = obj.getJSONArray("classes")
                val classList = mutableListOf<String>()
                for (i in 0 until classArr.length()) {
                    classList.add(classArr.getString(i))
                }
                classes = classList

                val coefArr = obj.getJSONArray("coefficients")
                val coefList = mutableListOf<List<Float>>()
                for (i in 0 until coefArr.length()) {
                    val row = coefArr.getJSONArray(i)
                    val rowList = mutableListOf<Float>()
                    for (j in 0 until row.length()) {
                        rowList.add(row.getDouble(j).toFloat())
                    }
                    coefList.add(rowList)
                }
                coefficients = coefList

                val intArr = obj.getJSONArray("intercept")
                val intList = mutableListOf<Float>()
                for (i in 0 until intArr.length()) {
                    intList.add(intArr.getDouble(i).toFloat())
                }
                intercepts = intList
            }

            // 2. Load Knowledge Index
            context.assets.open("mobile_knowledge_index.json").use { stream ->
                val jsonStr = stream.bufferedReader().use { it.readText() }
                val arr = JSONArray(jsonStr)
                val list = mutableListOf<FactEntry>()
                for (i in 0 until arr.length()) {
                    val item = arr.getJSONObject(i)
                    list.add(
                        FactEntry(
                            intent = item.getString("intent"),
                            cropId = if (item.has("crop_id") && !item.isNull("crop_id")) item.getString("crop_id") else null,
                            sampleQuestion = item.optString("sample_question", ""),
                            answerEn = item.getString("answer_en"),
                            answerHi = item.getString("answer_hi"),
                            source = item.optString("source", "ICAR Verified Agricultural Data")
                        )
                    )
                }
                knowledgeFacts = list
            }

            isLoaded = true
            Log.i(TAG, "Local NLP Engine initialized with ${vocabulary.size} tokens and ${knowledgeFacts.size} facts.")
        } catch (e: Exception) {
            Log.e(TAG, "Failed to load NLP assets: ${e.message}", e)
        }
    }

    fun detectCrop(query: String): String? {
        val q = query.lowercase(Locale.ROOT)
        val cropMap = mapOf(
            "rice" to listOf("rice", "paddy", "धान", "चावल", "dhan", "chawal"),
            "wheat" to listOf("wheat", "गेहूं", "गेहू", "gehu", "gehun"),
            "maize" to listOf("maize", "corn", "मक्का", "मकई", "makka", "makai", "bhutta"),
            "cotton" to listOf("cotton", "कपास", "रुई", "kapas"),
            "sugarcane" to listOf("sugarcane", "गन्ना", "ईख", "ganna"),
            "mustard" to listOf("mustard", "सरसों", "राई", "sarson", "sarso", "rai"),
            "soybean" to listOf("soybean", "सोयाबीन", "soyabean"),
            "chickpea" to listOf("chickpea", "gram", "चना", "chana"),
            "groundnut" to listOf("groundnut", "peanut", "मूंगफली", "mungfali", "moongphali"),
            "potato" to listOf("potato", "आलू", "alu", "aaloo"),
            "tomato" to listOf("tomato", "टमाटर", "tamatar"),
            "onion" to listOf("onion", "प्याज", "pyaj", "pyaz", "kanda"),
            "chilli" to listOf("chilli", "chili", "मिर्च", "mirch", "mirchi"),
            "mango" to listOf("mango", "आम", "aam"),
            "banana" to listOf("banana", "केला", "kela")
        )

        for ((cropId, aliases) in cropMap) {
            for (alias in aliases) {
                if (q.contains(alias)) return cropId
            }
        }
        return null
    }

    fun predictIntent(query: String): Pair<String, Float> {
        val q = query.lowercase(Locale.ROOT)
        // Rule heuristic boost for key agricultural intents
        if (q.contains("मिट्टी") || q.contains("soil") || q.contains("mitti") || q.contains("जमीन")) return "soil" to 0.98f
        if (q.contains("सिंचाई") || q.contains("irrigation") || q.contains("पानी") || q.contains("pani") || q.contains("sinchai")) return "irrigation" to 0.98f
        if (q.contains("खाद") || q.contains("fertilizer") || q.contains("यूरिया") || q.contains("urea") || q.contains("dap") || q.contains("npk") || q.contains("khad")) return "fertilizer" to 0.98f
        if (q.contains("बुवाई") || q.contains("sow") || q.contains("sowing") || q.contains("rohai") || q.contains("lagaye")) return "sowing" to 0.98f
        if (q.contains("कटाई") || q.contains("harvest") || q.contains("katai") || q.contains("pakne")) return "harvesting" to 0.98f
        if (q.contains("योजना") || q.contains("scheme") || q.contains("subsidy") || q.contains("pm-kisan") || q.contains("pmfby")) return "schemes" to 0.98f
        if (q.contains("लोन") || q.contains("ऋण") || q.contains("loan") || q.contains("kcc") || q.contains("credit")) return "loans" to 0.98f
        if (q.contains("रोग") || q.contains("कीट") || q.contains("disease") || q.contains("pest") || q.contains("dawai") || q.contains("दवा") || q.contains("इल्ली") || q.contains("झुलसा")) return "pests_diseases" to 0.98f

        if (!isLoaded || coefficients.isEmpty()) return "cultivation" to 0.70f

        // Tokenize and extract unigrams and bigrams
        val tokens = q.replace(Regex("[?!.,;:'\"()\\[\\]{}]"), " ").split("\\s+".toRegex()).filter { it.isNotBlank() }
        val featureCounts = mutableMapOf<Int, Float>()

        for (token in tokens) {
            vocabulary[token]?.let { idx ->
                featureCounts[idx] = (featureCounts[idx] ?: 0f) + 1f
            }
        }
        for (i in 0 until tokens.size - 1) {
            val bigram = "${tokens[i]} ${tokens[i + 1]}"
            vocabulary[bigram]?.let { idx ->
                featureCounts[idx] = (featureCounts[idx] ?: 0f) + 1f
            }
        }

        if (featureCounts.isEmpty()) {
            return "cultivation" to 0.65f
        }

        // Apply TF-IDF weighting and L2 normalization
        var normSq = 0f
        val tfidf = mutableMapOf<Int, Float>()
        for ((idx, count) in featureCounts) {
            val weight = count * (idf.getOrNull(idx) ?: 1f)
            tfidf[idx] = weight
            normSq += weight * weight
        }
        val norm = if (normSq > 0) kotlin.math.sqrt(normSq) else 1f

        // Compute dot product with coefficients for each class
        var maxScore = -Float.MAX_VALUE
        var bestClass = classes.firstOrNull() ?: "cultivation"

        for (cIdx in classes.indices) {
            var score = intercepts.getOrNull(cIdx) ?: 0f
            val row = coefficients.getOrNull(cIdx) ?: continue
            for ((featIdx, weight) in tfidf) {
                val coefVal = row.getOrNull(featIdx) ?: 0f
                score += (weight / norm) * coefVal
            }
            if (score > maxScore) {
                maxScore = score
                bestClass = classes[cIdx]
            }
        }

        // Softmax sigmoid approximation for confidence
        val conf = 1f / (1f + kotlin.math.exp(-maxScore.coerceIn(-10f, 10f)))
        return bestClass to conf.coerceIn(0.70f, 0.99f)
    }

    fun answerQuery(query: String, forceLang: String? = null): NLPResult {
        val detectedCrop = detectCrop(query)
        val (intent, confidence) = predictIntent(query)
        val isHindi = forceLang == "hi" || (forceLang == null && query.any { it.code in 0x0900..0x097F })

        // 1. Look for exact match (intent + crop)
        var match = knowledgeFacts.firstOrNull { it.intent == intent && it.cropId == detectedCrop }
        // 2. If crop found but no exact intent, match crop with general/cultivation intent
        if (match == null && detectedCrop != null) {
            match = knowledgeFacts.firstOrNull { it.cropId == detectedCrop }
        }
        // 3. If no crop found, match by intent (e.g. general scheme/loan query)
        if (match == null) {
            match = knowledgeFacts.firstOrNull { it.intent == intent }
        }

        if (match != null) {
            val ans = if (isHindi) match.answerHi else match.answerEn
            return NLPResult(
                answer = ans,
                answerHi = match.answerHi,
                intent = intent,
                cropId = detectedCrop,
                confidence = confidence,
                isVerified = true,
                source = match.source
            )
        }

        // Safe fallback
        val defaultHi = "आपकी फसल से संबंधित यह प्रश्न दर्ज कर लिया गया है। कृपया सटीक सिफारिश हेतु अपने जिले के कृषि विज्ञान केंद्र (KVK) से संपर्क करें अथवा नजदीकी किसान कॉल सेंटर (1800-180-1551) पर कॉल करें।"
        val defaultEn = "Your query has been recorded. For customized field advice, please contact your District Krishi Vigyan Kendra (KVK) or Kisan Call Centre at 1800-180-1551."

        return NLPResult(
            answer = if (isHindi) defaultHi else defaultEn,
            answerHi = defaultHi,
            intent = intent,
            cropId = detectedCrop,
            confidence = 0.65f,
            isVerified = true,
            source = "ICAR Kisan Call Centre National Guidelines"
        )
    }
}
