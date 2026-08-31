package com.krishimitra.app.domain.ai

import com.krishimitra.app.data.remote.ApiClient
import com.krishimitra.app.domain.model.ChatMessage
import com.krishimitra.app.ml.LocalNLPEngine
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

interface AIProvider {
    suspend fun answer(query: String, crop: String? = null, district: String? = null): ChatMessage
}

class LocalAIProvider(private val localEngine: LocalNLPEngine) : AIProvider {
    override suspend fun answer(query: String, crop: String?, district: String?): ChatMessage = withContext(Dispatchers.Default) {
        val result = localEngine.answerQuery(query, cropContext = crop, districtContext = district)
        return@withContext ChatMessage(
            text = result.answer,
            isUser = false,
            source = result.source,
            isVerified = result.isVerified,
            intent = result.intent
        )
    }
}

class CloudAIProvider(private val apiClient: ApiClient) : AIProvider {
    override suspend fun answer(query: String, crop: String?, district: String?): ChatMessage = withContext(Dispatchers.IO) {
        val cloudResponse = apiClient.queryCloudAI(query, crop, district)
        if (cloudResponse != null) {
            val ans = cloudResponse.get("answer").asString
            val source = cloudResponse.get("source")?.asString ?: "Cloud AI (ICAR Grounded)"
            val verified = cloudResponse.get("is_verified_fact")?.asBoolean ?: false
            val intent = cloudResponse.get("detected_intent")?.asString

            return@withContext ChatMessage(
                text = ans,
                isUser = false,
                source = source,
                isVerified = verified,
                intent = intent
            )
        }
        throw IllegalStateException("Cloud AI request failed or offline")
    }
}

class HybridAIRouter(
    private val localEngine: LocalNLPEngine,
    private val apiClient: ApiClient
) {
    private val localProvider = LocalAIProvider(localEngine)
    private val cloudProvider = CloudAIProvider(apiClient)

    suspend fun routeQuery(query: String, crop: String? = null, district: String? = null): ChatMessage = withContext(Dispatchers.Default) {
        val (predictedIntent, confidence) = localEngine.predictIntent(query)

        // Step 1: High local confidence OR offline -> Answer immediately using local knowledge
        if (confidence >= 0.70f || !apiClient.isNetworkAvailable()) {
            return@withContext localProvider.answer(query, crop, district)
        }

        // Step 2: Low confidence AND internet available -> Fall back to Cloud AI
        try {
            return@withContext cloudProvider.answer(query, crop, district)
        } catch (e: Exception) {
            // Step 3: Graceful fallback to local engine if cloud fails
            return@withContext localProvider.answer(query, crop, district)
        }
    }
}

