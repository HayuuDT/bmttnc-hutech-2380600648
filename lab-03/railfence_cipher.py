import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests
from ui.railfence import Ui_MainWindow 

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def validate_inputs(self, text, key):
        """Phương thức ràng buộc dữ liệu đầu vào cho Rail Fence"""
        if not text.strip():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản không được để trống!")
            return False
            
        if not key.strip():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) không được để trống!")
            return False
            
        if not key.isdigit():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa Rail Fence (Số hàng) phải là một số nguyên!")
            return False
            
        if int(key) < 2:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa Rail Fence phải lớn hơn hoặc bằng 2!")
            return False
            
        return True

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key = self.ui.txt_key.text()
        
        if not self.validate_inputs(plain_text, key):
            return

        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": int(key) # Chuyển đổi sang int
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Rail Fence Successfully")
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

        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": int(key) # Chuyển đổi sang int
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Rail Fence Successfully")
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