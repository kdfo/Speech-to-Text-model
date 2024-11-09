import pyttsx3
import speech_recognition as sr
import os
import socket
import streamlit as st

# Function to listen for audio input
def listen(duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.record(source, duration=duration)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Didn't hear perfectly!"
        except sr.RequestError:
            return "Could not request results; check your internet connection."

# Function to speak text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to save text to file
def save_text(filename, text):
    if os.path.exists(f"{filename}.txt"):
        st.error("File with this name already exists")
        speak("File with this name already exists")
    else:
        with open(f"{filename}.txt", "w") as file:
            file.write(text)
        st.success("File saved successfully")
        speak("File saved successfully")

# Streamlit app layout
st.title("Speech Processing App")
st.write("This app allows you to transcribe speech, speak text, and save it to a file.")

# Check internet connection
if socket.gethostbyname(socket.gethostname()) == "127.0.0.1":
    st.error("Your device is not connected to the internet.")
else:
    if st.button("Activate Microphone"):
        text = listen(5)
        st.text_area("Transcribed Text", value=text, height=100)

    # Text area for input
    user_text = st.text_area("Enter text here")

    # Speak button
    if st.button("Speak"):
        speak(user_text)

    # Save button
    filename = st.text_input("Enter filename to save text")
    if st.button("Save") and filename:
        save_text(filename, user_text)
