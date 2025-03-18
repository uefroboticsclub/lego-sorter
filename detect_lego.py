import cv2
import requests

# Capture image from webcam and save as JPG
def capture_image(filename="lego_piece.jpg"):
    cap = cv2.VideoCapture(0)  # Change index if using multiple cameras
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Camera failed to capture an image.")
        cap.release()
        return None

    # Convert and save image as a valid JPEG
    cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    
    cap.release()
    return filename

# Send image to API
def send_to_api(image_path):
    if image_path is None:
        print("Error: No valid image to send.")
        return

    url = "https://api.brickognize.com/predict/"
    files = {"query_image": (image_path, open(image_path, "rb"), "image/jpeg")}
    headers = {"accept": "application/json"}

    response = requests.post(url, files=files, headers=headers)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: API did not return valid JSON.")
        return None

# Run detection
image_path = capture_image()
data = send_to_api(image_path)

if data:
    print("\nDetected LEGO Piece:")
    print(data)
else:
    print("Error: No valid response from API.")
