class VigenereCipher:
    def __init__(self):
        pass

    def validate_inputs(self, text, key):
        """Phương thức ràng buộc cho Vigenere Cipher"""
        if not text:
            raise ValueError("Văn bản đầu vào không được để trống.")
        if not key:
            raise ValueError("Khóa không được để trống.")
        if not isinstance(key, str) or not key.isalpha():
            raise ValueError("Khóa của Vigenere phải là chuỗi ký tự liên tục và chỉ chứa chữ cái (A-Z, a-z).")

    def vigenere_encrypt(self, plain_text, key):
        self.validate_inputs(plain_text, key)
        
        encrypted_text = ""
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        self.validate_inputs(encrypted_text, key)
        
        decrypted_text = ""
        key_index = 0
        for char in encrypted_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)].upper()) - ord('A')
                if char.isupper():
                    decrypted_text += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text