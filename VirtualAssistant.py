import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pyaudio
import random
import time
import webbrowser
import os
from googlesearch import search
import spotipy


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <5:
        speak("Welcome Sumukh, it's bed time don't overload me XD")

    elif hour >= 5 and hour <7:
        speak("Morning Sumukh, What's up I just woke up") 

    elif hour >= 7 and hour <12:
        speak("Morning Sumukh, What's Up")

    elif hour >= 12 and hour <17:
        speak("Good afternoon sumukh")  

    elif hour >= 17 and hour <19:
        speak("Good evening Sumukh")

    elif hour >= 19 and hour <=24:
        speak("Wassup")       

    speak("I'm SMOKE")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold = 0.5
        r.energy_threshold = 500
        r.operation_timeout = 1 
        audio = r.listen(source)


        try:
            print("Tell me..")
            query = r.recognize_google(audio, language='en-in')
            print(f"User: {query.capitalize()} \n")

        except Exception:
            #print(e)
            print("Not Recognized")
            speak("Come again, you piece of shit")
            return "None"
        return query

def respond():
        query = takeCommand().lower()

        if 'wikipedia' in query or 'tell me about' in query or 'who is' in query:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            print(results)
            speak("According to wikipedia.org")
            speak(results)

        elif 'who are you' in query or 'what\'s your name' in query:
            results = ["I am Smoke, Crappy Sumukh's crappy assistant",
                    "I am Smoke, filled with bugs, xD",
                    "Some call me Smoke",
                    "Smoke. Developed by Sumukh",
                    "Smoke, your unreliable assistant",
                    ]
            results = random.choice(results)
            print(results)
            speak(results)

        elif 'who built you' in query:
            results = "Crappy Sumukh"
            print(results.capitalize())
            speak(results)

        elif 'when is your birthday' in query:
            results = "30th August"
            print(results)
            speak(results)

        elif 'are you single' in query:
            results = "Sorry mate"
            print(results)
            speak(results)

        elif 'can you dance' in query:
            results = "can you get laid?\n You peice of shit"
            print(results.capitalize())
            speak(results)

        elif 'are you real' in query:
            results = "Nothing is real in this world"
            print(results.capitalize())
            speak(results)
        
        elif 'open youtube' in query:
            results = "opening Youtube"
            print(results)
            webbrowser.get('windows-default').open('http://www.youtube.com')
            speak(results)
        
        elif 'search youtube for' in query:
            query = query.replace("search youtube for", "")
            results = f"Searching Youtube for{query}"
            print(results)
            webbrowser.get('windows-default').open(f'https://www.youtube.com/results?search_query={query}')
            speak(results)
        
        elif 'search google for' in query:
            query = query.replace("search google for", "")
            results = f"Searching Google for{query}"
            print(results)
            webbrowser.get('windows-default').open(f'https://www.google.com/search?q={query}')
            speak(results)

        elif 'google' in query:
            query = query.replace("google", "")
            results = f"Searching Google for{query}"
            print(results)
            webbrowser.get('windows-default').open(f'https://www.google.com/search?q={query}')
            speak(results)


        elif 'stack overflow' in query:
            webbrowser.get('windows-default').open('http://www.stackoverflow.com')

        #OPENING APPS///////////////////
        elif 'open chrome' in query or 'Google Chrome' in query:
            path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome"
            os.startfile(path)
            results = "Opening Chrome"
            print(results)
            speak(results)
        elif 'open whatsapp' in query:
            path = "C:\\Users\\sumuk\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Chrome Apps\\WhatsChrome" 
            os.startfile(path)
            results = "Opening Whatsapp"
            print(results)
            speak(results)
            
        elif 'open premiere pro' in query:
            path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Premiere Pro 2020"
            os.startfile(path)
            results = "Opening Premiere Pro"
            print(results)
            speak(results)

        elif 'open after effects' in query:
            path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe After Effects 2020"
            os.startfile(path)
            results = "Opening After Effects"
            print(results)
            speak(results)
        elif 'open photoshop' in query:
            path = "C:\\Program Files\Adobe\\Adobe Photoshop CC 2019\\photoshop"
            os.startfile(path)
            results = "Opening Photoshop"
            print(results)
            speak(results)
        elif 'open counter strike' in query or 'cs go' in query:
            path = "C:\\Users\\sumuk\\OneDrive\\Desktop\\Counter-Strike Global Offensive.url"
            os.startfile(path)
            results = "Opening CS GO, have fun"
            print(results)
            speak(results)
        elif 'open discord' in query or 'cs go' in query:
            path = "C:\\Users\\sumuk\\OneDrive\\Desktop\\Discord"
            results = "Opening Discord"
            print(results)
            speak(results)
            os.startfile(path)


        elif 'stop' in query or 'bye' in query:
            results = "K bye"
            print(results)
            print("Exiting...")
            speak(results)
            quit()

        else:
            webbrowser.get('windows-default').open(f'https://www.google.com/search?q={query}')

def Activate():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        r.energy_threshold = 200
        r.operation_timeout = 1 
        audio = r.listen(source)

        try:
            print("Active")
            queryy = r.recognize_google(audio, language='en-in')

        except Exception:
            #print(e)
            return "None"
        return queryy


if __name__ == "__main__":
    wishMe()
    while True:
        queryy = Activate().lower()
        if 'smoke' in queryy:
            speak("Yo")
            respond()