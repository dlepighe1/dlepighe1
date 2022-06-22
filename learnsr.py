"""
Learn Speech Recognition
------------------------
This is a module that translate speech from a source (microphone, or any source that gets voices)
to text. In other words, it's a Speech-to-text module. 
To install it, use the:

# pip install SpeechRecognition
# pip install pyaudio

Classes
* Recognizer class. 
Used for recording sound or audio
Here are some methods:
    recognize_bing()
    recognize_google()
    recognize_google_cloud() // Google cloud packages required
    recognize_houndify()
    recognize_ibm()
    recognize_sphinx() // For offline recognization. PocketSphinx required to use it.
    recognize_wit()
Here are some attributes that goes in the methods,
    - language = 'en-EN' : to define the language to be English (goes with the recognizer_ ...())
    - duration = 2: to set a duration for a certain amount of seconds (goes with the ambient_noise())
    - phrase_time_limit = 5: This is the maximum time the program will wait until stopping the process 
                              of listening. In other words, the program will wait 5 seconds and stop if 
                              nothing was said or recorded from the Microphone. 
    
* Microphone class
Used to record audio using the microphone. PyAudio package is required

Other information:
You can also have these modules:
    # pip install pyttsx3
    # pip install gTTS  
    # pip install playsound
    # pip install random (random2)
    # pip install time
"""

import speech_recognition as sr # sr is just a common abbreviation of speech recognition
import pyttsx3 # We can also use this for text to speech
from gtts import gTTS # Very well known and used because of its connection with Google
from random import *
from playsound import playsound # This is used with gTTS, pyttsx3 doesn't need it. Playsound is to play sounds :)
import time
import os # Just for some special stuff like removing files

###################################################################################
# A more basic way to use Speech Recognition

r = sr.Recognizer() # Initialize the recognizer to get ready to listen

with sr.Microphone() as source:
    # sr.Microphone() considers the microphone of the computer as input (source) by default.
    print("Basic session initialized: Speech Recognition ")
    print("-" * 45)
    print("Silence for noise calibration ...")  
    
    # Since there's no automatic noise cancellation, this method can help. It can be used to 
    # prepare the program to listen and avoid catching background noises for a duration of 
    # 2 seconds). In other words, it's like a filter of ambient noise. The duration is optional
    r.adjust_for_ambient_noise(source, duration= 2) 

    print("Now speak ...")   
    # Let's consider audio as the variable we will store the recording. 
    # While the recognizer r will be listening to the source, which is defined to be 
    # whatever comes from the microphone as on line 40, it will be stored in that variable audio
    audio = r.listen(source) 
    #audio = r.listen(source, phrase_time_limit = 5) # You can use this to limit the waiting time to listen
    
    # This will use Google's module to convert the audio into text
    print("Stop.")
    speech_to_text = r.recognize_google(audio)
    print("Text recorded: ", speech_to_text)
time.sleep(2)
print("Session end!")
print("*" * 45)
time.sleep(3) # Allow 3 seconds to move to the next session

#################################################################################
# Using Speech recognition with Pyttsx3 for text to speech 
 
counter = 0 # The number of times the program will run in a loop 
question = ["Say something", "How are you?", "Hey, what's up?"]
#byes = ["Good bye", "Bye bye", "See you soon!"]

#r1 = sr.Recognizer() # This is optional. We can still use the same recognizer r from the basic section above 

# Using PYTTSX3, let's make a function that will manage the speech
def speak(command): 
    # This function will make the computer speak
    # First, initialize the engine, than say the command
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

intro = "New session initialized: Speech Recognition plus Text-to-Speech using Pyttsx3 module"
print(intro)
print("-" * 84)
speak(intro) # To make the program read or say the intro
print("Initializing listener ...")
time.sleep(3) # Just to allow a small wait before the session starts

