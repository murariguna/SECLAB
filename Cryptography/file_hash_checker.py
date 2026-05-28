print("Welcome to the File Hash Checker!")
print("This tool checks the integrity of a file by comparing its hash value.")
import hashlib
def calculate_file_hash(file_path):
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
                hash_sha1.update(chunk)
                hash_sha256.update(chunk)
        return {
            "MD5": hash_md5.hexdigest(),
            "SHA-1": hash_sha1.hexdigest(),
            "SHA-256": hash_sha256.hexdigest()
        }
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
        return None
file_path = input("Enter the file path to check: ")
if not file_path:
    print("No file path entered.")
else:   
    file_hashes = calculate_file_hash(file_path)
    if file_hashes:
        print(f"MD5: {file_hashes['MD5']}")
        print(f"SHA-1: {file_hashes['SHA-1']}")
        print(f"SHA-256: {file_hashes['SHA-256']}")
        