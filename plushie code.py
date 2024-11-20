import cv2
import base64
from groq import Groq
import time
import os
from gtts import gTTS
import pygame

# Set your API key for Groq
os.environ['GROQ_API_KEY'] = "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"

pygame.mixer.init()

# Initialize a counter for unique file names
file_counter = 1

# Function to capture and encode image using OpenCV
def capture_and_encode_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        cap.release()
        return None

    # Encode image to Base64
    _, img_encoded = cv2.imencode('.jpg', frame)
    base64_image = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

    cap.release()  # Release the webcam
    return base64_image

# Function to recognize the image using Groq API
def recognize_image(base64_image):
    client = Groq(api_key="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")

    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Please describe the contents of this image in a short and crisp manner. not more than five lines"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ]
        }],
        model="llama-3.2-11b-vision-preview",
    )

    response_message = chat_completion.choices[0].message.content
    return response_message

# Function to speak the description using gTTS
def speak_text(text):
    global file_counter

    # Create a unique file path for each audio file
    file_path = f"C:\\Users\\aryan\\projects\\description_{file_counter}.mp3"

    # Convert text to speech and save as MP3
    tts = gTTS(text=text, lang='en')
    tts.save(file_path)

    # Load and play the saved audio file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Increment the counter for the next run
    file_counter += 1

# Main loop to capture and recognize images every 10 seconds
while True:
    base64_image = capture_and_encode_image()
    if base64_image:
        description = recognize_image(base64_image)
        print("Description:", description)
        speak_text(description)
    
    # Wait for 10 seconds before capturing the next image
    time.sleep(10)
