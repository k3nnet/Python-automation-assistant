from gtts import  gTTS
from pygame import mixer
import speech_recognition as sr
import time
import requests
import bs4
import random
import urllib
from selenium import webdriver
import speech_recognition as sr
from selenium.webdriver.common.keys import Keys
import re
import webbrowser



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
    r=sr.Recognizer()

    with sr.Microphone() as source:
        print("ready")
        r.pause_threshold=1
        #allow the recognizer a second to adjust the energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source,duration=1)

        #now listen for voice input from the user
        audio=r.listen(source)
       
      
       
    try:
        print("You gave command: \n")
        command=r.recognize_google(audio).lower()
        print("You gave command: "+command+"\n")
        return command
    #if can't recognize speech keep listening 
    except  sr.UnknownValueError:
        print("I could not hear your last command kenneth")
        command=myCommand()
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        command =myCommand()
        

    
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
    
        errorPhrases.append(phrase.get_text().split("-")[0])
      

    #print(errorPhrases)
    return errorPhrases;


def assistant(command):
    errors=getPhrases()
    print("here "+command)
    if 'hello' in command:
        talk("Hello Kenneth ,whats up?");
       
 
    elif 'open google and search' in command:
        reg_ex=re.search('open google and search (.*)',command)
        search_for=command.split("search",1)[1]
        url='https://www.google.com/'
        if reg_ex:
            subgoogle=reg_ex.group(1)
            url=url +'r/' +subgoogle
        talk('Okay!')

        driver=webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        driver.get('https://www.google.com')
        search=driver.find_element_by_name('q')
        search.send_keys(str(search_for))
        search.send_keys(Keys.RETURN)
    elif 'open google' in command:
        #matching command to check it is availabble
        reg_ex=re.search('open google (.*)',command)
        url='https://www.google.com'
        if reg_ex:
            subgoogle=reg_ex.group(1)
            url=url+'r/'+subgoogle
        webbrowser.open(url)
        print('done!')
    elif 'youtube' in command:
        talk('okay!');
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split("youtube",1)[1] 
            query_string = urllib.parse.urlencode({"search_query" : domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string) 
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) # finds all links in search result
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            pass
    
    
    else:
        error=random.choice(errors)
        talk(error.split("-")[0])
    


while True:
    time.sleep(5)
    command=myCommand()
    assistant(command)





