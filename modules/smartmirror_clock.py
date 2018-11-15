from tkinter import *
import threading
import time
import locale
import json
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


class Clock(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.time_data = ''

        utils_json = open('utils/utils.json')
        self.utils = json.load(utils_json)
        self.locale = self.utils['clock']['locale']
        self.time_format = self.utils['clock']['time_format']
        self.date_format = self.utils['clock']['date_format']

        self.clock_frame = Frame(self.master, bg='black')
        self.clock_frame.pack(side=RIGHT, anchor=N)
        self.time_label = Label(self.clock_frame, font=('Helvetica', 94), fg="white", bg="black")
        self.time_label.pack(side=TOP, anchor=N)
        self.day_of_week_data = ''
        self.day_of_week_label = Label(self.clock_frame, text=self.day_of_week_data, font=('Helvetica', 24), fg="white", bg="black")
        self.day_of_week_label.pack(side=TOP, anchor=N)
        self.date_data = ''
        self.date_label = Label(self.clock_frame, text=self.date_data, font=('Helvetica', 24), fg="white", bg="black")
        self.date_label.pack(side=TOP, anchor=N)
        self.tick()

    def tick(self):
        with setlocale(self.locale):
            if self.time_format == 12:
                time_data = time.strftime('%I:%M %p')
            else:
                time_data = time.strftime('%H:%M')

            day_of_week_data = time.strftime('%A')
            date_data = time.strftime(self.date_format)
            if time_data != self.time_data:
                self.time_data = time_data
                self.time_label.config(text=time_data)
            if day_of_week_data != self.day_of_week_data:
                self.day_of_week_data = day_of_week_data
                self.day_of_week_label.config(text=day_of_week_data)
            if date_data != self.date_data:
                self.date_data = date_data
                self.date_label.config(text=date_data)
            self.time_label.after(200, self.tick)

