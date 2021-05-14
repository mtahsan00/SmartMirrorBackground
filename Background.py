from __future__ import print_function
from tkinter import *
import tkinter
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
import datetime
import time
import requests
import csv
import textwrap
import sys
import random
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
# root = Tk()
# lab = Label(root)
# dateDisplay = Label(root)
class Clock(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self,parent,bg='black')
        self.time1=''
        self.timeLbl = Label(self, font=('Helvetica', 47), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        self.dayWeek = ''
        self.dayLbl = Label(self, text=self.dayWeek, font=('Helvetica', 18), fg="white", bg="black")
        self.dayLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        date = datetime.datetime.today().strftime('%A %B,%d')
        if time != self.time1:
            self.time1 = time
            self.timeLbl.config(text=time)
        if date != self.dayWeek:
            self.dayWeek = date
            self.dayLbl.config(text=date)

        self.timeLbl.after(200, self.tick)

class ClockBig(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self,parent,bg='black')
        self.time1=''
        self.timeLbl = Label(self, font=('Helvetica', 100), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=N)
        self.dayWeek = ''
        self.dayLbl = Label(self, text=self.dayWeek, font=('Helvetica', 18), fg="white", bg="black")
        self.dayLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        date = datetime.datetime.today().strftime('%A %B,%d')
        if time != self.time1:
            self.time1 = time
            self.timeLbl.config(text=time)
        if date != self.dayWeek:
            self.dayWeek = date
            self.dayLbl.config(text=date)

        self.timeLbl.after(200, self.tick)

class Weather(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self,parent,bg="black")
        self.temperature = ''
        self.forcast = ''
        self.location = ''
        self.icon = ''
        self.sunset = ''
        self.tempMin = ''
        self.tempMax = ''
        #min max frame
        self.mFrame = Frame(self, bg="black")
        self.mFrame.pack(side=RIGHT, anchor=N)
        #Temp Frame
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        #temp Lable Creation
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', 94), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        #Min weather Indicator
        self.minLbl = Label(self.mFrame, font=('Helvetica', 20), fg="white", bg="black")
        self.minLbl.pack(side=TOP, anchor=N)
        #max weather Indicator
        self.maxLbl=Label(self.mFrame, font=('Helvetica', 20), fg="white", bg="black")
        self.maxLbl.pack(side=BOTTOM, anchor=S)
        #Foracast Lable Creation
        self.forecastLbl = Label(self, font=('Helvetica', 16), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        #Sunset creation
        self.sunsetLbl = Label(self, font=('Helvetica', 17), fg="white", bg="black")
        self.sunsetLbl.pack(side=TOP, anchor=W)
        #City Lable creation
        self.cityLbl = Label(self, text="Minneapolis,MN", font=('Helvetica', 18), fg="white", bg="black")
        self.cityLbl.pack(side=TOP, anchor=W)

        self.get_weather()
    def get_weather(self):
        api_address="http://api.openweathermap.org/data/2.5/weather?appid=0267fed153829b1bcacdf19682b24b4d&q=Minneapolis&units=imperial"
        jason_data=requests.get(api_address).json()
        weatherType = jason_data['weather'][0]["description"]
        degree_sign= u'\N{DEGREE SIGN}'
        temp2 =  "%s%s" % (str(int(jason_data['main']["temp"])),degree_sign)
        tempMin2 = "%s%s" % (str(int(jason_data['main']["temp_min"])),degree_sign)
        tempMax2 = "%s%s" % (str(int(jason_data['main']["temp_max"])),degree_sign)
        sunsetGet = jason_data['sys']["sunset"]
        sunsetConvert = datetime.datetime.fromtimestamp(
                int(sunsetGet)
            ).strftime('%I:%M %p ')
        if self.temperature != temp2:
            self.temperature = temp2
            self.temperatureLbl.config(text=temp2)
        if self.tempMin != tempMin2:
            self.tempMin = tempMin2
            self.minLbl.config(text="min " + tempMin2)
        if self.tempMax != tempMax2:
            self.tempMax = tempMax2
            self.maxLbl.config(text="max " + tempMax2)
        if self.sunset != sunsetConvert:
            self.sunset = sunsetConvert
            self.sunsetLbl.config(text="Sunset " + sunsetConvert)
        if self.forcast != weatherType:
            self.forcast = weatherType
            self.forecastLbl.config(text = weatherType)
        self.after(600000,self.get_weather)

class Messages(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self,parent,bg='black')
        self.SAMPLE_SPREADSHEET_ID = '1CB5v25TsFs1pffgv1gMjg1WjxM6YbdmuggUwHFOsJMA'
        self.SAMPLE_RANGE_NAME = "Form Responses 1"
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.message = ''
        self.messageNumber = 0
        self.lineNumber = 20
        self.messageLable=Label(self, font=('Helvetica', 40), fg="white", bg="black")
        self.messageLable.pack(side=TOP, anchor=N)
        self.messages = []
        self.get_messages()
        # with open('Hourly_MessagesH.csv','r') as csv_file: #use "Hourly Messages" for windows and "Hourly_Messages" for raspberry pi's
        #     reader = csv.reader(csv_file)
        #     for line in reader:
        #         self.messages.append(line)
        #         #print(line)
        # random.shuffle(self.messages)
        # with open('Motivation_QuotesH.csv','r') as csv_file: #use "Hourly Messages" for windows and "Hourly_Messages" for raspberry pi's
        #     reader = csv.reader(csv_file)
        #     for line in reader:
        #         self.motivational_quotes.append(line)
        # random.shuffle(self.motivational_quotes)
    def get_messages(self):
        self.sheet = service.spreadsheets()
        self.result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="Form Responses 1").execute()
        values = result.get('values', [])
        if(len(values)<self.lineNumber):
            for i in range(self.lineNumber-1,len(values)):
                for j in range(1,len(values[i])):
                    self.messages.append(values[i][j])
                self.lineNumber+=1
        if(self.messageNumber<=len(self.messages)-1):
           #self.message = "Happy St.Patty's day. Take a phat drink or 2 shots if you see this"
           self.message = self.messages[self.messageNumber]
           self.messageNumber+=1
        else:
           self.message = 'Hungry For More Messages :)'
                #print(messages[self.messageNumber][0])
                #self.messageNumber+=1
                #self.message = "Hello My name is Tayyab And I am here to hell you!"
                #self.message = "Humans are deutorosomes: after fertilization and the cells begin to divide to form a blastula, a concave hole forms, and that is our asshole. Everyone starts out as an asshole. Only some choose not to continue to be one."
        if len(self.message)>40:
            wrapped = textwrap.fill(self.message,70)
            self.messageLable.config(text=wrapped,font=('Helvetica',25))
        else:
            self.messageLable.config(text=self.message)
        self.after(43200000, self.get_messages)

class CalanderMuhammad(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self,parent,bg='black')
        self.calanderItem = ''
        self.locationName = ''
        self.timeItem = ''
        self.dateItem = ''
        #Calander Frame init
        self.cFrame = Frame(self, bg="black",relief="groove",bd=5)
        self.cFrame.pack(side=RIGHT, anchor=N)
        #Date labele Init
        self.dateLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.dateLable.pack(side=LEFT, anchor=E)
        #Time Lable init
        self.timeLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.timeLable.pack(side=LEFT, anchor=E)
        #Calander Labele init
        self.calanderLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.calanderLable.pack(side=LEFT, anchor=E)
        #location lable init
        self.locationLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.locationLable.pack(side=RIGHT, anchor=E)
        self.getCalander()
    def getCalander(self):
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = oauth_file.Storage('tokenPersonal.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentialsPersonal.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting Event(s)')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=4, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        event1 = events[0]
        event2 = events[1]
        event3 = events[2]
        event4 = events[3]
        #event 1
        datePullOne = self.getDate(event1)
        locationPullOne = self.geteventLocation(event1)
        eventNameOne = self.geteventName(event1)
        timeFinalOne = self.getTime(event1)
        #event 2
        datePull2 = self.getDate(event2)
        locationPull2 = self.geteventLocation(event2)
        eventName2 = self.geteventName(event2)
        timeFinal2 = self.getTime(event2)
        #event 3
        datePull3 = self.getDate(event3)
        locationPull3 = self.geteventLocation(event3)
        eventName3 = self.geteventName(event3)
        timeFinal3 = self.getTime(event3)
        #event 4
        datePull4 = self.getDate(event4)
        locationPull4 = self.geteventLocation(event4)
        eventName4 = self.geteventName(event4)
        timeFinal4 = self.getTime(event4)
        #set statements
        if self.dateItem != datePullOne:
            self.dateItem = datePullOne
            self.dateLable.config(text=datePullOne+"\n"+datePull2+"\n"+datePull3+"\n"+datePull4)
        if self.timeItem != timeFinalOne:
            self.timeItem = timeFinalOne
            self.timeLable.config(text=timeFinalOne+"\n"+timeFinal2+"\n"+timeFinal3+"\n"+timeFinal4)
        if self.calanderItem != eventNameOne:
            self.calanderItem = eventNameOne
            self.calanderLable.config(text=eventNameOne+"\n"+eventName2+"\n"+eventName3+"\n"+eventName4)
        if self.locationName != locationPullOne[0]:
            self.locationName = locationPullOne[0]
            self.locationLable.config(text=locationPullOne+"\n"+locationPull2+"\n"+locationPull3+"\n"+locationPull4)
        self.after(3600000, self.getCalander)
    def geteventLocation(self,eventz):
        location = eventz['location']
        locationPul = location.split(",")
        return "-"+locationPul[0]
    def geteventName(self,eventz):
        eventsName = eventz['summary']
        return eventsName
    def getDate(self,eventz):
        start = eventz['start'].get('dateTime', eventz['start'].get('date'))
        timePull = start.split("T")
        date = timePull[0]
        dateEdit = datetime.datetime.strptime(date,"%Y-%m-%d")
        finalDate = dateEdit.strftime("%m/%d/%y")
        return finalDate
    def getTime(self,eventz):
        start = eventz['start'].get('dateTime', eventz['start'].get('date'))
        end = eventz['end'].get('dateTime', eventz['end'].get('date'))
        timePull = start.split("T")
        d = datetime.datetime.strptime(timePull[1][:5], "%H:%M")
        timeGet = d.strftime("%I:%M %p")
        timePully = end.split("T")
        b = datetime.datetime.strptime(timePully[1][:5], "%H:%M")
        timeEndy = b.strftime("%I:%M %p")
        timeFinal1 = timeGet + "-" + timeEndy + ","
        return timeFinal1

class CalanderIan(Frame):
    def __init__(self,parent,*args,**kwargs):
        Frame.__init__(self,parent,bg='black')
        self.calanderItem = ''
        self.locationName = ''
        self.timeItem = ''
        self.dateItem = ''
        #Calander Frame init
        self.cFrame = Frame(self, bg="black",relief="groove",bd=5)
        self.cFrame.pack(side=RIGHT, anchor=N)
        #Date labele Init
        self.dateLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.dateLable.pack(side=LEFT, anchor=E)
        #Time Lable init
        self.timeLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.timeLable.pack(side=LEFT, anchor=E)
        #Calander Labele init
        self.calanderLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.calanderLable.pack(side=LEFT, anchor=E)
        #location lable init
        self.locationLable = Label(self.cFrame, font=('Times New Roman', 18), fg="white", bg="black")
        self.locationLable.pack(side=RIGHT, anchor=E)
        self.getCalander()
    def getCalander(self):
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = oauth_file.Storage('tokenPersonalIan.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentialIan.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting Event(s)')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=4, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        event1 = events[0]
        event2 = events[1]
        event3 = events[2]
        event4 = events[3]
        #event 1
        datePullOne = self.getDate(event1)
        locationPullOne = self.geteventLocation(event1)
        eventNameOne = self.geteventName(event1)
        timeFinalOne = self.getTime(event1)
        #event 2
        datePull2 = self.getDate(event2)
        locationPull2 = self.geteventLocation(event2)
        eventName2 = self.geteventName(event2)
        timeFinal2 = self.getTime(event2)
        #event 3
        datePull3 = self.getDate(event3)
        locationPull3 = self.geteventLocation(event3)
        eventName3 = self.geteventName(event3)
        timeFinal3 = self.getTime(event3)
        #event 4
        datePull4 = self.getDate(event4)
        locationPull4 = self.geteventLocation(event4)
        eventName4 = self.geteventName(event4)
        timeFinal4 = self.getTime(event4)
        #set statements
        if self.dateItem != datePullOne:
            self.dateItem = datePullOne
            self.dateLable.config(text=datePullOne+"\n"+datePull2+"\n"+datePull3+"\n"+datePull4)
        if self.timeItem != timeFinalOne:
            self.timeItem = timeFinalOne
            self.timeLable.config(text=timeFinalOne+"\n"+timeFinal2+"\n"+timeFinal3+"\n"+timeFinal4)
        if self.calanderItem != eventNameOne:
            self.calanderItem = eventNameOne
            self.calanderLable.config(text=eventNameOne+"\n"+eventName2+"\n"+eventName3+"\n"+eventName4)
        if self.locationName != locationPullOne[0]:
            self.locationName = locationPullOne[0]
            self.locationLable.config(text=locationPullOne+"\n"+locationPull2+"\n"+locationPull3+"\n"+locationPull4)
        self.after(3600000, self.getCalander)
    def geteventLocation(self,eventz):
        location = eventz['location']
        locationPul = location.split(",")
        return "-"+locationPul[0]
    def geteventName(self,eventz):
        eventsName = eventz['summary']
        return eventsName
    def getDate(self,eventz):
        start = eventz['start'].get('dateTime', eventz['start'].get('date'))
        timePull = start.split("T")
        date = timePull[0]
        dateEdit = datetime.datetime.strptime(date,"%Y-%m-%d")
        finalDate = dateEdit.strftime("%m/%d/%y")
        return finalDate
    def getTime(self,eventz):
        start = eventz['start'].get('dateTime', eventz['start'].get('date'))
        end = eventz['end'].get('dateTime', eventz['end'].get('date'))
        timePull = start.split("T")
        d = datetime.datetime.strptime(timePull[1][:5], "%H:%M")
        timeGet = d.strftime("%I:%M %p")
        timePully = end.split("T")
        b = datetime.datetime.strptime(timePully[1][:5], "%H:%M")
        timeEndy = b.strftime("%I:%M %p")
        timeFinal1 = timeGet + "-" + timeEndy + ","
        return timeFinal1


class FullScreen():

    def calanderStart(self):
        self.calanderThing = CalanderMuhammad(self.bottomFrame)
        self.calanderThing.pack(side=TOP,anchor='center', pady=40)
        #CalanderIan
        self.calanderThingIan = CalanderIan(self.bottomFrame)
        self.calanderThingIan.pack(side=TOP,anchor='center', pady=40)
        #Message icon
        self.messagesThing = Messages(self.topFrame)
        #self.messagesThing.place(x=575,y=450)
        self.messagesThing.pack(side=BOTTOM, anchor=N, pady=50)
        #clock
        self.clock = Clock(self.topFrame,size=80)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        #weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)

        def onClick():
            print("hello")

    def __init__(self):
        time = datetime.datetime.now().strftime("%I:%M %p")
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
       # self.calanderThing = CalanderMuhammad(self.bottomFrame)
       # self.calanderThing.pack(side=TOP,anchor='center', pady=40)
        #CalanderIan
#        self.calanderThingIan = CalanderIan(self.bottomFrame)
#        self.calanderThingIan.pack(side=TOP,anchor='center', pady=40)
        #Message icon
        self.messagesThing = Messages(self.topFrame)
        #self.messagesThing.place(x=575,y=450)
        self.messagesThing.pack(side=BOTTOM, anchor=N, pady=50)
        #clock
        self.clock = Clock(self.topFrame,size=80)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        #weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)

    #    b = Button(self.topFrame, text="Hell World").pack(padx="10", pady="10", command =self.calanderStart() )
        #width = self.topFrame.get_rect().width
        height = self.tk.winfo_screenheight()/2
        self.state = False
        #CalanderMuhammad
        #self.after(60000, self.__init__)
    # run first time
        # if time == "10:09 PM":
        #     self.clock = ClockBig(self.topFrame,size=80)
        #     self.clock.pack(side=TOP, anchor=N, padx=100, pady=60)
        #     #self.after(60000, self.__init__)
# clock()
if __name__ == '__main__':
    w = FullScreen()
    w.tk.geometry("1080x1700")
    w.tk.attributes("-type","dock")
    w.tk.mainloop()
#
# root.configure(background='black')
# root.mainloop()
