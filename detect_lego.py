sudo apt update && sudo apt install python3-pip python3-opencv curl -y
pip3 install requests




import cv2
import requests

# Capture image from webcam
def capture_image(filename="lego_piece.jpg"):
    cap = cv2.VideoCapture(0)  # Use /dev/video0 if only one camera is connected
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    cap.release()
    return filename

# Send image to API
def send_to_api(image_path):
    url = "https://api.brickognize.com/predict/"
    files = {"query_image": open(image_path, "rb")}
    headers = {"accept": "application/json"}
    
    response = requests.post(url, files=files, headers=headers)
    return response.json()

# Run detection
image_path = capture_image()
data = send_to_api(image_path)

# Print result
print("\nDetected LEGO Piece:")
print(data)
