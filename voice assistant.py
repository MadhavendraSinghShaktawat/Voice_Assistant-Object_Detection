import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import pyautogui
from plyer import notification
from bs4 import BeautifulSoup
import requests
import sys

from playsound import playsound

#  Importing self_made functions
import VolumeHandControl as vhc
# from MY_Functions.FingureCount import FingureCountingProject as fcp



# **********************Global Variables*******************************
Gender = ""
Male = 'Sir'
FeMale = 'maem'

# ---------------------------------------------------------------------



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def input_query():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('recognition is on....')
        recognizer.pause_threshold = 0.7
        voice = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(voice).lower()
            print('this is the query that was made....', query)
            return query
        except Exception as ex:
            print('An exception occurred', ex)
            # print("Didn't recognise")
            # pass

def report_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return current_time


def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()

def make_request(url):
  response = requests.get(url)
  return response.text

def activate_va():
    user_query = input_query()
    print('user query ....', user_query)
    if 'time' in user_query:
        current_time = report_time()
        print(f"the current time is {current_time}")
        speak_va(f"the current time is {current_time}")
    elif 'open website' in user_query:
        speak_va(
            "Please type the name of the website that you want to open (specify the full url) \n")
        website_name = input()
        print(website_name)
        webbrowser.get(
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(website_name)
        speak_va(f"{website_name} opened.")
    elif 'wikipedia' in user_query:
        speak_va("Searching on Wikipedia")
        user_query = user_query.replace('wikipedia', ' ')
        result = wikipedia.summary(user_query, sentences=4)
        print(result)
        speak_va(result)
    elif 'joke' in user_query:
        random_joke = pyjokes.get_joke()
        print(random_joke)
        speak_va(random_joke)
    elif 'screenshot' in user_query:
        image = pyautogui.screenshot()
        image.save('screenshot.png')
        speak_va('Screenshot taken.')
    elif 'search' in user_query:
        speak_va("What do you want me to search for (please type) ? ")
        search_term = input()
        search_url = f"https://www.google.com/search?q={search_term}"
        webbrowser.get(
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(search_url)
        speak_va(f"here are the results for the search term: {search_term}")
    elif 'covid' in user_query:
      html_data = make_request('https://www.worldometers.info/coronavirus/')
      # print(html_data)
      soup = BeautifulSoup(html_data, 'html.parser')
      total_global_row = soup.find_all('tr', {'class': 'total_row'})[-1]
      total_cases = total_global_row.find_all('td')[2].get_text()
      new_cases = total_global_row.find_all('td')[3].get_text()
      total_recovered = total_global_row.find_all('td')[6].get_text()
      print('total cases : ', total_cases)
      print('new cases', new_cases[1:])
      print('total recovered', total_recovered)
      notification_message = f" Total cases : {total_cases}\n New cases : {new_cases[1:]}\n Total Recovered : {total_recovered}\n"
      notification.notify(
        title="COVID-19 Statistics",
        message=notification_message,
        timeout=5
      )
      speak_va("here are the stats for COVID-19")

    elif "roommate name" in user_query:
        speak_va("vivek and josua")

    elif "volume controller" in user_query:
        speak_va(f'Opening Volume controller {Gender}')
        vhc.volumeController()

    # elif "count finger" in user_query:
    #     speak_va("Counting fingres is still developing by Madhavendra Sir, so it will just detect only right arms fingers, now i am Counting fingers sir")
    #     fcp.fCounting()

    else:
        pass



def sexChecker():
    #          Checking Gender
    speak_va("Enter F for Female or M for Male")
    print("Enter F for Female or M for Male")
    SexChecker = str(input())
    if SexChecker.lower() == "m":
        print("Hello Sir how may i help you")
        speak_va("Hello Sir how may i help you")
        Gender = Male

    elif SexChecker.lower() == 'f':
        speak_va('Hello maem nice to meet you')
        print('Hello maam nice to meet you')
        Gender = FeMale

    else:
        speak_va("Are you dumb!!")
        print("Enter Correct word")
        sys.exit()


if __name__ == "__main__":
    sexChecker()
    while True:
        activate_va()