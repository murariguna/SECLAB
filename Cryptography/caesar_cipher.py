print("Welcome to the Caesar Cipher!")
print("This tool allows you to encode and decode messages using the Caesar cipher.")

def encode_caesar(text, shift):
    encoded = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            encoded += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            encoded += char
    return encoded

def decode_caesar(text, shift):
    return encode_caesar(text, -shift)

choice = input("Do you want to encode or decode? (enter 'encode' or 'decode'): ").strip().lower()

if choice == "encode":
    input_text = input("Enter the string to encode: ")
    if not input_text:
        print("No string entered.")
    else:
        shift = int(input("Enter the shift value: "))
        encoded_string = encode_caesar(input_text, shift)
        print(f"Encoded string: {encoded_string}")

elif choice == "decode":
    input_text = input("Enter the string to decode: ")
    if not input_text:
        print("No string entered.")
    else:
        shift = int(input("Enter the shift value: "))
        decoded_string = decode_caesar(input_text, shift)
        print(f"Decoded string: {decoded_string}")

else:
    print("Invalid choice. Please enter 'encode' or 'decode'.")