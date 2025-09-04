import streamlit as st
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from pydub import AudioSegment
import io
import base64


import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\padda\OneDrive\Documents\onyx-sphere-468507-b7-374e6f78505f.json"
# Helper: Convert audio bytes to base64 for playback
def audio_bytes_to_base64(audio_bytes, format="mp3"):
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    return f"data:audio/{format};base64,{audio_base64}"

def transcribe_audio(audio_file, language_code="en-IN"):
    client = speech.SpeechClient()
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript

def synthesize_speech(text, language_code="en-IN", voice_name=None, gender=texttospeech.SsmlVoiceGender.NEUTRAL):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = {
        "language_code": language_code,
        "ssml_gender": gender,
    }
    if voice_name:
        voice_params["name"] = voice_name
    voice = texttospeech.VoiceSelectionParams(**voice_params)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

languages = [
    ("English (India)", "en-IN"),
    ("Hindi", "hi-IN"),
    ("Hinglish", "hi-IN"),  # Hinglish treated as Hindi for TTS
    ("Tamil", "ta-IN"),
    ("Telugu", "te-IN"),
    ("Malayalam", "ml-IN"),
    ("Kannada", "kn-IN"),
    ("Bengali", "bn-IN"),
    ("Marathi", "mr-IN"),
    ("Gujarati", "gu-IN"),
    ("Punjabi", "pa-IN"),
]

voices_by_language = {
    "en-IN": [
        ("English (Female A)", "en-IN-Wavenet-A"),
        ("English (Male B)", "en-IN-Wavenet-B"),
    ],
    "hi-IN": [
        ("Hindi (Female A)", "hi-IN-Wavenet-A"),
        ("Hindi (Male B)", "hi-IN-Wavenet-B"),
    ],
    "ta-IN": [
        ("Tamil (Female A)", "ta-IN-Wavenet-A"),
    ],
    "te-IN": [
        ("Telugu (Female A)", "te-IN-Wavenet-A"),
    ],
    # Others empty for demo
}

st.title("Multilingual STT & TTS with Hinglish Demo")

# Step 1: Select language button workflow
if 'language_selected' not in st.session_state:
    st.session_state.language_selected = False

if not st.session_state.language_selected:
    lang = st.selectbox(
        "Select Language for STT and TTS",
        options=languages,
        format_func=lambda x: x[0],
        key="language_select"
    )
    if st.button("Confirm Language"):
        st.session_state.language_selected = True
        st.session_state.lang = lang
else:
    lang = st.session_state.lang

    # Voices for selected language
    voice_options = voices_by_language.get(lang[1], [])
    if voice_options:
        selected_voice = st.selectbox(
            "Select TTS Voice",
            options=voice_options,
            format_func=lambda x: x[0],
            key="voice_select"
        )
        voice_name = selected_voice[1]
    else:
        st.info(f"No TTS voices available for {lang[0]}, using default voice.")
        voice_name = None

    st.subheader("Speech-to-Text (Upload WAV)")

    uploaded_audio = st.file_uploader("Upload a WAV audio file (16kHz, mono)", type=["wav"], key="audio_uploader")
    if uploaded_audio:
        try:
            transcript = transcribe_audio(uploaded_audio, language_code=lang[1])
            st.success("Transcription:")
            st.write(transcript)
        except Exception as e:
            st.error(f"Error during transcription: {e}")

    st.subheader("Text-to-Speech")

    input_text = st.text_area("Enter text to synthesize", height=100, key="tts_input")
    if st.button("Synthesize"):
        if input_text.strip():
            try:
                audio_content = synthesize_speech(
                    input_text, language_code=lang[1], voice_name=voice_name
                )
                audio_b64 = audio_bytes_to_base64(audio_content)
                st.audio(audio_content, format="audio/mp3")
                st.markdown(f'<audio controls src="{audio_b64}"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during synthesis: {e}")
        else:
            st.warning("Please enter some text to synthesize.")

    if st.button("Change Language"):
        st.session_state.language_selected = False