def check_strength(password):
    score = 0
    if len(password) > 8:
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.islower() for char in password):
        score += 1  
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in password):
        score += 1  
    if score <= 2:
        return "Weak"  
    elif score == 3:
        return "Moderate"
    else:        
        return "Strong"    
    

print("\n====== PASSWORD STRENGTH CHECKER ======\n")
print("This tool checks the strength of a given password.\n")
password = input("Enter a password to check its strength: ")
if not password:
    print("No password entered.")
with open("common_passwords.txt", "r" ,encoding="utf-8", errors="ignore") as file:
    data = file.read().splitlines()

if password in data:
    print("Weak and Common Password")
else:
    strength = check_strength(password)    
    print(f"Password Strength: {strength}")
