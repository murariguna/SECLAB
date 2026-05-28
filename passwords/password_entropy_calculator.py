print("\n\n   Welcome to the Password Entropy Calculator!")
print("   This tool calculates the entropy of a given password.")
import math 
def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in "!@#$%^&*()_+<>?{}[]|/.,-" for c in password):
        charset_size += 32
    if charset_size == 0:
        return 0
    entropy = len(password) * math.log2(charset_size)
    return entropy
password = input("  Enter a password to calculate its entropy: ")
if not password:
    print("  No password entered.")
else:
    entropy = calculate_entropy(password)
    print(f"  The entropy of the password is: {entropy:.2f} bits")

