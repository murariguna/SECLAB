import string
import secrets

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):

    characters = ""

    if use_upper:
        characters += string.ascii_uppercase

    if use_lower:
        characters += string.ascii_lowercase

    if use_digits:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "Error: No character types selected."

    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password


def random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

print("\n====== PASSWORD GENERATOR ======\n")
print("This tool generates a random password based on your preferences.\n")
print("1. Custom Password")
print("2. Random Password")
choice = input("Choose an option (1 or 2): ")
if choice == '1':
    length = int(input("Enter password length: "))
    upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    digits = input("Include numbers? (y/n): ").lower() == 'y'
    symbols = input("Include symbols? (y/n): ").lower() == 'y'
    password = generate_password(length, upper, lower, digits, symbols)
elif choice == '2':
    length = int(input("Enter password length: "))
    number_of_passwords = int(input("How many passwords to generate? "))
    for i in range(1,number_of_passwords+1):
        password = random_password(length)
        print(f" {i} Generated Password: {password}")
else:
    print("Invalid option.")
    password = None

