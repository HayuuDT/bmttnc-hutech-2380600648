class PlayFairCipher:
    def __init__(self):
        pass

    def validate_key(self, key):
        """Kiểm tra tính hợp lệ của khóa Playfair"""
        if not key:
            raise ValueError("Khóa không được để trống.")
        # Loại bỏ khoảng trắng tạm thời để kiểm tra ký tự chữ cái
        clean_key = key.replace(" ", "")
        if not clean_key.isalpha():
            raise ValueError("Khóa của Playfair phải là chuỗi chỉ chứa chữ cái.")

    def create_playfair_matrix(self, key):
        self.validate_key(key)
        
        key = key.replace(" ", "") # Loại bỏ khoảng trắng trong khóa nếu có
        key = key.replace("J", "I") # Chuyển "J" thành "I" trong khóa
        key = key.upper()
        
        # Loại bỏ các ký tự trùng lặp để giữ đúng thứ tự bảng chữ cái ma trận
        seen = set()
        matrix = []
        for letter in key:
            if letter not in seen:
                seen.add(letter)
                matrix.append(letter)
                
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [letter for letter in alphabet if letter not in seen]

        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break

        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError(f"Ký tự '{letter}' không nằm trong ma trận Playfair.")

    def playfair_encrypt(self, plain_text, matrix):
        if not plain_text:
            raise ValueError("Văn bản mã hóa không được để trống.")
            
        # Chuyển "J" thành "I" trong văn bản đầu vào
        plain_text = plain_text.replace("J", "I")
        # Giữ lại các chữ cái thuộc ma trận
        plain_text = "".join([c.upper() for c in plain_text if c.upper() in "ABCDEFGHIKLMNOPQRSTUVWXYZ"])
        
        if not plain_text:
            raise ValueError("Văn bản sau khi làm sạch không chứa chữ cái hợp lệ để mã hóa.")
            
        encrypted_text = ""
        i = 0
        while i < len(plain_text):
            # Lấy cặp ký tự
            c1 = plain_text[i]
            if i + 1 < len(plain_text):
                c2 = plain_text[i+1]
                if c1 == c2:
                    # Nếu 2 ký tự trùng nhau, chèn thêm 'X'
                    c2 = "X"
                    i += 1
                else:
                    i += 2
            else:
                c2 = "X"
                i += 1
                
            row1, col1 = self.find_letter_coords(matrix, c1)
            row2, col2 = self.find_letter_coords(matrix, c2)
            
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        if not cipher_text:
            raise ValueError("Văn bản giải mã không được để trống.")
            
        cipher_text = "".join([c.upper() for c in cipher_text if c.upper() in "ABCDEFGHIKLMNOPQRSTUVWXYZ"])
        if len(cipher_text) % 2 != 0:
            raise ValueError("Mã cipher của Playfair hợp lệ phải có độ dài là số chẵn.")
            
        decrypted_text = ""
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        banro = ""
        for i in range(0, len(decrypted_text)-2, 2):
            if decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + decrypted_text[i+1]

        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2] + decrypted_text[-1]
        return banro