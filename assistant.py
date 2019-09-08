from gtts import  gTTS
from pygame import mixer
import speech_recognition as sr
import time
import requests
import bs4
import random



#function to let the assistant speak  
def talk(audio):
    print(audio)
    for line in audio.splitlines():
        text_to_speech=gTTS(text=audio,lang='en-uk')
        text_to_speech.save('audio.mp3')
        mixer.init()
        mixer.music.load("audio.mp3")
        mixer.music.play()

# listen to command
def myCommand():
    #initialize the recognizer
    r=sr.Recognizer

    with sr.Microphone() as source:
        print("Kenneth your assistant is ready ")
        r.pause_threshold=1
        #allow the recognizer a second to adjust the energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source,duration=1)

        #now listen for voice input from the user
        audio=r.listen(source)
    try:
        command=r.recognize_google(audio).lower()
        print("You gave command: "+command+"\n")
    #if can't recognize speech keep listening 
    except sr.unknownValueError:
            print("I could hear your last command kenneth")
            command=myCommands()
    
    return command


#helper function to to return phrases
def getPhrases():

    errorPhrases=[]
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    URL="https://englishlive.ef.com/blog/language-lab/say-didnt-understand-someone-english/"
    raw_page_data=requests.get("https://englishlive.ef.com/blog/language-lab/say-didnt-understand-someone-english/",headers=headers)
    raw_page_data.raise_for_status()

    soup = bs4.BeautifulSoup(raw_page_data.text,'html.parser')
    content=soup.article.find_all('li')

    for phrase in content:
        print(phrase.get_text())
        errorPhrases.append(phrase.get_text())
      
    talk("i've found "+ str(len(errorPhrases))+" phrases you can use for error messages")
    time.sleep(5)
    #print(errorPhrases)
    return errorPhrases;


def assistant(command):
    errors=getPhrases()
    if 'Hello' in command:
        talk("Hello Kenneth ,whats up?");
        time.sleep(5)
    else:
        error=random.choice(errors)
        talk(error)
        time.sleep(5)


while True:
    assistant(myCommand())





