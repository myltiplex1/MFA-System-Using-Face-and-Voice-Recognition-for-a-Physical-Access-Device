import digitalio
import board
from PIL import Image, ImageDraw
import adafruit_rgb_display.st7735 as st7735

def init_display():
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)

    BAUDRATE = 24000000
    spi = board.SPI()

    # Set display rotation for portrait mode
    disp = st7735.ST7735R(spi, rotation=0, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)

    # Determine width and height based on rotation
    if disp.rotation % 180 == 90:
        width = disp.height
        height = disp.width
    else:
        width = disp.width
        height = disp.height

    return disp, width, height

def show_image_on_display(disp, image_path, width, height):
    image = Image.open(image_path)

    # Resize and crop the image to fit the display
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width

    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop the image to center it
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display the image
    disp.image(image)

def display_text(disp, text, width, height):
    # Create a blank image with the correct dimensions
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    draw.text((10, height // 2), text, fill=(255, 255, 255))
    disp.image(image)

