print("Welcome to the Digital Signature Demo!")
print("This tool demonstrates how to create and verify digital signatures using RSA.")
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key
def sign_message(message, private_key):
    rsa_key = RSA.import_key(private_key)
    h = SHA256.new(message.encode())
    signature = pkcs1_15.new(rsa_key).sign(h)
    return signature
def verify_signature(message, signature, public_key):
    rsa_key = RSA.import_key(public_key)
    h = SHA256.new(message.encode())
    try:
        pkcs1_15.new(rsa_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
private_key, public_key = generate_keys()
print("Generated RSA keys.")
choice = input("Do you want to sign a message or verify a signature? (enter 'sign' or 'verify'): ").strip().lower()
if choice == "sign":
    message = input("Enter the message to sign: ")
    if not message:
        print("No message entered.")
    else:
        signature = sign_message(message, private_key)
        print(f"Message signed. Signature (hex): {signature.hex()}")
elif choice == "verify":
    message = input("Enter the message to verify: ")
    signature_hex = input("Enter the hexadecimal signature to verify: ")
    if not message or not signature_hex:
        print("No message or signature entered.")
    else:
        try:
            signature = bytes.fromhex(signature_hex)
            is_valid = verify_signature(message, signature, public_key)
            if is_valid:
                print("Signature is valid.")
            else:
                print("Signature is invalid.")
        except Exception as e:
            print(f"Error verifying signature: {e}")
else:
    print("Invalid choice. Please enter 'sign' or 'verify'.")
    