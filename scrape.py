import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import datetime
import re
from urllib.request import urlopen

def changeToFullTime(hour, isPM):
    num_hours = 0
    if (":" not in hour):
        num_hours = int(hour)
        hour = hour + ":00"
    num_hours = int(hour[0]) if len(hour) == 4 else int(hour[0:2])
        
    if (isPM):
        second_part = hour[1:] if num_hours < 10 else hour[2:]
        if (num_hours != 12):
            num_hours += 12
        hour = str(num_hours) + second_part
    else:
        second_part = hour[1:] if num_hours < 10 else hour[2:]
        first_part = ""
        if (num_hours == 12):
            first_part = "00"
        elif (num_hours < 10):
            first_part = "0" + str(num_hours)
        else:
            first_part = str(num_hours)
            
        hour = first_part + second_part
            
    return hour
    

def convert(string, day):
    start = str(day)
    end = str(day)
    if (string == "All day"):
        start = start + " 00:00"
        end = end + " 23:59"
        ## Return array
    else:
        all_hours = re.findall("[0-9]+:?[0-9]*", string)
        am = "a.m." in string
        pm = "p.m." in string
        
        if (len(all_hours) == 1):
            hour = all_hours[0]
            if (pm):
                hour = changeToFullTime(hour, True)
            else:
                hour = changeToFullTime(hour, False)
                
            start = start + " " + hour
            end = end + " " + hour

        else:
            hour1 = all_hours[0]
            hour2 = all_hours[1]
            
            if (am and pm):
                hour1 = changeToFullTime(hour1, False)
                hour2 = changeToFullTime(hour2, True)
            elif (pm):
                hour1 = changeToFullTime(hour1, True)
                hour2 = changeToFullTime(hour2, True)
            elif (am):
                hour1 = changeToFullTime(hour1, False)
                hour2 = changeToFullTime(hour2, False)
            
            start = start + " " + hour1
            end = end + " " + hour2
            
    start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
    return [start, end]

class Event:
	def __init__(self, event_id, name, start_datetime, end_datetime, building_name, full_location, description):
		self.event_id = event_id
		self.name = name
		self.full_location = full_location
		if full_location is not None:
			if "," in full_location:
				x = full_location.index(",")
				self.building_name = full_location[0:x]
			else:
				self.building_name = full_location
		else:
			self.building_name = full_location
		self.start_datetime = start_datetime
		self.end_datetime = end_datetime
		self.description = description

	def __str__(self) -> str:
		if self.name is not None:
			result = ("Title: " + self.name + "\n")
		if self.event_id is not None:
			result = (result + "event_id: " + self.event_id + "\n")
		if self.start_datetime is not None:
			result = (result + "start_datetime: " + str(self.start_datetime) + "\n")
		if self.end_datetime is not None:
  			result = (result + "end_datetime: " + str(self.end_datetime) + "\n")
		if self.building_name is not None:
			result = (result + "building_name: " + self.building_name + "\n")
		if self.full_location is not None:
			result = (result + "full_location: " + self.full_location + "\n")
		if self.description is not None:
			result = (result + "description: " + self.description + "\n")
		return result




time = date.today()

Events = []
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
                start = ""
                end = ""
                description = ""
                building = ""
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
                                        start = convert(eventTime, week[h])[0]
                                        end = convert(eventTime, week[h])[1]
                        else:
                                start = convert("All day", week[h])[0]
                                end = convert("All day", week[h])[1]

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
                                        
                        var = Event(id, name, start, end, building, location, description)
                        Events.append(var)
                        print(var)

