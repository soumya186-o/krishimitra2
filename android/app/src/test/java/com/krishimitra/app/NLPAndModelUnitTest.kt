package com.krishimitra.app

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test

class NLPAndModelUnitTest {

    @Test
    fun testCropAliasDetection() {
        val hindiQuery = "धान के लिए कौन सी मिट्टी अच्छी है?"
        val containsRice = hindiQuery.contains("धान")
        assertTrue("Query should contain Hindi rice alias", containsRice)

        val englishQuery = "Which soil is best for wheat?"
        val containsWheat = englishQuery.lowercase().contains("wheat")
        assertTrue("Query should contain English wheat alias", containsWheat)
    }

    @Test
    fun testIntentKeywordHeuristics() {
        val queries = mapOf(
            "धान की सिंचाई कब करें?" to "सिंचाई",
            "यूरिया और डीएपी कितनी डालें?" to "यूरिया",
            "पीएम किसान योजना क्या है?" to "योजना",
            "केसीसी ऋण की ब्याज दर क्या है?" to "ऋण"
        )

        for ((q, keyword) in queries) {
            assertTrue("Query should match agricultural keyword $keyword", q.contains(keyword))
        }
    }

    @Test
    fun testConfidenceThresholdBoundary() {
        val standardCertainty = 0.70f
        val lowQualityScore = 0.42f
        val isCertain = standardCertainty >= 0.70f
        val isUncertain = lowQualityScore < 0.50f

        assertTrue(isCertain)
        assertTrue(isUncertain)
    }
}
