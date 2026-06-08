class RailFenceCipher:
    def __init__(self):
        pass

    def validate_inputs(self, text, num_rails):
        """Phương thức ràng buộc cho Rail Fence Cipher"""
        if not text:
            raise ValueError("Văn bản đầu vào không được để trống.")
            
        if not isinstance(num_rails, int):
            raise ValueError("Số đường ray (Rails Key) phải là một số nguyên.")
            
        if num_rails < 2:
            raise ValueError("Số đường ray (Rails Key) phải có giá trị lớn hơn hoặc bằng 2.")

    def rail_fence_encrypt(self, plain_text, num_rails):
        self.validate_inputs(plain_text, num_rails)
        
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: down, -1: up
        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        self.validate_inputs(cipher_text, num_rails)
        
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(cipher_text[start:start + length])
            start += length

        plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            if not rails[rail_index]:  # Tránh lỗi chỉ mục nếu độ dài text quá ngắn
                break
            plain_text += rails[rail_index][0]
            rails[rail_index] = rails[rail_index][1:]
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return plain_text