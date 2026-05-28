print("Welcome to the RSA Demo!")
print("This tool demonstrates RSA encryption and decryption.")
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key
def encrypt_rsa(plain_text, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return cipher.encrypt(plain_text.encode())
def decrypt_rsa(cipher_text, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return cipher.decrypt(cipher_text).decode()
private_key, public_key = generate_keys()
print("Generated RSA keys.")    
choice = input("Do you want to encrypt or decrypt? (enter 'encrypt' or 'decrypt'): ").strip().lower()
if choice == "encrypt":
    plain_text = input("Enter the string to encrypt: ")
    if not plain_text:
        print("No string entered.")
    else:
        encrypted_data = encrypt_rsa(plain_text, public_key)
        print(f"Encrypted data (hex): {encrypted_data.hex()}")
elif choice == "decrypt":
    cipher_text_hex = input("Enter the hexadecimal string to decrypt: ")
    if not cipher_text_hex:
        print("No string entered.")
    else:
        try:
            cipher_text = bytes.fromhex(cipher_text_hex)
            decrypted_data = decrypt_rsa(cipher_text, private_key)
            print(f"Decrypted string: {decrypted_data}")
        except Exception as e:
            print(f"Error decrypting data: {e}")
else:
    print("Invalid choice. Please enter 'encrypt' or 'decrypt'.")

        