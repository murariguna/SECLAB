print("Welcome to the Base64 Encoder/Decoder!")
print("This tool allows you to encode and decode Base64 strings.")
import base64
def encode_to_base64(input_string):
    encoded_bytes = base64.b64encode(input_string.encode("utf-8"))
    return encoded_bytes.decode("utf-8")
def decode_from_base64(encoded_string):
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        return decoded_bytes.decode("utf-8")
    except Exception as e:
        return f"Error decoding Base64 string: {e}"
choice = input("Do you want to encode or decode? (enter 'encode' or 'decode'): ").strip().lower()
if choice == "encode":
    input_string = input("Enter the string to encode: ")
    if not input_string:
        print("No string entered.")
    else:
        encoded_string = encode_to_base64(input_string)
        print(f"Encoded Base64 string: {encoded_string}")
elif choice == "decode":
    encoded_string = input("Enter the Base64 string to decode: ")
    if not encoded_string:
        print("No Base64 string entered.")
    else:
        decoded_string = decode_from_base64(encoded_string)
        print(f"Decoded string: {decoded_string}")
else:
    print("Invalid choice. Please enter 'encode' or 'decode'.") 
    