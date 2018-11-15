from tkinter import *
import requests
import json
from PIL import Image, ImageTk

#icons: https://openweathermap.org/weather-conditions
icon_lookup = {
    '01d': "assets/Sun.png",
    '01n': "assets/Moon.png",
    '02d': "assets/PartlySunny.png",
    '02n': "assets/PartlyMoon.png",
    '03d': "assets/Cloud.png",
    '03n': "assets/Cloud.png",
    '04d': "assets/Cloud.png",
    '04n': "assets/Cloud.png",
    '09d': "assets/Rain.png",
    '09n': "assets/Rain.png",
    '10d': "assets/Rain.png",
    '10n': "assets/Rain.png",
    '11d': "assets/Storm.png",
    '11n': "assets/Storm.png",
    '13d': "assets/Snow.png",
    '13n': "assets/Snow.png",
    '50d': "assets/Haze.png",
    '50n': "assets/Haze.png",
}


class Weather(Frame):

    def __init__(self, parent,  *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.icon = ''
        self.temperature = ''
        self.humidity = ''
        self.forecast_heading = ''
        self.forecast_description = ''
        self.location = ''

        utils_json = open('utils/utils.json')
        self.utils = json.load(utils_json)
        self.openweathermap_api_key = self.utils['weather']['openweathermap_api_key']
        self.language = self.utils['weather']['language']
        self.units = self.utils['weather']['units']

        translation_json = open('language/%s.json' % (self.utils['language']))
        self.translation = json.load(translation_json)

        self.weather_frame = Frame(self.master, bg='black')
        self.weather_frame.pack(side=LEFT, anchor=N)

        self.degree_frame = Frame(self.weather_frame, bg='black')
        self.degree_frame.pack(side=TOP, anchor=N)
        self.icon_label = Label(self.degree_frame, bg="black")
        self.icon_label.pack(side=LEFT, anchor=N, padx=20)
        self.temperature_label = Label(self.degree_frame, font=('Helvetica', 94), fg="white", bg="black")
        self.temperature_label.pack(side=LEFT, anchor=N)

        self.humidity_frame = Frame(self.weather_frame, bg='black')
        self.humidity_frame.pack(side=TOP, anchor=N)
        self.humidity_label = Label(self.humidity_frame, font=('Helvetica', 18), fg="white", bg="black")
        self.humidity_label.pack(side=LEFT, anchor=W)

        self.forecast_frame = Frame(self.weather_frame, bg='black')
        self.forecast_frame.pack(side=TOP, anchor=W)
        self.forecast_heading_label = Label(self.forecast_frame, font=('Helvetica', 48), fg="white", bg="black")
        self.forecast_heading_label.pack(side=TOP, anchor=N, padx=55)
        self.forecast_description_label = Label(self.forecast_frame, font=('Helvetica', 28), fg="white", bg="black")
        self.forecast_description_label.pack(side=TOP, anchor=N, padx=30)
        self.location_label = Label(self.forecast_frame, font=('Helvetica', 18), fg="white", bg="black")
        self.location_label.pack(side=TOP, anchor=N, padx=55)
        self.get_weather()

    def get_weather(self):
        try:
            location_req_url = "http://ip-api.com/json"
            req = requests.get(location_req_url)
            location_obj = json.loads(req.text)
            lat = location_obj['lat']
            lon = location_obj['lon']
            location_data = "%s, %s" % (location_obj['city'], location_obj['countryCode'])
            weather_request_url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&lang=%s&units=%s&APPID=%s" % (lat, lon, self.language, self.units, self.openweathermap_api_key)
            r = requests.get(weather_request_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature_data = "%s%s" % (str(int(weather_obj['main']['temp'])), degree_sign)
            humidity_data = "%s%s" % (weather_obj['main']['humidity'], "%")
            icon_id = weather_obj['weather'][0]['icon']
            forecast_title = weather_obj['weather'][0]['main']
            forecast_description = weather_obj['weather'][0]['description']
            station_name = weather_obj['name']
            location_data += " (%s)" % (station_name)
            icon_data = None

            if icon_id in icon_lookup:
                icon_data = icon_lookup[icon_id]

            if icon_data is not None:
                if self.icon != icon_data:
                    self.icon = icon_data
                    image = Image.open(icon_data)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.icon_label.config(image=photo)
                    self.icon_label.image = photo
            else:
                self.icon_label.config(image='')

            if self.temperature != temperature_data:
                self.temperature = temperature_data
                self.temperature_label.config(text=temperature_data)

            if self.humidity != humidity_data:
                humidity_translation = self.translation['humidity']
                self.humidity = "%s: %s" % (humidity_translation.capitalize(), humidity_data)
                self.humidity_label.config(text=self.humidity)

            if self.forecast_heading != forecast_title.capitalize():
                self.forecast_heading = forecast_title.capitalize()
                self.forecast_heading_label.config(text=forecast_title.capitalize())

            if self.forecast_description != forecast_description.capitalize():
                self.forecast_description = forecast_description.capitalize()
                self.forecast_description_label.config(text=forecast_description.capitalize())

            if self.location != location_data:
                if location_data == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.location_label.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location_data
                    self.location_label.config(text=location_data)
        except Exception as e:
            print("Error: %s. Cannot get weather." % e)

        self.after(600000, self.get_weather)
