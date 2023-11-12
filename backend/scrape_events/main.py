import requests
import base64
import functions_framework
import re

from bs4 import BeautifulSoup

from datetime import date
import datetime

from common import *


# triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def run_scrape_events(cloud_event):
    message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    if message == "scrape events":
        print("running scrape events")
        event_data = scrape_event_data()
        print(
            "scraped " + str(len(event_data)) + " events successfully, publishing to DB"
        )
        publish_to_db(event_data)


def changeToFullTime(hour, isPM):
    num_hours = 0
    if ":" not in hour:
        num_hours = int(hour)
        hour = hour + ":00"
    num_hours = int(hour[0]) if len(hour) == 4 else int(hour[0:2])

    if isPM:
        second_part = hour[1:] if num_hours < 10 else hour[2:]
        if num_hours != 12:
            num_hours += 12
        hour = str(num_hours) + second_part
    else:
        second_part = hour[1:] if num_hours < 10 else hour[2:]
        first_part = ""
        if num_hours == 12:
            first_part = "00"
        elif num_hours < 10:
            first_part = "0" + str(num_hours)
        else:
            first_part = str(num_hours)

        hour = first_part + second_part

    return hour


def convert(string, day):
    start = str(day)
    end = str(day)
    if string == "All day":
        start = start + " 00:00"
        end = end + " 23:59"
        ## Return array
    else:
        all_hours = re.findall("[0-9]+:?[0-9]*", string)
        am = "a.m." in string
        pm = "p.m." in string

        if len(all_hours) == 1:
            hour = all_hours[0]
            if pm:
                hour = changeToFullTime(hour, True)
            else:
                hour = changeToFullTime(hour, False)

            start = start + " " + hour
            end = end + " " + hour

        else:
            hour1 = all_hours[0]
            hour2 = all_hours[1]

            if am and pm:
                hour1 = changeToFullTime(hour1, False)
                hour2 = changeToFullTime(hour2, True)
            elif pm:
                hour1 = changeToFullTime(hour1, True)
                hour2 = changeToFullTime(hour2, True)
            elif am:
                hour1 = changeToFullTime(hour1, False)
                hour2 = changeToFullTime(hour2, False)

            start = start + " " + hour1
            end = end + " " + hour2

    start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
    return [start, end]


def scrape_event_data() -> [Event]:
    time = date.today()

    events = []
    week = []
    for j in range(7):
        new_day = time + datetime.timedelta(days=j)
        week.append(str(new_day))

    for h in range(7):
        URL = "https://today.wisc.edu/events/day/" + week[h]
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="main")

        iDs = re.findall("<li class='event-row'.*?>", page.text)

        ids = []
        for x in iDs:
            x = re.findall("[0-9]+", x)[0]
            ids.append(x)
        i = 0
        details = results.find_all("div", class_="event-details")

        for detail in details:
            location = ""
            name = ""
            start = ""
            end = ""
            description = ""
            building = ""
            if detail is not None:
                if detail.find("p", class_="event-location") != -1:
                    location = detail.find("p", class_="event-location")
                    if location is not None:
                        location = location.text.strip()
                    else:
                        location = detail.find("p", class_="subtitle")
                        if location is not None:
                            location = location.text.strip()
                else:
                    location = detail.find("p", class_="subtitle")
                    if location is not None:
                        location = location.text.strip()

                if detail.find("h3", class_="event-title") != -1:
                    name = detail.find("h3", class_="event-title")
                    if name is not None:
                        name = name.text.strip()

                if detail.find("p", class_="event-time") != -1:
                    eventTime = detail.find("p", class_="event-time")
                    if eventTime is not None:
                        eventTime = eventTime.text
                        start = convert(eventTime, week[h])[0]
                        end = convert(eventTime, week[h])[1]
                    else:
                        start = convert("All day", week[h])[0]
                        end = convert("All day", week[h])[1]
                else:
                    start = convert("All day", week[h])[0]
                    end = convert("All day", week[h])[1]

                id = ids[i]
                i += 1

                URL = "https://today.wisc.edu/events/view/" + str(id)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find(id="main")
                if results.find("div", class_="event-description") != -1:
                    description = results.find("div", class_="event-description")
                    if description is not None:
                        description = description.text.strip()

                event = Event(id, name, start, end, building, location, description)
                events.append(event)

    return events


def publish_to_db(event_data: [Event]):
    # clear all events in the db
    events_db.delete_many({})

    # convert the event data from array of classes to array of dictionaries (required by insert_many)
    doc = []
    for e in event_data:
        doc.append(e.__dict__)

    events_db.insert_many(doc)
    print("inserted all events into the DB!")
