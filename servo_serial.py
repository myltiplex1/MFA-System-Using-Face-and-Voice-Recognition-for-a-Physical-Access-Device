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

# Initialize serial communication with ESP8266
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)  # Adjust the port to match your connection

# Load the known faces and embeddings
with open('final_model1.pkl', 'rb') as f:
    Names = pickle.load(f)
    Encodings = pickle.load(f)

# Function to save the captured image
def save_image(image, filename="image.jpg"):
    cv2.imwrite(filename, image)

# Function to display image on the screen
def display_image_on_display(image_path, disp, width, height):
    image = Image.open(image_path)
    # Resize and crop to fit the display
    image = image.resize((width, height), Image.BICUBIC)
    disp.image(image)

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

                    display_text(disp, f"Name: {name}", width, height)
                    time.sleep(3)

                    if name != "Unknown":
                        display_text(disp, f"Welcome {name}", width, height)
                        time.sleep(3)

                        # Send 'Open' message to ESP8266
                        ser.write(b'Open\n')
                        display_text(disp, "Door Opening...", width, height)

                        # Wait for response from ESP8266 (for door closure)
                        response = ser.readline().decode('utf-8').strip()
                        if response == "Closed":
                            time.sleep(5)
                            display_text(disp, "Door Closed", width, height)
                            print("Door is closed, going back to motion detection.")
                        else:
                            print(f"Unexpected response from ESP8266: {response}")
                    else:
                        display_text(disp, "Access Denied", width, height)

                else:
                    display_text(disp, "No face detected.\nPlease, position\nyour face clearly", width, height)
                    time.sleep(3)

                time.sleep(3)
                display_text(disp, "", width, height)

            else:
                display_text(disp, "Face Recognition\nWaiting...", width, height)
                time.sleep(1)

    finally:
        ser.close()  # Close the serial connection
        display_text(disp, "", width, height)

if __name__ == "__main__":
    main()