while counter < 3: # While it's running
    with sr.Microphone() as source:
        # choice is from random (It's like random.choice() if we imported like: import random (instead of *))
        # This will choose a random response from the list of questions and save it in a variable "tag"
        tag = choice(question) 
        print(">>> Program: ", tag)
        speak(tag) # Say whatever the tag turned out to be

        # Filter the noise, and then give ourselves 5 seconds for the listener to be active. 
        r.adjust_for_ambient_noise(source)
        print("Speak now ...")
        myaudio = r.listen(source, phrase_time_limit= 5) 
        print("Stop.")
    
    # This Try/Except block is used to manage errors in case anything happened
    try:
        # If everything goes well, the program will run this block
        the_speech = r.recognize_google(myaudio)
        print(">>> You: ", the_speech.lower())
        speak("You said, "+ the_speech)      
    except:
        # In case the program didn't understand the speech from myaudio, or didn't recognize it
        speak("Sorry, I didn't get that") # This will be its response. 

    counter = counter + 1 # Increment the counter until reaching 3 and end the session
print("The program ended successfully!\nThe session ended! ")
print("*" *84)
time.sleep(3) # Wait 3 seconds before starting a new session
""""""
#################################################################################################################
# Doing speech recognition plus gTTS for text to speech 
counter = 0
intro = "New session initialized: Speech Recognition plus Text-to-Speech using gTTS module"
print(intro)
print("-" * 84)
speak(intro)
# What we need to do here is being able to capture the sound and save that in a file. 
# Since we want to do with gTTS, we can do this (using our r recognizer)
while counter < 3:
    speech = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Speak now ...")
        ouraudio = r.listen(source, phrase_time_limit= 5)
        print("Stop.")
    
    try:
        speech = r.recognize_google(ouraudio)
        # Here are some gTTS features
        # You get the speech converted into text in line 150 and pass it into gTTS.
        saved_speech = gTTS("You said " + speech, lang = "en") # We might need to specify the language to read with 
        # fr = French, ja = Japanese, en = English, ar = Arabic, es = Spanish
        saved_speech.save("memo.mp3") # Save the whole speech as an audio file. The name doesn't matter.
        print("You said: ", speech)
    except:
        speech = "Sorry, I didn't get that"
        saved_speech = gTTS(speech, lang= 'en')
        saved_speech.save("memo.mp3")
    playsound("memo.mp3") # Play the sound we just saved
    os.remove("memo.mp3") # To remove the file and make a new one afterwards.This will avoid an error to occur
    
    counter += 1 # Increment the count
print("The session ended !")
time.sleep(3)
#####################################################################################################
"""
A bit more about gTTS
---------------------
This module is more of a text to speech thing. There is a small program below that you can use to 
practice with entering data and making the program read the text and return to you as a speech.
"""
intro = "A bit more with gTTS"
print(intro)
print("-" * 20)
speak(intro)
speak("This is just a small program that will ask you to type in a sentence and the language for my sister to read")
time.sleep(2)

# Variables
sentence = input(">> Enter a sentence: ")
while True:
    language = input(">> Enter a language to read with(en, fr, ja, ar, es): ")
    lang_list = ["fr", "en", "ar", "ja", "es", "hi"]
    # Handle wrong entry
    if language not in lang_list: 
        print("Wrong entry! Check the list of chosen languages ...")
        continue
    else: 
        break

message = gTTS(str(sentence), lang = f'{language}')
message.save("test.mp3")

playsound("test.mp3")
###################################################################################

#What we could have done with gTTS:
def gtts_speak(message): 
    print("You : ", message) 
    toSpeak = gTTS(message, lang='en')
    file = "memo.mp3"
    toSpeak.save(file)
    playsound(file)
    os.remove(file)

def get_audio(): 
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source, phrase_time_limit=5)
    print("Stop.")
    try:
        text = r.recognize_google(audio,language='en-US')
        print(text)
        return text
    except:
        gtts_speak("Sorry, I didn't get that, Please try again!")
        return 0 # This would be like nothing was heard from the source

gtts_speak("This is awesome! I don't need to write a long line of code just to speak anymore. The function does the trick")
gtts_speak("Try to say something, I'm listening")
print("Speak now ...")
new_speech = get_audio().lower()
gtts_speak("You said: " + new_speech)