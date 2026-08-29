package com.krishimitra.app.voice

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.Locale

enum class VoiceMode {
    AUTO,
    HINDI,
    ENGLISH
}

class VoiceManager(private val context: Context) : TextToSpeech.OnInitListener {

    companion object {
        private const val TAG = "VoiceManager"
    }

    private var speechRecognizer: SpeechRecognizer? = null
    private var tts: TextToSpeech? = null
    private var isTtsReady = false

    private val _isListening = MutableStateFlow(false)
    val isListening: StateFlow<Boolean> = _isListening.asStateFlow()

    private val _isSpeaking = MutableStateFlow(false)
    val isSpeaking: StateFlow<Boolean> = _isSpeaking.asStateFlow()

    private val _transcription = MutableStateFlow<String?>(null)
    val transcription: StateFlow<String?> = _transcription.asStateFlow()

    private val _voiceMode = MutableStateFlow(VoiceMode.AUTO)
    val voiceMode: StateFlow<VoiceMode> = _voiceMode.asStateFlow()

    private var onSpeechResultCallback: ((String) -> Unit)? = null

    init {
        tts = TextToSpeech(context, this)
        initSpeechRecognizer()
    }

    private fun initSpeechRecognizer() {
        if (SpeechRecognizer.isRecognitionAvailable(context)) {
            speechRecognizer = SpeechRecognizer.createSpeechRecognizer(context).apply {
                setRecognitionListener(object : RecognitionListener {
                    override fun onReadyForSpeech(params: Bundle?) {
                        _isListening.value = true
                    }

                    override fun onBeginningOfSpeech() {}
                    override fun onRmsChanged(rmsdB: Float) {}
                    override fun onBufferReceived(buffer: ByteArray?) {}

                    override fun onEndOfSpeech() {
                        _isListening.value = false
                    }

                    override fun onError(error: Int) {
                        _isListening.value = false
                        val errorMsg = when (error) {
                            SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "Network timeout"
                            SpeechRecognizer.ERROR_NO_MATCH -> "No speech match"
                            SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "Busy"
                            SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "Permission required"
                            else -> "Recognition error ($error)"
                        }
                        Log.w(TAG, "Speech error: $errorMsg")
                    }

                    override fun onResults(results: Bundle?) {
                        _isListening.value = false
                        val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                        if (!matches.isNullOrEmpty()) {
                            val recognized = matches[0]
                            _transcription.value = recognized
                            onSpeechResultCallback?.invoke(recognized)
                        }
                    }

                    override fun onPartialResults(partialResults: Bundle?) {
                        val matches = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                        if (!matches.isNullOrEmpty()) {
                            _transcription.value = matches[0]
                        }
                    }

                    override fun onEvent(eventType: Int, params: Bundle?) {}
                })
            }
        }
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            isTtsReady = true
            tts?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(utteranceId: String?) {
                    _isSpeaking.value = true
                }

                override fun onDone(utteranceId: String?) {
                    _isSpeaking.value = false
                }

                override fun onError(utteranceId: String?) {
                    _isSpeaking.value = false
                }
            })
        }
    }

    fun setVoiceMode(mode: VoiceMode) {
        _voiceMode.value = mode
    }

    fun startListening(onResult: (String) -> Unit) {
        stopSpeaking()
        this.onSpeechResultCallback = onResult
        _transcription.value = null

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)

            when (_voiceMode.value) {
                VoiceMode.HINDI -> {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN")
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "hi-IN")
                }
                VoiceMode.ENGLISH -> {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, "en-IN")
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "en-IN")
                }
                VoiceMode.AUTO -> {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault().toLanguageTag())
                    putExtra(RecognizerIntent.EXTRA_SUPPORTED_LANGUAGES, arrayListOf("hi-IN", "en-IN"))
                }
            }
        }

        try {
            speechRecognizer?.startListening(intent)
            _isListening.value = true
        } catch (e: Exception) {
            Log.e(TAG, "Failed to start listening: ${e.message}")
            _isListening.value = false
        }
    }

    fun stopListening() {
        try {
            speechRecognizer?.stopListening()
        } catch (e: Exception) {
            Log.e(TAG, "Error stopping listening: ${e.message}")
        } finally {
            _isListening.value = false
        }
    }

    fun speak(text: String, isHindi: Boolean = true) {
        if (!isTtsReady || tts == null) return
        stopSpeaking()

        val loc = if (isHindi || text.any { it.code in 0x0900..0x097F }) {
            Locale("hi", "IN")
        } else {
            Locale("en", "IN")
        }

        tts?.language = loc
        tts?.setSpeechRate(0.92f) // Slightly relaxed pace for maximum farmer clarity
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "krishi_tts_${System.currentTimeMillis()}")
    }

    fun stopSpeaking() {
        if (isTtsReady) {
            tts?.stop()
            _isSpeaking.value = false
        }
    }

    fun destroy() {
        try {
            speechRecognizer?.destroy()
            tts?.stop()
            tts?.shutdown()
        } catch (e: Exception) {
            Log.e(TAG, "Error destroying voice manager: ${e.message}")
        }
    }
}
