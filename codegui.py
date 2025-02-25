import sys
import cv2
import numpy as np
pip install PyQt6

try:
    from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QVBoxLayout
except ModuleNotFoundError:
    print("Error: PyQt6 is not installed. Install it using 'pip install PyQt6'")
    sys.exit(1)

class ImageEncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.imagePath = None  # Ensure imagePath is always defined
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Image Encryption")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Select an image:", self)
        self.btnBrowse = QPushButton("Browse", self)
        self.btnBrowse.clicked.connect(self.loadImage)

        self.msgLabel = QLabel("Enter secret message:", self)
        self.msgInput = QLineEdit(self)
        
        self.encryptButton = QPushButton("Encrypt Image", self)
        self.encryptButton.clicked.connect(self.encryptImage)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btnBrowse)
        layout.addWidget(self.msgLabel)
        layout.addWidget(self.msgInput)
        layout.addWidget(self.encryptButton)
        self.setLayout(layout)
    
    def loadImage(self):
        options = QFileDialog.Option()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)", options=options)
        if filePath:
            self.imagePath = filePath
            self.label.setText(f"Image: {filePath}")
    
    def encryptImage(self):
        if not self.imagePath:
            QMessageBox.warning(self, "Warning", "Please select an image.")
            return

        secretMessage = self.msgInput.text()
        if not secretMessage:
            QMessageBox.warning(self, "Warning", "Please enter a secret message.")
            return
        
        image = cv2.imread(self.imagePath)
        
        message_bytes = secretMessage.encode('utf-8') + b'\0'
        binary_message = ''.join(format(byte, '08b') for byte in message_bytes)
        data_index = 0

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                for k in range(3):
                    if data_index < len(binary_message):
                        image[i, j, k] = (image[i, j, k] & 0xFE) | int(binary_message[data_index])
                        data_index += 1

        savePath, _ = QFileDialog.getSaveFileName(self, "Save Encrypted Image", "encryptedImage.png", "Images (*.png)")
        if savePath:
            cv2.imwrite(savePath, image)
            QMessageBox.information(self, "Success", f"Image encrypted successfully!\nSaved at: {savePath}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEncryptionApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Application closed successfully.")
