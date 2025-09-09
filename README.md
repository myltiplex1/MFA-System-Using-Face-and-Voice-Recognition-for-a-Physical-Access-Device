# MFA Device — Face + Voice Multi-Factor Authentication

A multi-factor authentication (MFA) device combining face and voice recognition, designed to run on an NVIDIA Jetson Nano. The device requires both facial recognition and voice verification before granting physical access. It is intended for secure spaces such as labs, offices, and data centers.

---

## 🚀 Features
- Face recognition using a CSI or USB camera.
- Voice authentication using mel-spectrograms and a ResNet ONNX model.
- Training pipeline to build a database of known faces.
- PIR motion sensor to trigger recognition flow.
- 1.8" SPI TFT display for user feedback i.e Display messages and   captured images on an ST7735 RGB screen.
- Serial communication with ESP8266 to open/close the door via servo.
- Multi-step verification:
  1. Detect face → Recognize authorized person.
  2. Voice authentication → Say the "magic word".
  3. On success → Send `Open` command to ESP8266 to unlock.
---

## 📂 Project structure (summary)
- `main.py` — Main entry point / device orchestration  
- `train_faces.py` — Train and save face embeddings
- `pir_capture.py` — Motion detection and image capture  
- `display_utils.py` — TFT display initialization & text rendering  
- `audio.py` — Audio recording utilities  
- `audio_spec.py` — Convert audio to spectrogram  
- `audio_pred.py` — Predict speaker class from spectrogram  
- `known/` - Folder with known faces (images for training) 
- `model/voice/` — contain model and lebels.txt file
- `image_capture.py` — initialization of camera and image capture
- `face_model.pkl`  - a pkl file with saved embeddings (generated after training)
- `servo_serial.py` - test face recognition + servo serial communication
---

## 🔧 Setup & Training

### 1. Train Face Recognition Model
- Place images of known people inside the `known/` folder
- Train a face recognition model and save it as `face_model.pkl`.

```bash
python train_faces.py
```
### 2. Train / Use Voice Recognition Model
- Prepare dataset of spoken keywords or passphrases recording audio:

```bash
python audio.py
```
- Convert audio into spectrograms:

```bash
python audio_spec.py
```
- Train a ResNet model (export as .onnx)
- Save the model and labels in: 
    `model/voice/resnet.onnx`
    `model/voice/labels.txt`
- Classifies with:

```bash
python audio_pred.py
```
### 3. Configure Serial Communication
- ESP8266 listens for the Open command over serial.
- When access is granted: Jetson -> ESP8266: Open ESP8266 drives servo -> unlocks door ESP8266 -> Jetson: Closed when door is relocked
- Set the correct port in main.py:

```bash
import serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)
```
#### Notes:
- Replace /dev/ttyUSB0 with your actual serial port. On Windows this will be a COM port (for example COM3).
- Ensure the baud rate and timeout match the ESP8266's configuration.

## ⚙️ Software prerequisites (Jetson Nano)
- Python 3.6+ (or Python compatible with Jetson packages)
- face-recognition (requires dlib — install Jetson-compatible build)
- Packages (install on Jetson Nano):
  - cmake
  - gfortran
  - libopenblas-dev
  - liblapack-dev

Notes:
- dlib on Jetson often requires building from source or using a prebuilt wheel for Jetson;
- Save Python dependencies in `requirements.txt` and install with:
  ```bash
  python3 -m pip install -r requirements.txt
  ```

---

## 🔧 Hardware (suggested)
- NVIDIA Jetson Nano (4GB recommended)
- CSI camera or USB camera
- PIR motion sensor
- 1.8" TFT display (SPI)
- ESP8266 (serial interface) for lock control
- Servo motor or solenoid lock with relay
- USB microphone
- SD Card (64GB, high-speed)

### Example display pin connections
| Display Pin | Jetson Nano Pin |
|-------------|-----------------|
| GND         | GND             |
| VCC         | 3.3V / 5V       |
| LED         | 3.3V / 5V       |
| SCK         | Pin 23 (SCK)    |
| SDA (MOSI)  | Pin 19 (MOSI)   |
| A0 (DC)     | Pin 22 (D25)    |
| RESET       | Pin 18 (D24)    |
| CS          | Pin 24 (CE0)    |

---

## 🛠️ Useful commands (Jetson / Linux)
Video Devices
- List processes using camera device:
  ```bash
  sudo lsof /dev/video0
  ```

SPI Setup
- Load SPI and verify:
  ```bash
  sudo modprobe spidev
  lsmod | grep spi
  ls /dev/spidev*
  ```

Audio Devices
- List capture devices:
  ```bash
  arecord -l
  ```

Device troubleshooting tips:
- If camera missing, check `vcgencmd` / device tree overlays or use `v4l2-ctl --list-devices`.
- For audio issues, ensure PulseAudio/ALSA is configured and mic is detected.

---

## ▶️ Usage

1. Power up the Jetson Nano and connect all peripherals.
2. Ensure face embeddings model and the trained audio model files are present in the project root (or in configured model paths).
3. Run the main program:
   ```bash
   python3 main.py
   ```

Flow:
- PIR detects motion
- Camera captures image
- Face recognition → if matched, prompt for voice input
- Voice spectrogram classification → if matched, unlock door via ESP8266

---

## 🔒 Expected impact

This device strengthens security where single-factor authentication is insufficient.

Applications:
- Banks and financial institutions
- Data centers
- Research labs
- Secure offices and smart homes

---
