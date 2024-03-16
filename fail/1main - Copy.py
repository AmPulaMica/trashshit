def speak(str):
    from win32com.client import Dispatch
    speak=Dispatch("SAPI.spVoice")
    speak.Speak(str)

if __name__ == "__main__":
    import requests
    import json

   
    for i in range(0, 4):
        
        get_speech = input("enter text : ")
        speak(get_speech)     
