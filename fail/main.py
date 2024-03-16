#Yoink os
import time
import os

os.system("cls")
time.sleep(0.2)
ask = input("Already have an account?")
if ask == "yes":
    time.sleep(2)
    os.startfile("os.py")
elif ask == "Yes":
    time.sleep(2)
    os.startfile("os.py")

elif ask == "Y":
    time.sleep(2)
    os.startfile("os.py")

elif ask == "y":
    time.sleep(2)
    os.startfile("os.py")

else:
    user = input("Username [?] ")
    password = input("password [?] ")
    f = open('user.txt', 'w')
    f.write(user)
    f.close()
    f = open('pass.txt', 'w')
    f.write(password)
    f.close()
    print("System rebooting....")
    time.sleep(3)
    os.startfile("os.py")