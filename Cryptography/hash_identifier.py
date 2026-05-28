print("Welcome to the Hash Identifier!")
print("This tool identifies the hash type of a given hash value.")
import re   
def identify_hash(hash_value):
    hash_patterns = {
        "MD5": r"^[a-fA-F0-9]{32}$",
        "SHA-1": r"^[a-fA-F0-9]{40}$",
        "SHA-256": r"^[a-fA-F0-9]{64}$",
        "SHA-512": r"^[a-fA-F0-9]{128}$"
    }
    for hash_type, pattern in hash_patterns.items():
        if re.match(pattern, hash_value):
            return hash_type
    return "Unknown hash type"
hash_value = input("Enter a hash value to identify: ")
if not hash_value:
    print("No hash value entered.")     
else:
    hash_type = identify_hash(hash_value)
    print(f"The identified hash type is: {hash_type}")
    