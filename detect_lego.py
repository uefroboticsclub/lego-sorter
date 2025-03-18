import cv2
import requests
import time

# Capture image from webcam and save as JPG
def capture_image(filename="lego_piece.jpg"):
    cap = cv2.VideoCapture(0)  # Use 0 for default camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Camera failed to capture an image.")
        cap.release()
        return None

    # Save the image as a valid JPEG
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

# Continuously capture and detect LEGO pieces
try:
    while True:
        image_path = capture_image()
        data = send_to_api(image_path)

        if data and "prediction" in data:
            print(f"Detected LEGO Part ID: {data['prediction']}")
        else:
            print("No valid LEGO part detected.")

        time.sleep(3)  # Wait 3 seconds before capturing the next image

except KeyboardInterrupt:
    print("\nStopping detection process.")



Detected LEGO Piece:
{'listing_id': '551d3d2cc552', 'bounding_box': {'left': 229.0087890625, 'upper': 349.59051513671875, 'right': 359.536865234375, 'lower': 439.36932373046875, 'image_width': 640.0, 'image_height': 480.0, 'score': 0.7006657123565674}, 'items': [{'id': '3001', 'name': 'Brick 2 x 4', 'img_url': 'https://storage.googleapis.com/brickognize-static/thumbnails-v2.9/part/3001/0.webp', 'external_sites': [{'name': 'bricklink', 'url': 'https://www.bricklink.com/v2/catalog/catalogitem.page?P=3001'}], 'category': 'Brick', 'type': 'part', 'score': 0.898294}, {'id': '3020', 'name': 'Plate 2 x 4', 'img_url': 'https://storage.googleapis.com/brickognize-static/thumbnails-v2.9/part/3020/0.webp', 'external_sites': [{'name': 'bricklink', 'url': 'https://www.bricklink.com/v2/catalog/catalogitem.page?P=3020'}], 'category': 'Plate', 'type': 'part', 'score': 0.5894171}]}

