import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from functions.os_ops import close_notepad, paths, open_camera, open_cmd, open_notepad, open_calculator, play_music
from random import choice
from utils import opening_text
from decouple import config
import pyttsx3
from datetime import datetime
import speech_recognition as sr
import os
import random
import sys
import pyjokes


# Using the config method from decouple, we are getting the value of USER and BOT from the environment variables
USERNAME = config('USER')
BOTNAME = config('BOT')

# Create a speech engine first.
# I've initialized an engine using pyttsx3 module.
engine = pyttsx3.init('sapi5')    # sapi5 is a Microsoft Speech API that helps us use the voices

# Set voice
voices = engine.getProperty('voices')  # The pyttsx3 module supports three voices first is male and the second(& 3rd) is female which is provided by “sapi5” for windows.
engine.setProperty('voice', voices[1].id)  

engine.setProperty('rate', 180)     # Set rate. Integer speech rate in words per minute. The base value is 200
engine.setProperty('volume', 1.0)   # Set volume. Floating point volume in the range of 0.0 to 1.0 inclusive

# Note: If you get an error related to PyAudio, download PyAudio wheel and install it.

# Text to speach conversion
# The speak function will be responsible for speaking whatever text is passed to it.
def speak(text):
    engine.say(text)   # the engine speaks whatever text is passed to it using the say() method
    engine.runAndWait()   # It processes the voice commands. Blocks while processing all the currently queued commands
    
def greet_User():
    '''Greets the user according to the time'''
    hour = datetime.now().hour   # It tells the current time (only hour)

    if hour>=6 and hour<12:
        speak(f"Good morning {USERNAME}")
    elif hour>=12 and hour<16:
        speak(f"Good afternoon {USERNAME}")
    elif hour>=16 and hour<19:
        speak(f"Good evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you!")
    

'''We use this function to take the commands from the user and recognize the command using the speech_recognition module.'''
def take_user_input():
    # Takes user input, recognizes it using speech recognition module and converts it into text
    
    r = sr.Recognizer()    # The Recognizer class within the speech_recognition module helps us recognize the audio.

    # So, With microphone as source, we try to listen to the audio using listen() method in the recognizer class.
    with sr.Microphone() as source:    # The same module has microphone class gives us access to the microphone of the device. 
        print("Listening...")
        r.pause_threshold = 1.2  # It means it will not complain even if we pause for 1.2 seconds during we speak.
        r.energy_threshold = 3000   # Minimum audio energy to consider for recording.
        audio = r.listen(source) 

    try:
        print("Recognizing...")
        # The recognize_google() method performs speech recognition on the audio passed to it, using the Google Speech Recognition API.
        query = r.recognize_google(audio, language = 'en-in')   # Using recognize_google() method, we try to recognize the audio
        print(f"User said: {query}\n")  # It prints the transcript of the audio which is nothing but a string we have stored in a variable called query.

        if not 'exit' and not 'stop' and not 'bye' in query:
            speak(choice(opening_text))
        elif 'exit' in query or 'stop' in query or 'bye' in query:
            hour = datetime.now().hour
            speak('Thanks for using me sir!')
            if hour>=21 or hour<5:
                speak("Good night, take care!")
            else:
                speak("Have a good day!")
            sys.exit()

    except Exception:
        speak("Sorry, I couldn't understand. Could you please say that again?")
        query = 'None'
    return query


if __name__ == '__main__':
    greet_User()
    while True:
        query = take_user_input().lower()

        if 'notepad' in query:
            if 'open notepad' in query:
                speak("Opening notepad, sir")
                open_notepad()
            elif 'close notepad' in query:
                speak("Closing notepad.")
                close_notepad()

        elif 'open calculator' in query:
            speak("Opening calculator, sir")
            open_calculator()

        elif 'open cmd' in query or 'open command prompt' in query:
            speak("Opening command prompt, sir")
            open_cmd()

        elif 'open camera' in query:
            speak("Opening Camera, sir")
            open_camera()

        elif 'play music' in query:
            speak('Here you go with the music.')
            songs = play_music()
            rd = random.choice(songs)
            os.startfile(os.path.join(paths['music_dir'], rd))
            
        elif 'ip' in query:
            ip_address = find_my_ip()
            speak(f"Your ip address is {ip_address}.\n For your convenience, I am printing it on the screen sir.")
            print(f"Your ip address is {ip_address}")
            
        elif 'wikipedia' in query:
            speak('What do you want to search on wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to wikipedia {results}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on youtube, sir?')
            video = take_user_input().lower()
            print("Playing...\n")
            play_on_youtube(video)

        elif 'google' in query:
            speak('What do you want to search on google, sir?')
            search_query = take_user_input().lower()
            print("Searching...\n")
            search_on_google(search_query)
        
        elif "send whatsapp message" in query:
            speak("On what number should i send the message sir? Please enter in console")
            number = int(input("Enter the number: "))
            speak("What is the message sir?")
            message = take_user_input().lower()
            if send_whatsapp_message(number, message):
                print("Sending...\n")
                speak("I have sent the message sir!")
            else:
                speak("Something went wrong while sending the whatsapp message.")

        elif "send email" in query:
            speak("On what email address do I send sir? Please enter in console")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I have sent the mail, sir.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'news' in query:
            speak('I am reading out the latest news headlines, sir!')
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen")
            print(*get_latest_news(), sep = '\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city, {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature} but, it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

        elif 'trending movies' in query:
            speak(f"Some of the trending movies are {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen")
            print(f"{get_trending_movies()} \n")

        elif 'joke' in query:
            speak('Hope you like this one sir!')
            joke = pyjokes.get_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen.")
            print(joke)

        elif 'advice' in query:
            speak("Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen.")
            print(advice)

        elif 'time' in query:
            time = datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {time}")
            speak("For your convenience, I am printing it on the screen.")
            print(time) 

        elif 'meaning' in query:
            speak("EDITH means Even Dead I Am The Hero.")

        # Most asked questions from any assistant
        elif 'how are you' in query:
            speak('I am fine, Thank you')
            speak('How are you, sir?')

        elif 'fine' in query:
            speak("It's good to know that you are fine.")

        elif 'who are you' in query:
            speak('I am EDITH, a virtual assistant created by Rohit')

        elif 'will you be my girlfriend' in query or 'will you be my boyfriend' in query:
            speak('I am not sure as of now. But would love to, someday!')