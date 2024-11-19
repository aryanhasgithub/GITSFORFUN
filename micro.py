import serial
import speech_recognition as sr
import pyttsx3
import os
from groq import Groq  # Import the Groq class

# Initialize TTS (Text-to-Speech)
tts = pyttsx3.init()
recognizer = sr.Recognizer()

# Set up serial communication with micro:bit
ser = serial.Serial('COM3', 115200)  # Replace 'COM3' with your actual port

# Initialize GroqCloud API
client = Groq(api_key="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")


# Function to query GroqCloud AI
def query_groqcloud(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"{text} ."}
            ],
            model="llama3-8b-8192"  # Use the correct model name
        )
        response = chat_completion.choices[0].message.content.strip()
        return response
    except Exception as e:
        print(f"Error with GroqCloud: {e}")
        return "ERROR"

# Function to capture audio and query AI
def capture_audio():
    with sr.Microphone() as source:
        print("Listening for query...")
        recognizer.adjust_for_ambient_noise(source)
        print("You can speak now...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            query_text = recognizer.recognize_google(audio)
            print(f"User said: {query_text}")

            # Send the query to GroqCloud and get the response
            ai_response = query_groqcloud(query_text)
            print(f"AI Response: {ai_response}")

            # Speak out the AI's response
            tts.say(ai_response)
            tts.runAndWait()

            # Send the response back to the micro:bit via serial
            ser.write(ai_response.encode())  # Send response as bytes
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            ser.write("Could not understand audio".encode())
        except sr.RequestError as e:
            print(f"Error with Speech Recognition: {e}")
            ser.write("Error with recognition".encode())
        except Exception as e:
            print(f"Error during listening: {e}")
            ser.write("Error during listening".encode())

# Main loop to listen for start/stop signal from micro:bit
listening = False
print("Serial communication started.")

while True:
    if ser.in_waiting > 0:
        # Read raw data from serial and decode it
        raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"Raw data received: {repr(raw_data)}")
        
        # Replace any '\\n' with an empty string to handle literal backslash sequences
        processed_command = raw_data.replace("\\n", "").strip()
        print(f"Processed command: {repr(processed_command)}")

        if processed_command == "start":
            print("Start command received.")
            listening = True
            capture_audio()
        elif processed_command == "stop":
            print("Stop command received.")
            listening = False
        else:
            print(f"Unknown command received: {repr(processed_command)}")
