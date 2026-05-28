print("Welcome to the Secure File Encryptor!")
print("This tool allows you to encrypt and decrypt files securely using AES encryption.")
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    with open(file_path + '.enc', 'wb') as f:
        f.write(cipher.iv + ct_bytes)
    print(f"File encrypted successfully: {file_path}.enc")
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        ct = f.read()
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(ct), AES.block_size)
    with open(file_path[:-4], 'wb') as f:
        f.write(data)
    print(f"File decrypted successfully: {file_path[:-4]}")
choice = input("Do you want to encrypt or decrypt a file? (enter 'encrypt' or 'decrypt'): ").strip().lower()
if choice == "encrypt":
    file_path = input("Enter the path of the file to encrypt: ")
    key = input("Enter the 16-character key: ")
    if not file_path or not key:
        print("No file path or key entered.")
    elif len(key) != 16:
        print("Key must be 16 characters long.")
    else:
        try:
            encrypt_file(file_path, key)
        except Exception as e:
            print(f"Error encrypting file: {e}")
elif choice == "decrypt":
    file_path = input("Enter the path of the file to decrypt (must end with .enc): ")
    key = input("Enter the 16-character key: ")
    if not file_path or not key:
        print("No file path or key entered.")
    elif len(key) != 16:
        print("Key must be 16 characters long.")
    elif not file_path.endswith('.enc'):
        print("File must have a .enc extension.")
    else:
        try:
            decrypt_file(file_path, key)
        except Exception as e:
            print(f"Error decrypting file: {e}")
else:
    print("Invalid choice. Please enter 'encrypt' or 'decrypt'.")
    