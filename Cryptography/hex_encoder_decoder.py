print("Welcome to the Hex Encoder/Decoder!")
print("This tool allows you to encode and decode hexadecimal strings.")
def encode_to_hex(input_string):    
    return input_string.encode("utf-8").hex()
def decode_from_hex(hex_string):
    try:
        bytes_object = bytes.fromhex(hex_string)
        return bytes_object.decode("utf-8")
    except Exception as e:
        return f"Error decoding hexadecimal string: {e}"
choice = input("Do you want to encode or decode? (enter 'encode' or 'decode'): ").strip().lower()
if choice == "encode":
    input_string = input("Enter the string to encode: ")
    if not input_string:
        print("No string entered.")
    else:
        encoded_string = encode_to_hex(input_string)
        print(f"Encoded hexadecimal string: {encoded_string}")
elif choice == "decode":
    hex_string = input("Enter the hexadecimal string to decode: ")
    if not hex_string:
        print("No hexadecimal string entered.")
    else:
        decoded_string = decode_from_hex(hex_string)
        print(f"Decoded string: {decoded_string}")
else:
    print("Invalid choice. Please enter 'encode' or 'decode'.")

        