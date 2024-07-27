import speech_recognition as sr
import os
import pyttsx3
import google.generativeai as genai


def speech_to_text():
    # Initialize recognizer class (for recognizing speech)
    recognizer = sr.Recognizer()

    # Capture audio from the default microphone
    with sr.Microphone() as source:
        print("Listening... (Speak for 5 seconds)")
        # Adjust for ambient noise levels
        recognizer.adjust_for_ambient_noise(source)

        # Record audio for 5 seconds
        audio_data = recognizer.record(source, duration=5)

        # Use Google Web Speech API to perform speech recognition
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Question: {text}")
            genai.configure(api_key="AIzaSyBxHXH1MS-v0YVLazh5BFCBCQHC-50fHXg")

            # Create the model
            # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                # safety_settings = Adjust safety settings
                # See https://ai.google.dev/gemini-api/docs/safety-settings
            )

            chat_session = model.start_chat(
                history=[
                ]
            )
            inst = "Instruction : Talk like Iron Man, Reply as  Movie Star to audience, Limit to 100 words , Question is "
            response = chat_session.send_message(inst + text)

            print(response.text)

            engine = pyttsx3.init()
            engine.say(response.text)
            engine.runAndWait()


        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error fetching results; {e}")



speech_to_text()
