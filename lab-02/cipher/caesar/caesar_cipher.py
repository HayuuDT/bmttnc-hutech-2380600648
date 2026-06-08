from cipher.caesar import ALPHABET 

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def validate_inputs(self, text: str, key: int):
        """Phương thức ràng buộc cho Caesar Cipher"""
        if not text:
            raise ValueError("Văn bản đầu vào không được để trống.")
        
        # Kiểm tra kiểu dữ liệu của key
        if not isinstance(key, int):
            raise ValueError("Khóa (Key) của Caesar phải là một số nguyên.")
            
        # Kiểm tra khoảng giá trị toán học
        if key < 0 or key > 25:
            raise ValueError("Khóa (Key) của Caesar bắt buộc phải nằm trong khoảng từ 0 đến 25.")

    def encrypt_text(self, text: str, key: int) -> str:
        self.validate_inputs(text, key) # Gọi kiểm tra ràng buộc
        
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypted_text = []
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index + key) % alphabet_len
                output_letter = self.alphabet[output_index]
                encrypted_text.append(output_letter)
            else:
                encrypted_text.append(letter)
        return "".join(encrypted_text)
    
    def decrypt_text(self, text: str, key: int) -> str:
        self.validate_inputs(text, key) # Gọi kiểm tra ràng buộc
        
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypted_text = []
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index - key) % alphabet_len
                output_letter = self.alphabet[output_index]
                decrypted_text.append(output_letter)
            else:
                decrypted_text.append(letter)
        return "".join(decrypted_text)