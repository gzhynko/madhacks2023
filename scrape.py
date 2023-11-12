import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime

class Event:
        def __init__(self, name, location, date, eventTime, description):
                self.name = name
                self.date = date
                self.location = location
                self.eventTime = eventTime
                self.description = description

time = date.today()
time = str(time)
URL = "https://today.wisc.edu/events/day/" + time
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="main")
iDs = re.findall("<li class='event-row'.*?>", page)
ids[]
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
                                location = location.text
                else:
                        location = detail.find("p", class_="subtitle")
                        location = location.text
                if detail.find("h3", class_="event-title") != -1:
                        name = detail.find("h3", class_="event-title")
                        if name is not None:
                                name = name.text
                date = time;
                if detail.find("p", class_="event-time") != -1:
                        eventTime = detail.find("p", class_="event-time")
                        if eventTime is not None:
                                eventTime = eventTime.text
                        else:
                                eventTime = "All day"
                else:
                        eventTime = "All day"
                var = Event(name, location, date, eventTime, description)
                print(var.name)
                print(var.location)
                print(var.date)
                print(var.eventTime)
                print(var.description)
                id = ids[i]
                 i++
                
                URL = "https://today.wisc.edu/events/view/" + str(id)
                page = requests.get(URL)
