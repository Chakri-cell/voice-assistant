import pyttsx3 # type: ignore
import datetime
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests # type: ignore
import json
import time
import random
import os
class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.email_client = smtplib.SMTP('smtp.gmail.com', 587)
        self.email_client.starttls()
        self.email_client.login('your_email@gmail.com', 'your_password')
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    def get_voice_input(self):
        print("Listening...")
        try:
            text = input("You: ")
            return text
        except:
            print("Sorry, I didn't understand that.")
            return None
    def respond(self, text):
        if "hello" in text.lower():
            self.speak("Hello How can I assist you today?")
        elif "time" in text.lower():
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}.")
        elif "date" in text.lower():
            current_date = datetime.date.today().strftime("%B %d, %Y")
            self.speak(f"Today's date is {current_date}.")
        elif "search" in text.lower():
            query = text.split("search")[1].strip()
            self.speak(f"Searching the web for: {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "email" in text.lower():
            self.send_email()
        elif "reminder" in text.lower():
            self.set_reminder()
        elif "weather" in text.lower():
            self.get_weather()
        elif "smart home" in text.lower():
            self.control_smart_home()
        elif "general knowledge" in text.lower():
            self.answer_general_knowledge()
        else:
            self.speak("I'm sorry, I didn't understand that command.")
    def send_email(self):
        subject = "Test Email"
        body = "This is a test email."
        msg = MIMEMultipart()
        msg['From'] = 'your_email@gmail.com'
        msg['To'] = 'recipient_email@example.com'
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        self.email_client.sendmail('your_email@gmail.com', 'recipient_email@example.com', text)
        self.speak("Email sent successfully.")
    def set_reminder(self):
        reminder_text = "Reminder: This is a test reminder."
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        self.speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}.")
        time.sleep(5)
        self.speak(reminder_text)
    def get_weather(self):
        api_key = "YOUR_API_KEY_HERE"
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": "London",
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        weather_data = json.loads(response.text)
        self.speak(f"The current weather in London is {weather_data['weather'][0]['description']} with a temperature of {weather_data['main']['temp']}°C.")
    def control_smart_home(self):
        api_key = "YOUR_API_KEY_HERE"
        base_url = "http://api.smart-home.com/devices"
        params = {
            "api_key": api_key
        }
        response = requests.get(base_url, params=params)
        devices = json.loads(response.text)
        self.speak(f"Available devices: {', '.join([device['name'] for device in devices])}.")
        device_name = input("Enter the name of the device you want to control: ")
        for device in devices:
            if device['name'] == device_name:
                self.speak(f"Controlling {device_name}.")
                # Control the device using the API
                break
        else:
            self.speak(f"Device not found.")
    def answer_general_knowledge(self):
        api_key = "YOUR_API_KEY_HERE"
        base_url = "http://api.general-knowledge.com/questions"
        params = {
            "api_key": api_key
        }
        response = requests.get(base_url, params=params)
        questions = json.loads(response.text)
        self.speak(f"Here are the questions: {', '.join([question['text'] for question in questions])}.")
        question_text = input("Enter the text of the question you want to answer: ")
        for question in questions:
            if question['text'] == question_text:
                self.speak(f"The answer is {question['answer']}.")
                break
        else:
            self.speak(f"Question not found.")
    def main(self):
        print("Welcome to the Voice Assistant!")
        print("Say 'hello', 'time', 'date', 'search [query]', 'email', 'reminder', 'weather', 'smart home', or 'general knowledge' to get started.")
        while True:
            text = self.get_voice_input()
            if text:
                self.respond(text)
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.main()