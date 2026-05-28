print("Welcome to the Vigenère Cipher!")
print("This tool allows you to encode and decode messages using the Vigenère cipher.")
def encode_vigenere(plain_text, key):
    encoded = ""
    key_length = len(key)
    key_index = 0
    for char in plain_text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            key_char = key[key_index % key_length].upper()
            shift = ord(key_char) - 65
            encoded += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            key_index += 1
        else:
            encoded += char
    return encoded

def decode_vigenere(cipher_text, key):
    decoded = ""
    key_length = len(key)
    key_index = 0
    for char in cipher_text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            key_char = key[key_index % key_length].upper()
            shift = ord(key_char) - 65
            decoded += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            key_index += 1
        else:
            decoded += char
    return decoded

choice = input("Do you want to encode or decode? (enter 'encode' or 'decode'): ").strip().lower()

if choice == "encode":
    plain_text = input("Enter the string to encode: ")
    key = input("Enter the key: ")
    if not plain_text or not key:
        print("No string or key entered.")
    else:
        encoded_string = encode_vigenere(plain_text, key)
        print(f"Encoded string: {encoded_string}")

elif choice == "decode":
    cipher_text = input("Enter the string to decode: ")
    key = input("Enter the key: ")
    if not cipher_text or not key:
        print("No string or key entered.")
    else:
        decoded_string = decode_vigenere(cipher_text, key)
        print(f"Decoded string: {decoded_string}")

else:
    print("Invalid choice. Please enter 'encode' or 'decode'.")
    