import cv2
import requests
import time

# Capture image from webcam
def capture_image(filename="lego_piece.jpg"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Camera failed to capture an image.")
        cap.release()
        return None

    cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    
    cap.release()
    return filename

# Send image to API
def send_to_api(image_path):
    if image_path is None:
        return None

    url = "https://api.brickognize.com/predict/"
    files = {"query_image": (image_path, open(image_path, "rb"), "image/jpeg")}
    headers = {"accept": "application/json"}

    try:
        response = requests.post(url, files=files, headers=headers)
        data = response.json()
        return data
    except requests.exceptions.JSONDecodeError:
        print("Error: API did not return valid JSON.")
        return None

# Run detection in a loop every 3 seconds
try:
    while True:
        image_path = capture_image()
        data = send_to_api(image_path)

        if data and "items" in data and len(data["items"]) > 0:
            first_part_id = data["items"][0]["id"]
            print(f"Detected LEGO Part ID: {first_part_id}")
        else:
            print("No valid LEGO part detected.")

        time.sleep(3)  # Wait 3 seconds before capturing the next image

except KeyboardInterrupt:
    print("\nStopping detection process.")
