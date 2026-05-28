import random
import pyautogui

chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+<>?{}[]\|/.,"
allchar= list(chars)
pwd=pyautogui.password("enter a password")
sample=""

while(sample!=pwd):
    sample = random.choices(allchar, k=len(pwd))
    print(sample)
    if sample == list(pwd):
        sample2=str(sample)
        print("your password is "+sample2)
        break