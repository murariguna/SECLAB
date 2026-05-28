def is_common_password(password):
    with open("common_passwords.txt", "r" ,encoding="utf-8", errors="ignore") as file:
        data = file.read().splitlines()
    return password in data

print("\n====== PASSWORD COMMONNESS CHECKER ======\n")
print("This tool checks if a given password is common.\n")
password = input("Enter a password to check : ")
if not password:
    print("No password entered.")       
if is_common_password(password):
    print("This password is common and weak. Consider using a stronger password.")
else:   
    print("This password is not common. However, make sure to check its strength as well.")
