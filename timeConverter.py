import datetime
from datetime import date
from datetime import datetime
import re

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
            
    start = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end = datetime.strptime(end, "%Y-%m-%d %H:%M")
    return [start, end]
