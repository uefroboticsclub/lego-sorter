import cv2

def capture_image(filename="lego_piece.jpg"):
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(filename, frame)
    camera.release()
    return filename