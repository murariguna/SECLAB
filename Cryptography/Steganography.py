print("Welcome to the Steganography Tool!")
print("This tool allows you to hide a message inside an image using LSB steganography and retrieve it with a password.")

import cv2
import os

def encode_lsb(image, msg):
    width, height, _ = image.shape
    message_bits = ''.join(format(ord(c), '08b') for c in msg)
    data_len = len(message_bits)
    bit_idx = 0
    
    for row in range(height):
        for col in range(width):
            for channel in range(3):
                if bit_idx < data_len:
                    image[row, col, channel] &= 0b11111110 
                    image[row, col, channel] |= int(message_bits[bit_idx])  
                    bit_idx += 1
    return image

def decode_lsb(image, msg_length):
    width, height, _ = image.shape
    message_bits = []
    bit_idx = 0
    
    for row in range(height):
        for col in range(width):
            for channel in range(3):
                if bit_idx < msg_length * 8:  
                    message_bits.append(str(image[row, col, channel] & 1))  
                    bit_idx += 1
    
    message_bits = ''.join(message_bits)
    message = ''.join(chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8))
    return message

try:
    img_filename = "mypic.jpg"
    img = cv2.imread(img_filename)
    if img is None:
        raise FileNotFoundError("Error: Image not Present in the given Directory.")
    
    msg = input("Enter message: ")
    if not msg:
        raise ValueError("Error: Message cannot be empty.")
        
    password = input("Enter password: ")
    if not password:
        raise ValueError("Error: Password cannot be empty.")

    if len(msg) * 8 > img.size:
        raise ValueError("Error: Message too long for this image.")
    
    encoded_img = encode_lsb(img, msg)
    cv2.imwrite("Encryptedmsg.jpg", encoded_img)
    os.system("start Encryptedmsg.jpg")
    
    pas = input("Enter password for decryption: ")
    if password == pas:
        decrypted_msg = decode_lsb(encoded_img, len(msg))
        print("Decrypted message: ", decrypted_msg)
    else:
        print("Invalid password.")

except Exception as e:
    print(e)
