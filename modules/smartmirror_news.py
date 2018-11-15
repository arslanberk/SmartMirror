from tkinter import *
import requests
import json
from PIL import Image, ImageTk


class News(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        utils_json = open('utils/utils.json')
        self.utils = json.load(utils_json)
        self.newsapi_key = self.utils['news']['newsapi_key']
        self.country = self.utils['news']['country']
        self.page_size = self.utils['news']['page_size']
        translation_json = open('language/%s.json' % (self.utils['language']))
        self.translation = json.load(translation_json)
        self.popular_title = self.translation['popular_news_title']
        self.technology_title = self.translation['technology_news_title']

        self.popular_news = Frame(self.master, bg="black")
        self.popular_news.pack(side=RIGHT)
        self.popular_news_label = Label(self.popular_news, text=self.popular_title, font=('Helvetica', 18), fg="white", bg="black")
        self.popular_news_label.pack(side=TOP, anchor=W)
        self.popular_news_container = Frame(self.popular_news, bg="black")
        self.popular_news_container.pack(side=BOTTOM, anchor=W)

        self.technology_news = Frame(self.master, bg="black")
        self.technology_news.pack(side=RIGHT)
        self.technology_news_label = Label(self.technology_news, text=self.technology_title, font=('Helvetica', 18), fg="white", bg="black")
        self.technology_news_label.pack(side=TOP, anchor=W)
        self.technology_news_container = Frame(self.technology_news, bg="black")
        self.technology_news_container.pack(side=BOTTOM, anchor=W)
        self.get_popular_headlines()
        self.get_technology_headlines()

    def get_popular_headlines(self):
        try:
            for widget in self.popular_news_container.winfo_children():
                widget.destroy()

            popular_news_url = (
            'https://newsapi.org/v2/top-headlines?country=%s&pageSize=%s&sortBy=popularity&apiKey=%s' % (self.country, self.page_size, self.newsapi_key))

            popular_news_request = requests.get(popular_news_url)
            popular_news_obj = json.loads(popular_news_request.text)

            for news in popular_news_obj["articles"]:
                headline = NewsItem(self.popular_news_container, news)
                headline.pack(side=TOP, anchor=W)

        except Exception as e:
            print("Error: %s. Cannot get news." % e)

        self.after(600000, self.get_popular_headlines)

    def get_technology_headlines(self):
        try:
            for widget in self.technology_news_container.winfo_children():
                widget.destroy()

            technology_news_url = (
            'https://newsapi.org/v2/top-headlines?country=%s&pageSize=%s&category=technology&sortBy=popularity&apiKey=%s' % (self.country, self.page_size, self.newsapi_key))

            technology_news_request = requests.get(technology_news_url)
            technology_news_obj = json.loads(technology_news_request.text)

            for news in technology_news_obj["articles"]:
                headline = NewsItem(self.technology_news_container, news)
                headline.pack(side=TOP, anchor=W)

        except Exception as e:
            print("Error: %s. Cannot get news." % e)

        self.after(600000, self.get_technology_headlines)


class NewsItem(Frame):

    def __init__(self, parent, event_name):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.icon_frame = Frame(self, bg="black")
        self.icon_frame.pack(side=LEFT, anchor=N)
        self.icon_label = Label(self.icon_frame, bg='black', image=photo)
        self.icon_label.image = photo
        self.icon_label.pack(side=LEFT, anchor=N)
        self.news_frame = Frame(self, bg="black")
        self.news_frame.pack(side=LEFT, anchor=N)
        self.news_title = event_name['title']
        self.news_title_label = Label(self.news_frame, text=self.news_title, font=('Helvetica', 14), fg="white", bg="black")
        self.news_title_label.pack(side=TOP, anchor=N)


