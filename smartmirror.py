from tkinter import *

from modules.smartmirror_clock import Clock
from modules.smartmirror_currency import Currency
from modules.smartmirror_news import News
from modules.smartmirror_weather import Weather


class FullScreenApp(object):

    def __init__(self, master, **kwargs):
        self.master = master
        self.bind_keys()
        self._geometry = "400x400+0+0"
        self._fullscreen_toggle = True
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.master.configure(background='black')
        self.master.attributes('-fullscreen', True)
        self.master.focus()
        self.topFrame = Frame(self.master, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=E, padx=100, pady=60)
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=W, padx=100, pady=60)
        self.bottomFrame = Frame(self.master, background='black')
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=NO)
        self.currencyFrame = Frame(self.bottomFrame, background='black')
        self.currencyFrame.pack(side=LEFT)
        self.currency = Currency(self.currencyFrame)
        self.currency.pack(side=BOTTOM, anchor=W)
        self.newsFrame = Frame(self.bottomFrame, background='black')
        self.newsFrame.pack(side=RIGHT)
        self.news = News(self.newsFrame)
        self.news.pack(side=BOTTOM, anchor=E)

    def bind_keys(self):
        self.master.bind('<Return>', self.toggle_fullscreen)
        self.master.bind('<Escape>', self.quit)

    def toggle_fullscreen(self, event):
        geometry = self.master.winfo_geometry()
        self.master.geometry(self._geometry)
        self._geometry = geometry
        self._fullscreen_toggle = not self._fullscreen_toggle
        self.master.attributes('-fullscreen', self._fullscreen_toggle)

    def quit(self, event):
        quit(0)


if __name__ == '__main__':
    root = Tk()
    app = FullScreenApp(root)
    root.mainloop()
