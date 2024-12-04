import pytesseract
from PIL import ImageGrab
import pyautogui
import time

# Update this path with the correct location of Tesseract on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Disable PyAutoGUI fail-safe (use with caution)
pyautogui.FAILSAFE = False

# Configure characters per minute (directly based on WPM)
WPM = 100
chars_per_second = WPM / 60  # Calculate characters per second for typing
delay_between_chars = 0.3  # Time delay between typing each character (adjust as needed)

time.sleep(5)
# Function to capture and process the text
def capture_text(region):
    # Capture the specified screen region
    screenshot = ImageGrab.grab(bbox=region)  # Adjust region (x1, y1, x2, y2)
    # Use Tesseract OCR to extract text
    text = pytesseract.image_to_string(screenshot, config='--psm 6')
    # Clean up the text by removing spaces and line breaks
    filtered_text = text.replace(' ', '').replace('\n', '')
    if filtered_text and filtered_text[0] == '[':
        filtered_text = filtered_text[1:]
    
    return filtered_text

# Main loop to capture and type text
def type_text(region, duration):
    start_time = time.time()  # Record the start time
    while time.time() - start_time < duration:  # Run for the specified duration
        # Capture the text
        captured_text = capture_text(region)
        if captured_text:
            print(f"Captured text: {captured_text}")  # Debugging/logging
            # Type the text character by character with a delay between each
            for char in captured_text:
                pyautogui.typewrite(char)
                time.sleep(delay_between_chars)  # Control typing speed
    print("Typing completed. Exiting program.")

# Define the region of the screen to capture (x1, y1, x2, y2)
region = (75, 334, 714, 507)  # Replace with your coordinates

# Set the duration of the program (in seconds)
duration = 30  # Stop after 30 seconds

# Start typing text
type_text(region, duration)
