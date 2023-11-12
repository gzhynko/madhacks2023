import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import re
from urllib.request import urlopen

class Event:
        def __init__(self, name, location, date, eventTime, description):
                self.name = name
                self.date = date
                self.location = location
                self.eventTime = eventTime
                self.description = description

time = date.today()

week = []
for j in range(7):
        new_day = time + datetime.timedelta(days=j)
        week.append(str(new_day))
        
for h in range(7):
        
        URL = "https://today.wisc.edu/events/day/" + week[h]
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="main")

        html = urlopen(URL).read().decode("utf-8")
        iDs = re.findall("<li class='event-row'.*?>", html)

        ids = []
        for x in iDs:
                x = re.findall("[0-9]+", x)[0]
                ids.append(x)
        i = 0
        details = results.find_all("div", class_="event-details")

        for detail in details:
                location = ""
                name = ""
                date = ""
                eventTime = ""
                description = ""
                if detail is not None:
                        if detail.find("p", class_="event-location") != -1:
                                location = detail.find("p", class_="event-location")
                                if location is not None:
                                        location = location.text
                                else:
                                        location = detail.find("p", class_="subtitle")
                                        if location is not None:
                                                location = location.text
                        else:
                                location = detail.find("p", class_="subtitle")
                                if locatino is not None:
                                        location = location.text
                                        
                        if detail.find("h3", class_="event-title") != -1:
                                name = detail.find("h3", class_="event-title")
                                if name is not None:
                                        name = name.text
                                        
                        date = week[h];
                        
                        if detail.find("p", class_="event-time") != -1:
                                eventTime = detail.find("p", class_="event-time")
                                if eventTime is not None:
                                        eventTime = eventTime.text
                                else:
                                        eventTime = "All day"
                        else:
                                eventTime = "All day"

                        id = ids[i]
                        i+=1
                
                        URL = "https://today.wisc.edu/events/view/" + str(id)
                        page = requests.get(URL)
                        soup = BeautifulSoup(page.content, "html.parser")
                        results = soup.find(id="main")
                        if results.find("div", class_="event-description") != -1:
                                description = results.find("div", class_="event-description")
                                if description is not None:
                                        description = description.text
                                        
                        var = Event(name, location, date, eventTime, description)
