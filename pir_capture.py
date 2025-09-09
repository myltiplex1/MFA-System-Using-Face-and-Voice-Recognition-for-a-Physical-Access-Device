import digitalio
import board
import time
from image_capture import capture_img
from display_utils import init_display, display_text  # Import the display functions

def motion_img():
    # Set up the PIR pin as a digital input using digitalio
    pir_pin = digitalio.DigitalInOut(board.D6)  # Use D6 instead of GPIO pin 7
    pir_pin.direction = digitalio.Direction.INPUT

    # Initialize display (assuming the display is initialized here)
    try:
        disp, width, height = init_display()
    except Exception as e:
        print(f"Error initializing display: {e}")
        return None

    try:
        while True:
            if pir_pin.value:  # Check for motion detected
                print("Motion detected! Waiting...")
                
                # Display message for face placement
                display_text(disp, "Hello, Place your\nface in front of\nthe camera and wait", width, height)
                time.sleep(3)  # Wait for 3 seconds after motion is detected

                # Capture the image after displaying the message
                image = capture_img()
                if image is not None:
                    print("Image captured!")
                    display_text(disp, "Image Captured", width, height)
                    time.sleep(1)
                    return image
            else:
                print("No motion detected")
                display_text(disp, "Waiting.....", width, height)
                
            time.sleep(1)  # Delay to avoid rapid printing

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pir_pin.deinit()  # Clean up the PIR pin on exit


