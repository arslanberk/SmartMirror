from tkinter import *
import requests
import json


class Currency(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        utils_json = open('utils/utils.json')
        self.utils = json.load(utils_json)
        self.usd_data = ''
        self.eur_data = ''
        self.gbp_data = ''
        self.rub_data = ''
        self.currency_frame = Frame(self.master, bg='black')
        self.currency_frame.pack(side=LEFT, anchor=W)

        self.usd_label = Label(self.currency_frame, font=('Helvetica', 30), fg="white", bg="black")
        self.usd_label.pack(side=TOP, anchor=N)
        self.eur_label = Label(self.currency_frame, font=('Helvetica', 30), fg="white", bg="black")
        self.eur_label.pack(side=TOP, anchor=N)
        self.gbp_label = Label(self.currency_frame, font=('Helvetica', 30), fg="white", bg="black")
        self.gbp_label.pack(side=TOP, anchor=N)
        self.rub_label = Label(self.currency_frame, font=('Helvetica', 30), fg="white", bg="black")
        self.rub_label.pack(side=TOP, anchor=N)

        self.get_currency_rates()

    def get_currency_rates(self):
        try:
            usd_request_url = "https://api.exchangeratesapi.io/latest?base=%s" % ('USD')
            eur_request_url = "https://api.exchangeratesapi.io/latest?base=%s" % ('EUR')
            gbp_request_url = "https://api.exchangeratesapi.io/latest?base=%s" % ('GBP')
            rub_request_url = "https://api.exchangeratesapi.io/latest?base=%s" % ('RUB')
            exchange_to = self.utils['currency']['exchange_to']

            usd_request = requests.get(usd_request_url)
            usd_obj = json.loads(usd_request.text)
            usd_rate = "USD: %0.2f" % (usd_obj['rates'][exchange_to])

            eur_request = requests.get(eur_request_url)
            eur_obj = json.loads(eur_request.text)
            eur_rate = "EUR: %0.2f" % (eur_obj['rates'][exchange_to])

            gbp_request = requests.get(gbp_request_url)
            gbp_obj = json.loads(gbp_request.text)
            gbp_rate = "GBP: %0.2f" % (gbp_obj['rates'][exchange_to])

            rub_request = requests.get(rub_request_url)
            rub_obj = json.loads(rub_request.text)
            rub_rate = "RUB: %0.2f" % (rub_obj['rates'][exchange_to])

            if self.usd_data != usd_rate:
                self.usd_data = usd_rate
                self.usd_label.config(text=usd_rate)

            if self.eur_data != eur_rate:
                self.eur_data = eur_rate
                self.eur_label.config(text=eur_rate)

            if self.gbp_data != gbp_rate:
                self.gbp_data = gbp_rate
                self.gbp_label.config(text=gbp_rate)

            if self.rub_data != rub_rate:
                self.rub_data = rub_rate
                self.rub_label.config(text=rub_rate)

        except Exception as e:
            print("Error: %s. Cannot get currencies." % e)

        self.after(600000, self.get_currency_rates)


