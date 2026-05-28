print("Welcome to the URL Encoder/Decoder!")
print("This tool allows you to encode and decode URL strings.")
import urllib.parse
def encode_to_url(input_string):
    return urllib.parse.quote(input_string, safe='~()*!.\'')
def decode_from_url(url_string):
    return urllib.parse.unquote(url_string)
choice = input("Do you want to encode or decode? (enter 'encode' or 'decode'): ").strip().lower()
if choice == "encode":
    input_string = input("Enter the string to encode: ")
    if not input_string:
        print("No string entered.")
    else:
        encoded_string = encode_to_url(input_string)
        print(f"Encoded URL string: {encoded_string}")
elif choice == "decode":
    url_string = input("Enter the URL string to decode: ")
    if not url_string:
        print("No URL string entered.")
    else:
        decoded_string = decode_from_url(url_string)
        print(f"Decoded string: {decoded_string}")
else:
    print("Invalid choice. Please enter 'encode' or 'decode'.")
    