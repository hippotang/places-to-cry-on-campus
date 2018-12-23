import re
import os
from os import listdir
from schedule import Schedule
from bs4 import BeautifulSoup

def to_military(time_range):
    #example time_range: '11:00 AM - 11:50 AM'
    #returns tuple
    #time_range = time_range.translate(None, ':')
    new_string = ""
    num = 0
    for char in time_range:
        if (char != ":"):
            new_string += char
    time_range = new_string
    time_range = time_range.split('- ')
    #convert to military time
    if (time_range[0].find('PM') > 0): 
        if (not(int(time_range[0][:4]) < 1300)): #time is before 1:00 PM
            num = int(time_range[0][:4])+1200
        num = int(time_range[0][:4])
    else: 
        num = int(time_range[0][:4])
    start = num

    if (time_range[1].find('PM') > 0): 
        if (not(int(time_range[1][:4]) < 1300)): #time is before 1:00 PM
            num = int(time_range[1][:4])+1200
        num = int(time_range[1][:4])
    else: 
        num = int(time_range[1][:4])
    end = num

    return [start, end]

def get_week_schedule(file_path):
    f = open(file_path)
    html_data = f.read()
    soup = BeautifulSoup(html_data,'lxml')
    tag = soup.find(id="calendar")
    cal_tag = tag.find("div", {'class':'fc-event-container'})
    cal_tag = cal_tag.parent # <td> <div class = 'fc-event-container' ...

    days = {}
    days['m'] = {}
    days['t'] = {}
    days['w'] = {}
    days['r'] = {}
    days['f'] = {}

    
    for i in days:
        days[i]['root_tag'] = {}
        days[i]['root_tag'] = cal_tag
        days[i]['schedule'] = ""
        cal_tag = cal_tag.next_sibling

    for i in days:
        days[i]['content_tags'] = days[i]['root_tag'].div.find_all('div', {'class': "fc-time"})
        for div in days[i]['content_tags']:
            #days[i]['schedule'] += str(days[i]['content_tags'][a].span.contents) + ", "
            days[i]['schedule'] += str(div['data-full']) + ","
        days[i]['schedule'] = days[i]['schedule'].split(',')
        days[i]['schedule'].pop() # removes last element (which is an empty string)
        
        index = 0
        for j in days[i]['schedule']:
            days[i]['schedule'][index] = to_military(j)
            index+=1
        
        sc = Schedule(days[i]['schedule'])
        days[i]['schedule'] = sc
    
    return days

'''days = {
    m: {
        {root_tag: <div class = 'fc-event-container' ...},
        {content_tags: (list) div.find_all('div', {'class': "fc-time"}}
        {schedule: [1300, 1350], [1400, 1450]}
    }
    t: ...
    w: ...
    r: ...
    f: ...
} '''


#week_calendar = get_week_schedule('html_data.txt')

"""
for day in week_calendar:
    print(str(day))
    week_calendar[day]['schedule'].print_schedule()
"""












