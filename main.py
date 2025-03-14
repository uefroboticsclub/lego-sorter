from camera.capture_image import capture_image
from api.send_to_api import send_to_api
from control.servo_control import move_paddle
import time

image_path = capture_image()
data = send_to_api(image_path)
lego_type = data.get("prediction", "Unrecognized")
print(f"Detected LEGO Type: {lego_type}")
if lego_type != "Unrecognized":
    time.sleep(3)  # Adjust timing based on conveyor speed
    move_paddle()