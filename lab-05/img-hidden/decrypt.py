import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""
    
    # Bước 1: Trích xuất tất cả các bit LSB từ các kênh màu của điểm ảnh
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]

    # Bước 2: Dịch chuỗi bit thành ký tự và kiểm tra chuỗi kết thúc của encrypt.py
    message = ""
    for i in range(0, len(binary_message), 8):
        # SỬA TẠI ĐÂY: Kiểm tra nếu gặp 16 bit đánh dấu kết thúc thì dừng lại ngay
        if binary_message[i:i+16] == '1111111111111110':
            break
            
        # Nếu chưa gặp ký hiệu kết thúc, tiến hành dịch 8 bit thành 1 ký tự chữ
        char = chr(int(binary_message[i:i+8], 2))
        message += char
        
    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
        
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()