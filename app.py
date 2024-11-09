# app.py
import streamlit as st
import whisper
from pydub import AudioSegment
import tempfile

# Load Whisper model
model = whisper.load_model("base")  # Change model size if needed

st.title("Speech-to-Text AI Model")
st.write("Upload an audio file, and this app will transcribe the speech to text.")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])

def transcribe_audio(file_path):
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    result = model.transcribe(audio)
    return result['text']

if uploaded_file is not None:
    # Convert uploaded audio to WAV if necessary
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        if uploaded_file.type == "audio/wav":
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        else:
            # Convert to WAV format using pydub
            audio = AudioSegment.from_file(uploaded_file)
            audio.export(temp_file.name, format="wav")
            temp_file_path = temp_file.name

    # Transcribe audio
    st.write("Transcribing audio...")
    transcription = transcribe_audio(temp_file_path)
    
    # Display the transcription
    st.write("Transcription:")
    st.write(transcription)

    # Cleanup temporary file
    os.remove(temp_file_path)
