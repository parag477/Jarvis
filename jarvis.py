# ---------IMPORTS---------
import os
import time
import ssl
import pyttsx3
import PyPDF2
import operator
import winsound
import speedtest
import wikipedia
import webbrowser
import smtplib
from random import choice
from sys import argv, exit
from datetime import datetime
from pyjokes import get_joke
from psutil import sensors_battery
from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows
from pyautogui import keyUp, keyDown, press, screenshot
from pywhatkit import search, sendwhatmsg
from speech_recognition import Microphone, Recognizer
from requests import get
from jarvisui import Ui_JarvisUI
from PyDictionary import PyDictionary
from geopy.geocoders import Nominatim
from pywikihow import search_wikihow
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime, QDate, Qt


# ---------CONSTANTS---------
TWILIO_ACCOUNT_SID = "ACc269e4fe004416f202126a98f0232787"
TWILIO_AUTH_TOKEN = "6b25c5f636caaf444856f6108feb3034"
NEWS_URL = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=207b8ddeb9b947249bad4f180d7fea7a"


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
# engine.setProperty('rate', 200)


# ---------FUNCTIONS---------
# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Wish function
def wish():
    """Jarvis will wish at the start"""
    now = datetime.now()
    hour = int(now.hour)
    # current_time = now.strftime("%H:%M %p")
    current_time = now.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"Good Morning, it's {current_time}")
    elif hour > 12 and hour < 18:
        speak(f"Good Afternoon, it's {current_time}")
    else:
        speak(f"Good Evening, it's {current_time}")
    speak("I am Jarvis sir. Please tell me how may I help you.")

def sendEmail(to, content):
    """Function to send email"""
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("shobhitnibariya62@gmail.com", "6264293151")
        server.sendmail("shobhitnibariya62@gmail.com", to, content)

def news():
    """Function to fetch five top headlines"""
    main_page = get(NEWS_URL).json()
    article = main_page["articles"]
    head = []
    # day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    day = ["first", "second", "third", "fourth", "fifth"]
    for ar in article:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")

def pdf_reader():
    """Function to read PDF files"""
    book = open('Black Hat Go.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this book are {pages}")
    speak("Sir please enter the page number from where I have to read")
    pg = int(input("Please enter the page number:"))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)

def alarm(timing):
    altime = str(datetime.now().strptime(timing, "%I:%M%p"))

    altime = altime[11:-3]

    Horeal = altime[:2]
    Horeal = int(Horeal)
    Mireal = altime[3:5]
    Mireal = int(Mireal)
    print(f"Done, alarm is set for {timing}")

    while True:
        if Horeal == datetime.now().hour:
            if Mireal == datetime.now().minute:
                print("Alarm is running")
                winsound.PlaySound('abc', winsound.SND_LOOP)

            elif Mireal < datetime.now().minute:
                break


