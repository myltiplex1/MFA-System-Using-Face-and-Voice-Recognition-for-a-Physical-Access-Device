# image_capture.py
import cv2

def capture_img(camera_source='nvarguscamerasrc', width=1280, height=720, flip=2, dispW=640, dispH=480):
    if camera_source == 'nvarguscamerasrc':
        camSet = (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), width={width}, height={height}, format=NV12, framerate=21/1 '
            f'! nvvidconv flip-method={flip} ! video/x-raw, width={dispW}, height={dispH}, format=BGRx '
            f'! videoconvert ! video/x-raw, format=BGR ! appsink'
        )
    else:
        camSet = camera_source

    cam = cv2.VideoCapture(camSet)
    ret, frame = cam.read()

    cam.release()
    cv2.destroyAllWindows()

    if ret:
        return frame
    else:
        print('Error: Unable to capture image')
        return None

