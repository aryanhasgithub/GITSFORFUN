import serial
import time
from groq import Groq

# Set up Groq client
client = Groq(api_key="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")

# Set up serial communication with Arduino
serial_connection = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Wait for the serial connection to initialize

# Ask for a question and get the response from Groq
q = input("Enter question here: ")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": q + " Give answer in YES or NO, all capital letters.",
        }
    ],
    model="llama3-8b-8192",
)

response_content = chat_completion.choices[0].message.content.strip().upper()
print("Groq API response:", response_content)

# Send "YES" or "NO" to Arduino based on the response
if response_content == "YES":
    serial_connection.write(b"YES")  # Send "YES" command to Arduino
    print("Sent YES to Arduino")
elif response_content == "NO":
    serial_connection.write(b"NO")   # Send "NO" command to Arduino
    print("Sent NO to Arduino")
else:
    print("Unexpected response:", response_content)

# Close the serial connection
serial_connection.close()
