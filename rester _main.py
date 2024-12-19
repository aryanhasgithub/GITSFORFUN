import requests
import pyttsx3
import speech_recognition as sr
from homeassistant_api import Client
from datetime import datetime
from threading import Timer
import os
from groq import Groq

client= Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class Assistant:
    def __init__(self, home_assistant_url, access_token, groqcloud_key, weather_api_key):
        self.client = Client(home_assistant_url, access_token)
        
        self.groqcloud_key = groqcloud_key
        self.weather_api_key = weather_api_key
        self.tts_engine = pyttsx3.init()

    def speak(self, message):
        self.tts_engine.say(message)
        self.tts_engine.runAndWait()
    def process_command(self, command):
        print(f"Processing command: {command}")
        if "set alarm at" in command:
            time = self.extract_alarm_time(command)
            self.set_alarm(time)
        elif "set timer for" in command:
            duration = self.extract_duration(command)
            self.set_timer(duration)
        elif "turn on" in command or "turn off" in command:
            entity_id = self.extract_entity(command)
            if "turn on" in command:
                self.turn_on_device(entity_id)
            else:
                self.turn_off_device(entity_id)
        elif "weather" in command:
            self.get_weather("Ghaziabad")
            
        elif "time" in command:
            self.speak(datetime.now())
            return datetime.now()
        else:
            self.send_to_groqcloud(command)

    def get_weather(self, city_name="Ghaziabad"):
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Ghaziabad&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] == 200:
            main_weather = weather_data["main"]
            weather_desc = weather_data["weather"][0]["description"]
            temperature = main_weather["temp"]
            humidity = main_weather["humidity"]
            
            weather_report = f"The current temperature in {city_name} is {temperature}°C with {weather_desc}. Humidity is {humidity}%."
            self.speak(weather_report)
            print(weather_report)
        else:
            self.speak("Sorry, I couldn't fetch the weather data.")
            print("Error fetching weather data.")

    def send_to_groqcloud(self, command):
        chat_completion = client.chat.completions.create(
            messages=[
           {
            "role": "user",
            "content":command,
           }
         ],
         model="llama3-8b-8192",
         )   
    
        self.speak(chat_completion.choices[0].message.content)
        print(chat_completion.choices[0].message.content)
        

    def extract_entity(self, command):
        if "light" in command:
            return "light"
        elif "fan" in command:
            return "fan"
        else:
            return None

    def turn_on_device(self, entity_id):
        if entity_id:
            print(f"Turning on {entity_id}")
            self.client.call_service("light.turn_on", entity_id=entity_id)
            self.speak(f"{entity_id} turned on.")
        else:
            self.speak("Device not recognized.")

    def turn_off_device(self, entity_id):
        if entity_id:
            print(f"Turning off {entity_id}")
            self.client.call_service("light.turn_off", entity_id=entity_id)
            self.speak(f"{entity_id} turned off.")
        else:
            self.speak("Device not recognized.")

    def extract_duration(self, command):
        if "minute" in command:
            return 60
        elif "hour" in command:
            return 3600
        return 0

    def set_timer(self, duration):
        if duration:
            self.speak(f"Timer set for {duration / 60} minutes.")
            Timer(duration, self.timer_finished).start()
        else:
            self.speak("Invalid duration for timer.")

    def timer_finished(self):
        self.speak("Your timer has finished!")

    def extract_alarm_time(self, command):
        if "time" in command:
            return datetime.now()

    def set_alarm(self, alarm_time):
        self.speak(f"Alarm set for {alarm_time}.")
        # Add actual alarm setting logic here, e.g., integration with a real alarm system.
    

    def listen_to_voice(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        print("Listening for commands... Say 'Assistant' to activate.")

        while True:
          try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio).lower()
            print(f"Detected: {command}")
            if "assistant" in command:
              print(self.process_command(command))
            else:
                print("speak")

          except sr.UnknownValueError:
            print("Could not understand the audio, please try again.")
          except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
          finally:
            print("done")
            

    
if __name__ == "__main__":
    home_assistant_url = "http://homeassistant.local:8123"
    access_token = "YOUR_HOME_ASSISTANT_ACCESS_TOKEN"
    
    groqcloud_key = "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"
    weather_api_key = "47f17fcedd2cfb3849a3ec381dc5804e"  # Add your weather API key here

    assistant = Assistant(home_assistant_url, access_token,  groqcloud_key, weather_api_key)
    assistant.listen_to_voice()
