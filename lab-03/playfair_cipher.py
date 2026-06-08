import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests
from ui.playfair import Ui_MainWindow 

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def validate_inputs(self, text, key):
        """Phương thức ràng buộc dữ liệu đầu vào cho Playfair"""
        if not text.strip():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản không được để trống!")
            return False
            
        if not key.strip():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) không được để trống!")
            return False
            
        # Loại bỏ khoảng trắng để kiểm tra chữ cái liên tục
        clean_key = key.replace(" ", "")
        if not clean_key.isalpha():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa của mã hóa Playfair chỉ được chứa chữ cái!")
            return False
            
        return True

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key = self.ui.txt_key.text()
        
        if not self.validate_inputs(plain_text, key):
            return

        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Playfair Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Lỗi Server", f"API trả về mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Server: {e}")

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key = self.ui.txt_key.text()
        
        if not self.validate_inputs(cipher_text, key):
            return

        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Playfair Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Lỗi Server", f"API trả về mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Server: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())