# ---------MAIN PROGRAM STARTS FROM HERE---------
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()
        speak("Please say wakeup to continue")
        while True:
            self.query = self.take_command_2()
            if "wakeup" in self.query or "wake up" in self.query:
                self.TaskExecution()
            elif "exit" in self.query:
                speak("Thanks for using me sir! Have a nice day...")
                exit()

    # Convert voice into text
    def take_command(self):
        """This function takes voice input from user and converts it into text format"""
        r = Recognizer()
        with Microphone() as source:
            print('listening...')
            r.pause_threshold = 1
            audio = r.listen(source, timeout=4, phrase_time_limit=7)

        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")
        except Exception as e:
            speak("Say that again please...")
            return "none"
        query = query.lower()
        return query

    def take_command_2(self):
        """This function is for when jarvis is on sleep. It doesn't say speak again"""
        r = Recognizer()
        with Microphone() as source:
            print('listening...')
            r.pause_threshold = 1
            audio = r.listen(source, timeout=4, phrase_time_limit=7)

        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")
        except Exception as e:
            return "none"
        query = query.lower()
        return query

    def whatsapp(self):
        """This function sends messages on whatsapp to given specific persons"""
        speak("To whom should I send the message?")
        name = self.take_command()

        if "john" in name:
            speak("What would the message look like?")
            msg = self.take_command()
            speak("When should I send this message?")
            speak("Time in hour")
            hour = int(self.take_command())
            speak("Time in minutes")
            min = int(self.take_command())
            speak("Sending message!!!")
            sendwhatmsg("+917470728915", msg, hour, min, 20)
            # speak("Message sent!!!")
        elif "geetesh" in name:
            speak("What would the message look like?")
            msg = self.take_command()
            speak("When should I send this message?")
            speak("Time in hour")
            hour = int(self.take_command())
            speak("Time in minutes")
            min = int(self.take_command())
            speak("Sending message!!!")
            sendwhatmsg("+917470728915", msg, hour, min, 20)
        elif "parag" in name:
            speak("What would the message look like?")
            msg = self.take_command()
            speak("When should I send this message?")
            speak("Time in hour")
            hour = int(self.take_command())
            speak("Time in minutes")
            minute = int(self.take_command())
            speak("Sending message!!!")
            sendwhatmsg("+917489918182", msg, hour, minute, 20)

        else:
            speak("Sorry Sir, I am not able to send message.")
            # speak("Sorry Sir, I am not able to send message.")
            pass
            # self.whatsapp()

    def Dict(self):
        """This function gives meaning of words that are in dictionary"""
        speak("Activated Dictionary!")
        speak("What is your problem")
        self.probl = self.take_command()

        if "meaning" in self.probl:
            self.probl = self.probl.replace("what is the", "")
            self.probl = self.probl.replace("jarvis", "")
            self.probl = self.probl.replace("meaning of ", "")
            print(self.probl)
            self.result = PyDictionary.meaning(self.probl)
            speak(f"The Meaning of {self.probl} is {self.result}")

        elif "synonym" in self.probl:
            self.probl = self.probl.replace("what is the", "")
            self.probl = self.probl.replace("jarvis", "")
            self.probl = self.probl.replace("synonym of ", "")
            print(self.probl)
            self.result = PyDictionary.meaning(self.probl)
            speak(f"The Synonym of {self.probl} is {self.result}")

        elif "antonym" in self.probl:
            self.probl = self.probl.replace("what is the", "")
            self.probl = self.probl.replace("jarvis", "")
            self.probl = self.probl.replace("antonym of ", "")
            print(self.probl)
            self.result = PyDictionary.meaning(self.probl)
            speak(f"The Antonym of {self.probl} is {self.result}")
        else:
            speak("Sorry Sir I didn't get what you said")

        speak("Exited dictionary")

    def TaskExecution(self):
        # take_command()
        wish()
        while True:
            self.query = self.take_command()

            if "open notepad" in self.query:
                speak("Opening Notepad!")
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif "time" in self.query:
                now = datetime.now()
                hour = int(now.hour)
                current_time = now.strftime("%I:%M %p")

            elif "how are you" in self.query:
                speak("I am fine sir what about you!!")

            elif "open command prompt" in self.query or "open cmd" in self.query:
                speak("Opening Command Prompt")
                os.system('start cmd')

            elif "open camera" in self.query:
                speak("Opening Camera!")
                cap = VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    imshow('webcam', img)
                    k = waitKey(50)
                    if k==27:
                        break
                cap.release()
                destroyAllWindows()

            elif "play music" in self.query:
                try:
                    speak("Playing music!")
                    music_dir = "C:\\Users\\parag\\PycharmProjects\\Jarvis\\jarvisui"
                    songs = os.listdir(music_dir)
                    # r_songs = random.choice(songs)
                    for song in songs:
                        if song.endswith('.mp3'):
                            os.startfile(os.path.join(music_dir, song))
                except Exception as e:
                    speak("Some error occured! Unable to play music...")
                    pass

            elif "ip address" in self.query:
                ip = get("https://api.ipify.org").text
                speak(f"Your ip address is {ip}")

            elif "how are you" in self.query:
                how_reply = ["i am fine sir, what about you", "I am fine", "I'am good", "All right"]
                a = choice(how_reply)
                speak(a)

            elif "hello" in self.query or "hi" in self.query:
                hello_reply = ["hello sir", "hi"]
                hel = choice(hello_reply)
                speak(hel)

            elif "good morning" in self.query:
                m_reply = ["morning", "morning sir", "good morning sir"]
                m = choice(m_reply)
                speak(m)

            elif "wikipedia" in self.query:
                try:
                    speak("Searching Wikipedia...")
                    self.query = self.query.replace("wikipedia", "")
                    self.query = self.query.replace("search", "")
                    self.query = self.query.replace("on", "")
                    results = wikipedia.summary(self.query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception as e:
                    speak("Sir please speak correctly!")
                    pass

            elif "open youtube" in self.query:
                speak("Opening YouTube!!")
                webbrowser.open("www.youtube.com")

            elif "open instagram" in self.query:
                speak("Opening Instagram!!")
                webbrowser.open("www.instagram.com")

            elif "open facebook" in self.query:
                speak("Opening FaceBook!!")
                webbrowser.open("www.facebook.com")

            elif "open google" in self.query or "google search" in self.query:
                speak("This is what I found on google..")
                self.query = self.query.replace("jarvis", "")
                self.query = self.query.replace("open google", "")
                self.query = self.query.replace("google search", "")
                search(self.query)

            elif "send whatsapp message" in self.query or "send a whatsapp message" in self.query:
                try:
                    self.whatsapp()
                except Exception as e:
                    speak("Unable to send message!")
                    pass
                    # speak("Sorry Sir, I am not able to send message.")

            elif "search on youtube" in self.query or "youtube search" in self.query:
                speak("Sir that is what I found on youtube...")
                self.query = self.query.replace("jarvis", "")
                self.query = self.query.replace("search", "")
                self.query = self.query.replace("on youtube", "")
                self.query = self.query.replace("youtube search", "")
                web = 'https://www.youtube.com/results?search_query=' + self.query
                webbrowser.open(web)

            elif "email" in self.query:
                try:
                    speak("What should i say?")
                    content = self.take_command()
                    to = "paragagrawal577@gmail.com"
                    speak("Sir please wait for a while!!")
                    sendEmail(to, content)
                    speak("Email has been sent to parag")

                except Exception as e:
                    print("Sorry Sir! I am not able to send this mail")
                    pass

            elif "close notepad" in self.query:
                speak("Closing notepad!")
                os.system("taskkill /f /im notepad.exe")

            elif "tell me joke" in self.query:
                joke = get_joke()
                speak(joke)

            elif "shut down the system" in self.query:
                speak("Shutting down the system...")
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:
                speak("Restarting...")
                os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:
                speak("The system is going to sleep....")
                os.system("rundll32.exe powrprof.dll.SetSuspentState 0,1,0")

            elif "how much power left" in self.query or "battery" in self.query:
                battery = sensors_battery()
                percentage = battery.percent
                speak(f"Sir our system have {percentage} percent battery left")
                if percentage >= 75:
                    speak("Sir we have enough power to keep working")
                elif percentage >=40 and percentage <= 75:
                    speak("Sir I think we should connect the charger.")
                elif percentage >= 15 and percentage <= 40:
                    speak("Sir we don't have enough power to keep working")
                elif percentage <=15:
                    speak("Sir our battery is going to die in a few minutes. Please connect the charger.")
                else:
                    speak("Charging...")

            elif "switch the window" in self.query:
                keyDown('alt')
                press('tab')
                time.sleep(1)
                keyUp('alt')

            elif "tell me news" in self.query or "headline" in self.query:
                speak("Please wait sir, fetching the latest headlines")
                news()

            elif "where am i" in self.query or "what is my location" in self.query or "where are we" in self.query:
                # ------------------------------
                speak("Wait sir, let me check!!!")
                try:
                    ipad = get("https://api.ipify.org").text
                    geolocator = Nominatim(user_agent="geoapiExercises")
                    # print(ipad)
                    url = "https://get.geojs.io/v1/ip/geo/"+ipad+".json"
                    geo_requests = get(url)
                    geo_data = geo_requests.json()
                    # Latitude = "22.654822"
                    # Longitude = "75.825967"
                    # print(geo_data)
                    # city = geo_data['city']
                    # state = geo_data["state"]
                    # country = geo_data["country"]
                    latitude = geo_data["latitude"]
                    longitude = geo_data["longitude"]
                    location = geolocator.reverse(latitude + "," + longitude)
                    # location = geolocator.reverse(Latitude + "," + Longitude)
                    # speak(f"Sir i am not sure, but I think we are in {city},{state}")
                    speak(f"Sir i am not sure, but I think we are in {location}")
                except Exception as e:
                    speak("Sorry sir, due to network issues I am not able to find where we are.")
                    pass

            elif "take screenshot" in self.query:
                speak("Sir what would be the name of the screenshot file?")
                name = self.take_command()
                speak("Okay sir, taking screenshot")
                time.sleep(3)
                img = screenshot()
                img.save(f"{name}.png")
                speak("Screenshot taken!!!")

            elif "dictionary" in self.query:
                self.Dict()

            elif "read pdf" in self.query:
                pdf_reader()

            elif "do some calculations" in self.query:
                r = Recognizer()
                with Microphone() as source:
                    speak("Say what you want to calculate, example 5 plus 10")
                    print("listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)
                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'x': operator.mul,
                        'divided' : operator.__truediv__,
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)
                speak("Your result is")
                speak(eval_binary_expr(*(my_string.split())))

            elif "temperature" in self.query:
                try:
                    api_key = "5f9334ac2ceb5c65b2908ca92057c987"
                    base_url = "http://api.openweathermap.org/data/2.5/weather?"
                    self.query = self.query.replace("jarvis", "")
                    self.query = self.query.replace("what", "")
                    self.query = self.query.replace("is", "")
                    self.query = self.query.replace("the", "")
                    self.query = self.query.replace("current", "")
                    self.query = self.query.replace("temperature", "")
                    self.query = self.query.replace("in ", "")
                    self.query = self.query.replace(" ", "")
                    city_name = self.query.lower()
                    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                    response = get(complete_url)
                    x = response.json()
                    if x["cod"] != "404":
                        y = x["main"]
                        cur_temp = y["temp"]
                        z = x["weather"]
                        weather_desc = z[0]["description"]
                        speak(f"Current temperature in {city_name} is " + str(
                            round(cur_temp - 273)) + " degree Celcius. It looks like " + str(weather_desc) + ".")
                    else:
                        speak("Sorry Sir, City Not Found!")
                except Exception as e:
                    speak("Sir please specify the city name also")
                    pass

            elif "how to" in self.query:
                self.query = self.query.replace("jarvis", "")
                self.query = self.query.replace("how to", "")
                # speak("Please tell me what you want to know")
                # how = self.take_command()
                max_results = 1
                how_to = search_wikihow(self.query, max_results)
                assert len(how_to) == 1
                how_to[0].print()
                speak(how_to[0].summary)

            elif "internet speed" in self.query:
                try:
                    speak("Sir please wait for a while, fetching internet speed...")
                    st = speedtest.Speedtest()
                    dl = st.download()
                    up = st.upload()
                    speak(f"Sir we have {dl} bit per second downloading speed and {up} bit per second uploading speed")
                except Exception as e:
                    speak("Sorry Sir unable to fetch internet speed!!!")

            elif "send message" in self.query or "send a message" in self.query:
                speak("Sir what should I say")
                msg = self.take_command()
                from twilio.rest import Client

                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                message = client.messages.create(body=msg, from_='+13092205327', to='+917489918182')
                print(message.sid)
                speak("Message sent!")

            elif "volume up" in self.query:
                press("volumeup")

            elif "volume down" in self.query:
                press("volumedown")

            elif "volume mute" in self.query or "mute" in self.query:
                press("volumemute")

            elif "set alarm" in self.query:
                try:
                    speak("Sir please tell me the time to set the alarm, for example, set alarm for 5:30 am")
                    self.inp = self.take_command()
                    self.inp = self.inp.replace("set", "")
                    self.inp = self.inp.replace("alarm", "")
                    self.inp = self.inp.replace("to", "")
                    self.inp = self.inp.replace("for", "")
                    self.inp = self.inp.replace(".", "")
                    self.inp = self.inp.replace(" ", "")
                    print(self.inp)
                    # inp = inp.upper()
                    # import MyAlarm
                    # MyAlarm.alarm(self.inp)
                    alarm(self.inp)
                except Exception as e:
                    speak("Sir unable to set the alarm!")

            elif "you can sleep" in self.query:
                speak("Ok sir, I am going to sleep, you can call me anytime sir.")
                break

            elif "exit" in self.query:
                speak("Thanks for using me sir! Have a nice day...")
                exit()


            # speak("Sir, do you have any other work")


startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarvisUI()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../photos/loading.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../photos/pro.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../photos/model.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../photos/pro3.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss ap')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)



app = QApplication(argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())


# if __name__ == '__main__':
#     # TaskExecution()
#     while True:
#         permission = take_command()
#         if "wake up" in permission:
#             TaskExecution()
#         elif "goodbye" in permission:
#             speak("Thanks for using me sir, Have a good day.")
#             sys.exit()
