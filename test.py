import serial
import time

# Initialize serial communication with the micro:bit
ser = serial.Serial('COM3', 115200)  # Replace 'COM3' with your actual port

print("Serial communication started.")

while True:
    if ser.in_waiting > 0:
        # Read the command and decode it
        raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"Raw data received: {repr(raw_data)}")  # Debug raw data
        
        # Replace any '\\n' with an empty string to handle literal backslash sequences
        processed_command = raw_data.replace("\\n", "").strip()
        print(f"Processed command: {repr(processed_command)}")  # Debug processed command
        
        # Compare the processed command
        if processed_command == "start":
            print("Start command received.")
        elif processed_command == "stop":
            print("Stop command received.")
        else:
            print(f"Unknown command received: {repr(processed_command)}")
    
    time.sleep(0.1)  # Small delay to prevent overloading the CPU
