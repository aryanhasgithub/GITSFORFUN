import cv2
import face_recognition

# Load and encode known faces (Aryan, Sarita, and New Person)
aryan_image = face_recognition.load_image_file("aryan.jpg")
sarita_image = face_recognition.load_image_file("sarita.jpg")
new_person_image = face_recognition.load_image_file("parveen.jpg")  # Replace with actual image path

# Generate encodings for Aryan, Sarita, and New Person
aryan_encoding = face_recognition.face_encodings(aryan_image)[0]
sarita_encoding = face_recognition.face_encodings(sarita_image)[0]
new_person_encoding = face_recognition.face_encodings(new_person_image)[0]

# Known faces and corresponding names
known_face_encodings = [aryan_encoding, sarita_encoding, new_person_encoding]
known_face_names = ["Aryan", "Sarita", "parveen"]

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to capture image")
        break

    # Convert the image from BGR (OpenCV default) to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop over each detected face
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the detected face with the known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"  # Default name if no match is found

        # If a match is found, assign the corresponding name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the name of the person on the frame
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Print the recognized name to the console
        if name != "Unknown":
            print(f"Recognized: {name}")

    # Display the resulting frame with recognized faces
    cv2.imshow('Video', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()
