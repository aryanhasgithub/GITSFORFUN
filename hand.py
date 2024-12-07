import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Open webcam
cap = cv2.VideoCapture(0)

def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    
    # Flip and convert frame to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe Hands
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get landmarks
            landmarks = hand_landmarks.landmark

            # Extract relevant points (index finger tip, thumb tip, and middle finger tip)
            index_finger = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb = landmarks[mp_hands.HandLandmark.THUMB_TIP]
            middle_finger = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Convert normalized coordinates to screen coordinates
            index_finger_pos = (int(index_finger.x * screen_width), int(index_finger.y * screen_height))
            thumb_pos = (int(thumb.x * screen_width), int(thumb.y * screen_height))
            middle_finger_pos = (int(middle_finger.x * screen_width), int(middle_finger.y * screen_height))

            # Move mouse based on index finger position
            pyautogui.moveTo(index_finger_pos[0], index_finger_pos[1])

            # Detect thumb and middle finger touch for left click
            if calculate_distance((thumb.x, thumb.y), (middle_finger.x, middle_finger.y)) < 0.05:  # Increase threshold to 0.05
              pyautogui.click()

            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Hand Tracking Mouse", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
