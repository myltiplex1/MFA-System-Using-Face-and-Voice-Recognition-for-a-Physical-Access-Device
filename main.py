import cv2
import time
import os
import numpy as np
import pickle
from pir_capture import motion_img  # Handles motion detection and image capture
from jetson_utils import cudaFromNumpy
import face_recognition
from display_utils import init_display, display_text
from PIL import Image
import serial
from audio import record_single_audio  # Handles audio recording
from audio_spec import save_audio_spectrogram  # Converts audio to spectrogram
from audio_pred import predict_image_class  # Predicts audio class from spectrogram

# Initialize serial communication with ESP8266
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)

# Load the known faces and embeddings
with open('face_model.pkl', 'rb') as f:
    Names = pickle.load(f)
    Encodings = pickle.load(f)

# Function to save the captured image
def save_image(image, filename="image.jpg"):
    cv2.imwrite(filename, image)

# Function to display image on the screen
def display_image_on_display(image_path, disp, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.BICUBIC)  # Resize and crop to fit the display
    disp.image(image)

def perform_voice_authentication(disp, width, height):
    """Perform voice authentication after face recognition."""
    for attempt in range(3):  # Allow up to 3 attempts
        attempts_left = 2 - attempt  # Calculate remaining attempts (2 - attempt number)
        
        display_text(disp, f"Audio verification\ninitialized.", width, height)
        time.sleep(2)

        display_text(disp, "Say the magic word.", width, height)
        record_single_audio()  # Record audio
        time.sleep(2)
        display_text(disp, "Audio recording\ncomplete.", width, height)
        time.sleep(1)

        display_text(disp, "Generating spectrogram.", width, height)
        time.sleep(1)
        save_audio_spectrogram()  # Save spectrogram
        display_text(disp, "Spectrogram saved.", width, height)
        time.sleep(1)

        display_text(disp, "Making prediction...", width, height)
        time.sleep(1)
        label, confidence = predict_image_class("audio_spec.jpg")  # Predict from spectrogram

        if label in ["David", "Enoch"]:
            display_text(disp, f"Access Granted\nWelcome {label}", width, height)
            return True  # Successful authentication
        elif label == "Noise":
            if attempt < 2:  # If not the final attempt
                display_text(disp, f"Voice not recognized.\n{attempts_left} attempts left.", width, height)
                time.sleep(3)
            else:
                display_text(disp, "Access Denied.\nToo many attempts.", width, height)
                time.sleep(3)
        else:
            display_text(disp, "Voice authentication\nfailed.", width, height)
            time.sleep(3)
            break

    return False  # Authentication failed

def main():
    # Initialize the display
    try:
        disp, width, height = init_display()
    except Exception as e:
        print(f"Error initializing display: {e}")
        return

    # Initial display message
    display_text(disp, "Face Recognition\nWaiting...", width, height)
    time.sleep(2)

    try:
        while True:
            # Capture image after motion is detected
            captured_image = motion_img()

            if captured_image is not None:
                save_image(captured_image, "image.jpg")
                display_text(disp, "Displaying captured\nimage...", width, height)
                time.sleep(2)

                display_image_on_display("image.jpg", disp, width, height)
                time.sleep(3)

                # Convert to RGB and detect faces
                rgb_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
                face_positions = face_recognition.face_locations(rgb_image, model='cnn')
                face_encodings = face_recognition.face_encodings(rgb_image, face_positions)

                if len(face_encodings) > 0:
                    face_encoding = face_encodings[0]
                    matches = face_recognition.compare_faces(Encodings, face_encoding)

                    name = "Unknown"
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = Names[first_match_index].split("_")[0]

                    if name != "Unknown":
                        display_text(disp, f"Face recognized:\n{name}", width, height)
                        time.sleep(3)

                        # Proceed to voice authentication
                        if perform_voice_authentication(disp, width, height):
                            # Send 'Open' message to ESP8266
                            ser.write(b'Open\n')
                            display_text(disp, "Door Opening...", width, height)

                            # Wait for response from ESP8266
                            response = ser.readline().decode('utf-8').strip()
                            if response == "Closed":
                                time.sleep(1)
                                display_text(disp, "Door Closed", width, height)
                                time.sleep(3)
                            else:
                                print(f"Unexpected response from ESP8266: {response}")
                        else:
                            display_text(disp, "Access Denied.", width, height)

                    else:
                        display_text(disp, "Access Denied.", width, height)

                else:
                    display_text(disp, "No face detected.\nPosition your face\nclearly.", width, height)
                    time.sleep(5)

                display_text(disp, "", width, height)

            else:
                display_text(disp, "Face Recognition\nWaiting...", width, height)
                time.sleep(3)

    finally:
        ser.close()  # Close the serial connection
        display_text(disp, "", width, height)

if __name__ == "__main__":
    main()

