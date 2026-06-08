import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def validate_inputs(self, text, key):
        """
        Phương thức ràng buộc dữ liệu đầu vào cho Caesar Cipher.
        Chặn text rỗng, key rỗng, key không phải số, và key ngoài khoảng 0-25.
        """
        if not text.strip():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Văn bản không được để trống!")
            return False
        
        if not key.strip():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa (Key) không được để trống!")
            return False
            
        # 1. Kiểm tra xem có phải là các ký số nguyên hay không
        if not key.isdigit():
            QMessageBox.warning(self, "Lỗi nhập liệu", "Khóa của Caesar phải là một số nguyên hợp lệ!")
            return False
            
        # 2. Kiểm tra giá trị toán học phải nằm trong khoảng từ 0 đến 25
        int_key = int(key)
        if int_key < 0 or int_key > 25:
            QMessageBox.warning(
                self, 
                "Lỗi nhập liệu", 
                f"Khóa Caesar phải nằm trong khoảng từ 0 đến 25!\n(Bạn đang nhập: {int_key})"
            )
            return False
            
        return True

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key = self.ui.txt_key.text()
        
        # Kiểm tra ràng buộc trước khi gọi API
        if not self.validate_inputs(plain_text, key):
            return

        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": int(key)  # Ép sang kiểu int để truyền qua json đúng chuẩn số
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Lỗi Server", f"API trả về mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Server: {e}")

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key = self.ui.txt_key.text()
        
        # Kiểm tra ràng buộc trước khi gọi API
        if not self.validate_inputs(cipher_text, key):
            return

        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": int(key)  # Ép sang kiểu int
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
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