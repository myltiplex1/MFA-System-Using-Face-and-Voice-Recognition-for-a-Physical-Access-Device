import face_recognition
import cv2
import os
import pickle

print(cv2.__version__)

Encodings = []
Names = []

image_dir = 'known'
for root, dirs, files in os.walk(image_dir):
    print(files)
    for file in files:
        path = os.path.join(root, file)
        print(path)
        name = os.path.splitext(file)[0]
        print(name)
        
        # Load the image
        person = face_recognition.load_image_file(path)
        
        # Try to get face encodings
        encodings = face_recognition.face_encodings(person)
        
        # Check if any faces were found
        if len(encodings) > 0:
            # Append the first encoding and the corresponding name
            encoding = encodings[0]
            Encodings.append(encoding)
            Names.append(name)
        else:
            # Print a message if no face was detected
            print(f"No face found in {file}")

print(Names)

with open('rain_model.pkl', 'wb') as f:
    pickle.dump(Names, f)
    pickle.dump(Encodings, f)

