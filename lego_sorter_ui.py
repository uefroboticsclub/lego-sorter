sudo apt update
sudo apt install python3-pyqt6 python3-opencv python3-pip -y
pip3 install requests numpy


import sys
import cv2
import requests
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import Qt, QTimer
from urllib.request import urlopen

class LegoSorterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LEGO Sorter - Real-Time Detection")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("background-color: #0b0c10; color: #66fcf1; font-size: 18px;")

        # Layout
        self.layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("🚀 LEGO SORTER AI SYSTEM 🚀")
        self.title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #45a29e;")
        self.layout.addWidget(self.title_label)

        # Sorting Process Visualization
        self.process_label = QLabel("Processing... Identifying LEGO Piece 🔍")
        self.process_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.process_label.setStyleSheet("color: #f8f8f2; font-size: 16px;")
        self.layout.addWidget(self.process_label)

        # Images Section
        self.images_layout = QHBoxLayout()

        # Captured Camera Image
        self.camera_label = QLabel("Capturing LEGO Piece...")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setStyleSheet("border: 2px solid #45a29e; padding: 5px;")
        self.images_layout.addWidget(self.camera_label)

        # API Response Image
        self.api_image_label = QLabel("Fetching LEGO Model...")
        self.api_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.api_image_label.setStyleSheet("border: 2px solid #45a29e; padding: 5px;")
        self.images_layout.addWidget(self.api_image_label)

        self.layout.addLayout(self.images_layout)

        # Detected Part Info
        self.part_label = QLabel("Detected Part: Processing... 🔄")
        self.part_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.part_label.setStyleSheet("color: #ffcc00; font-size: 20px;")
        self.layout.addWidget(self.part_label)

        self.setLayout(self.layout)

        # Timer for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_detection)
        self.timer.start(3000)  # every 3 seconds

        self.update_detection()  # initial update

    def capture_image(self, filename="lego_piece.jpg"):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            cap.release()
            return filename, frame
        else:
            cap.release()
            return None, None

    def send_to_api(self, image_path):
        if not image_path:
            return None
        url = "https://api.brickognize.com/predict/"
        files = {"query_image": (image_path, open(image_path, "rb"), "image/jpeg")}
        headers = {"accept": "application/json"}

        try:
            response = requests.post(url, files=files, headers=headers)
            return response.json()
        except Exception as e:
            print("API error:", e)
            return None

    def update_detection(self):
        self.process_label.setText("🔄 Capturing image and analyzing...")
        image_path, frame = self.capture_image()

        if frame is not None:
            self.display_camera_image(frame)

        data = self.send_to_api(image_path)

        if data and "items" in data and len(data["items"]) > 0:
            part = data["items"][0]
            part_id = part.get("id", "Unknown")
            part_name = part.get("name", "Unknown")
            img_url = part.get("img_url", "")

            self.part_label.setText(f"🧱 {part_name} (ID: {part_id})")
            self.process_label.setText("✅ LEGO Part Identified!")
            self.display_api_image(img_url)
        else:
            self.part_label.setText("❌ No valid LEGO part detected.")
            self.process_label.setText("Retrying...")

    def display_camera_image(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.camera_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

    def display_api_image(self, url):
        try:
            image_data = urlopen(url).read()
            qimg = QImage()
            qimg.loadFromData(image_data)
            pixmap = QPixmap.fromImage(qimg)
            self.api_image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            print("Error loading API image:", e)
            self.api_image_label.setText("Failed to load API image.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LegoSorterUI()
    window.show()
    sys.exit(app.exec())
