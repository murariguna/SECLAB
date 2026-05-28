print("Welcome to the AES Demo!")
print("This tool allows you to encrypt and decrypt messages using the AES cipher.")
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
def encrypt_aes(plain_text, key):
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    return cipher.iv + ct_bytes
def decrypt_aes(cipher_text, key):
    iv = cipher_text[:AES.block_size]
    ct = cipher_text[AES.block_size:]
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()
choice = input("Do you want to encrypt or decrypt? (enter 'encrypt' or 'decrypt'): ").strip().lower()
if choice == "encrypt":
    plain_text = input("Enter the string to encrypt: ")
    key = input("Enter the 16-character key: ")
    if not plain_text or not key:
        print("No string or key entered.")
    elif len(key) != 16:
        print("Key must be 16 characters long.")
    else:
        encrypted_data = encrypt_aes(plain_text, key)
        print(f"Encrypted data (hex): {encrypted_data.hex()}")
elif choice == "decrypt":
    cipher_text_hex = input("Enter the hexadecimal string to decrypt: ")
    key = input("Enter the 16-character key: ")
    if not cipher_text_hex or not key:
        print("No string or key entered.")
    elif len(key) != 16:
        print("Key must be 16 characters long.")
    else:
        try:
            cipher_text = bytes.fromhex(cipher_text_hex)
            decrypted_data = decrypt_aes(cipher_text, key)
            print(f"Decrypted string: {decrypted_data}")
        except Exception as e:
            print(f"Error decrypting data: {e}")
else:
    print("Invalid choice. Please enter 'encrypt' or 'decrypt'.")   
    