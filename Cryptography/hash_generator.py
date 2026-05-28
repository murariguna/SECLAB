print("   Welcome to the Hash Generator!")
print("   This tool generates a hash for a given password using SHA-256.")
import hashlib
def generate_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

password = input("   Enter a password to hash: ")
if not password:
    print("    No password entered.")
else:
    hash_value = generate_hash(password)
    print(f"    The SHA-256 hash of the password is: {hash_value}")
