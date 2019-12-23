from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import time
import pytz
import tkinter as tk
from tkinter import ttk

# -- Windows only configuration  for high DPI screens--
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# -- End Windows only configuration --

age_info = []

# main window for tkinter
class AgeCounter(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Family Age Counter')

        self.geometry("800x900")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.data_frame = AgeData(self)
        self.data_frame.grid(row=0, column=0, sticky='NSWE')


# frame with the elements to print age statistics
class AgeData(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # main frame with text
        self.text = tk.Text(self,
                            height=20,
                            width=50,
                            font=("Verdana", 10),
                            insertborderwidth=0,
                            padx=10, pady=5,
                            relief='flat',
                            spacing1=4
                            )
        self.text.grid(column=0, row=0, sticky='nswe')

        self.text_scroll = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text_scroll.grid(column=1, row=0, sticky=("NSW"))

        self.text['yscrollcommand'] = self.text_scroll.set

        self.update_data_widget()

    def update_data_widget(self):
        for line in age_info:
            self.text.insert(tk.END, line)
            self.text.insert(tk.END, '\n')


class FamilyMember:
    def __init__(self, name, year, month, day, hour, minute):  # exact date of birth with hour and minute
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

        self.count_age()


    def count_age(self):
        tz = pytz.timezone('Europe/Warsaw')
        y = int(time.strftime("%Y", time.localtime()))
        m = int(time.strftime("%m", time.localtime()))
        d = int(time.strftime("%d", time.localtime()))

        bd = date(self.year, self.month, self.day)
        today = date(y, m, d, )
        days = (today - bd).days
        weeks = (today - bd).days // 7
        lacking_days = days - (weeks * 7)

        now = datetime.now()
        birthday = datetime(self.year, self.month, self.day, self.hour, self.minute)
        age = relativedelta(now, birthday)

        age_info.append((datetime.now(tz=tz).strftime("Today is %Y-%m-%d %H:%M %A.\n")))
        age_info.append(f"{self.name} was born on {birthday.strftime('%Y-%m-%d %H:%M %A')}.")
        age_info.append(f'{self.name} is {age.years} years {age.months} months {age.days} days {age.hours} hours'
                        f' {age.minutes} minutes old.')
        age_info.append(f'{self.name} has {(age.years * 12) + age.months} months and {age.days} days.')
        age_info.append(f"{self.name} has {days} days or {weeks} weeks and {lacking_days} days.\n")


# here we create instances of family members (name, year, month, day, hour, minute)
robert = FamilyMember('Robert De Niro', 1943, 8, 17, 3, 0)
al = FamilyMember('Al Pacino', 1940, 4, 25, 11, 2)
henry = FamilyMember('Henry Cavill', 1983, 5, 5, 2, 40)
my_son = FamilyMember('Aleks', 2019, 5, 2, 6, 00)
donald = FamilyMember('Donald Trump',1946, 6, 14, 10, 54)
tom = FamilyMember('Tom Cruise', 1962, 7, 3, 15, 6)


root = AgeCounter()

root.mainloop()
