import time
import os
import pyautogui
import psutil
# ---------------------
os.system("cls")
#clearr screen

print("Yoink terminal[v 0.1]")
while True:
   term = input("Terminal: ")
   if term == "install py module":
       ml = input("Name of module [?] ")
       pyautogui.hotkey('win', 'r')
       time.sleep(2)
       pyautogui.typewrite('powershell')
       time.sleep(2)
       pyautogui.press('enter')
       time.sleep(2)
       pyautogui.typewrite('pip install ' +ml)

       pyautogui.press('enter')
       time.sleep(2)
   if term == "open code":
       pyautogui.hotkey('win', 'r')
       time.sleep(2)
       pyautogui.typewrite('powershell')
       time.sleep(2)
       pyautogui.press('enter')
       time.sleep(2)
       pyautogui.typewrite('code .')

       pyautogui.press('enter')
       time.sleep(2)

   if term == "Boost pc":
       pyautogui.hotkey('win' , 'r')
       time.sleep(2)
       pyautogui.typewrite('powershell')
       time.sleep(2)
       pyautogui.press('enter')
       time.sleep(2)
       pyautogui.typewrite('%temp%')

       pyautogui.press('enter')
       time.sleep(2)

   if term == "python":      
      pyautogui.hotkey('win' , 'r')
      time.sleep(2)
      pyautogui.typewrite('cmd')
      time.sleep(2)
      pyautogui.press('enter')
      time.sleep(2)
      pyautogui.typewrite('python')

      pyautogui.press('enter')
      time.sleep(2)