import threading
from tkinter import Label, Entry, Button, Tk
import tkinter as tk
import requests
from datetime import datetime
import time
import pyttsx3
import smtplib
engine = pyttsx3.init()
stop = False

window = Tk()
window.title("Vaccine Notifier")
window.geometry("300x400")

class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        execute()

def execute():
    while True:
        global stop
        pincode = pincode_value.get()
        is18 = var1.get()
        is45 = var2.get()
        audio = var3.get()
        email = var4.get()
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="
        url = url + pincode + "&date=" + date
        headers = {'content-type': "application/json"}
        response = requests.request("GET", url, headers=headers)
        response = response.json()
        centres = response['centers']
        msg45 = ''
        msg18 = ''
        for centre in centres:
            try:
#                print(centre['name'])
                sessions = centre['sessions']
                if len(sessions) > 0:
                    for session in sessions:
                        date = session['date']
                        capacity = session['available_capacity']
                        age = session['min_age_limit']
                        if capacity > 0:
                            if age == 45:
                                msg45 = msg45 + centre['name'] + " for age 45+\n"
                                msg45 = msg45 + str(date) +   " Capacity: " + str(capacity) + "\n\n"
                            else:
                                msg18 = msg18 + centre['name'] + " for age 18 to 44\n"
                                msg18 = msg18 + str(date) +   " Capacity: " + str(capacity) + "\n\n"
#                        print("Date: ", date, "Capacity: ", capacity, "Age: ", age)
            except Exception as error:
                print(error)

        if audio == 1:
            if msg45 != '' and is45 == 1:
                engine.say("Vaccines are avaiable for 45 +")
                engine.runAndWait()
            if msg18 != '' and is18 == 1:
                engine.say("Vaccines are avaiable for 18 +")
                engine.runAndWait()

        if email == 1:
            gmail_user = ''
            gmail_password = ''
            sent_from = gmail_user
            to = [email_value.get()]
            body = """\
Subject: Vaccine Availability Notification"""
            if is45 == 1:
                body = body + "\n\n" + msg45
            if is18 == 1:
                body = body + "\n\n" + msg18
            try:
                if (msg18 != '' and is18 == 1) or (msg45 != '' and is45 == 1):
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, body)
                    server.close()
                    print("Email sent...")
            except:
                print('Something went wrong...')

        msg = ''
        if msg45 == 1:
            msg = msg + msg45
        if msg18 == 1:
            msg = msg + msg18
        logs.config(text=msg)
        time.sleep(30)
        if stop:
            break

thread1 = myThread()
def start_thread():
    global thread1, stop
    stop = False
    thread1 = myThread()
    thread1.start()

def stop_thread():
    global stop
    stop = True

title = Label(window, text="Vaccine Notifier - India", fg='blue', font=('Helvetica', 16)).place(x=40, y=10)
pin_label = Label(window, text="Enter Pin Code: ", fg='black', font=('Helvetica', 12)).place(x=20, y=60)
pincode_value = Entry(window, text="", fg='black')
pincode_value.place(x=150, y=60)

age_grp = Label(window, text="Select Age Group: ", fg='black', font=('Helvetica', 12)).place(x=20, y=90)
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
var4 = tk.IntVar()
c1 = tk.Checkbutton(window, text='18 to 44', variable=var1, onvalue=1, offvalue=0)
c1.place(x=20, y=110)
c2 = tk.Checkbutton(window, text='45+', variable=var2, onvalue=1, offvalue=0)
c2.place(x=20, y=130)

settings_label = Label(window, text="Settings", fg='black', font=('Helvetica', 12)).place(x=20, y=160)
c3 = tk.Checkbutton(window, text='Audio Notifications', variable=var3, onvalue=1, offvalue=0)
c3.place(x=20, y=180)
c4 = tk.Checkbutton(window, text='Email Notifications', variable=var4, onvalue=1, offvalue=0)
c4.place(x=20, y=200)
email_label = Label(window, text="Email ID", fg='blue', font=('Helvetica', 8)).place(x=50, y=220)
email_value = Entry(window, text="", fg='black')
email_value.place(x=100, y=220)

start = Button(window, text="Start", fg='black', bd=5, bg='green', font=('Helvetica', 11), command=start_thread).place(x=50, y=270)
stop = Button(window, text="Stop", fg='black', bd=5, bg='red', font=('Helvetica', 11), command=stop_thread).place(x=180, y=270)
logs = Label(window, text="No new notifications", fg='black', font=('Helvetica', 9))
logs.place(x=20, y=340)

window.mainloop()
