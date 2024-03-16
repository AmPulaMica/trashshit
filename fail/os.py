import time
import os
#...................#
user_name = open('user.txt')
u_n = user_name.read()
user_pass = open('pass.txt')
u_p = user_pass.read()

print("Welcome",u_n)
passw = input("Enter password : ")
if passw == u_p:
    while True:
        print("Welcome",u_n)
        print("""
        [!]About os  
        [.]Terminal
        [^]Text to speech
        [+]Calculator     
        [-_-]Sleep
        [.] Shut down
        [._.] Restart        
        """)
        app = input("[?] ")
        if app == "!":
            time.sleep(1)
            os.startfile("About.py")
        if app == ".":
            time.sleep(1)
            os.startfile("Terminal.py")
        if app == "^":
            time.sleep(1)
            os.startfile("1main - Copy.py")
        if app == "+":
            time.sleep(1)
            os.startfile("Calc.py")  
        if app == "-_-":
            time.sleep(1)
            print("Os: Time?")
            time1 = input("You: ")  
            time.sleep(time1)


else:
    print("Wrong password")