import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from os import listdir
import shutil

import usoup
from usoup import get_week_schedule

import schedule
from schedule import Schedule

def scrape(url, delay, output_file_path):
    browser = webdriver.Chrome()
    browser.get(url)
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fc-view-container"))
        )
    except:
        print("element not found")
        browser.close()
        return False
    else:
        #write browser.page_source to file
        f = open(output_file_path,'w')
        f.write(browser.page_source)
        print("wrote " + url + "to " + output_file_path)
        browser.close()
        return True
    return True

url_arr = []
term = '19W' # change to 19S in the spring

if os.path.exists('../rooms') and os.path.isdir('../rooms'):
    shutil.rmtree('../rooms')

os.mkdir('../rooms')

# Boelter Hall
rooms = [1541,1567,1805,2444,2760,2808,3400,3424,3436,3564,3704,3760,4275,4283,4404,4413,5249,5252,5264,5272,5273,5280,5419,5420,5422,5436,5440,5513,5514]
n = 0
for i in rooms:
    url_arr.append("https://www.registrar.ucla.edu/Faculty-Staff/Classrooms-and-Scheduling/Classroom-Grid-Search/Classroom-Details?class=BOELTER%20%7C%20%200" + str(i) + "%20%20&term=" + term)
    os.mkdir('../rooms/BOELTER_' + str(i))
    if (not scrape(url_arr[n], 5, ('../rooms/BOELTER_' + str(i) + '/html_data.txt'))):
        print("room " + str(i) + "isn't doing anything this quarter")
        os.rmdir('../rooms/BOELTER_' + str(i))
    n = n+1

# BUNCHE hall
rooms = ['1209B', '1221A', '1221B', '1221D', '1261','1265', '2121', '2150', '2156', '2160', '2168', '2173', '2174','2178', '2181', '2209A', '2249', '3117', '3123', '3143', '3150', '3153', '3156', '3157', '3164', '3170', '3178', '3211', '3357', '4276', '4357', '5288', '6250', '6265', '6299', '6339', '6345', '7386', '9294', '9383', '10383', '11372', 'A152', 'A162', 'A163']
n = 0
for i in rooms:
    url_arr.append('https://www.registrar.ucla.edu/Faculty-Staff/Classrooms-and-Scheduling/Classroom-Grid-Search/Classroom-Details?class=BUNCHE%20%20%7C%20%200' + str(i) +  '%20&term=' + term)
    os.mkdir('../rooms/BUNCHE_' + str(i))
    if (not scrape(url_arr[n], 5, ('../rooms/BUNCHE_' + str(i) + '/html_data.txt'))):
        print("room " + str(i) + "isn't doing anything this quarter")
        os.rmdir('../rooms/BUNCHE_' + str(i))
    n = n+1

def removeAndReturnLastCharacter(a):
        #c = a[-1]
        a = a[:-1]
        return a

folders = os.listdir('../rooms')

for folder in folders:
    #shutil.rmtree(folder)
    path = '../rooms/' + folder + '/week_calendar.txt'
    path2 = '../rooms/' + folder + '/html_data.txt'
    f2 = open(path,'a')
    f = open(path, 'r+')
    temp_week_schedule = get_week_schedule(path2)
    week_schedule = {}
    f.write('{' + '\n')
    f.write('"room_name": "' + folder + '",\n')
    for day in temp_week_schedule:
        week_schedule[day] = temp_week_schedule[day]['schedule']
        temp_string = temp_week_schedule[day]['schedule'].string_schedule()
        temp_string = removeAndReturnLastCharacter(temp_string)
        temp_string = '[' + temp_string + '],'
        f.write("\"" + day + "\": " + temp_string + '\n')
    f.seek(0, 2)
    pos = f.tell()
    f.seek(pos-2)
    f.write('\n')
    f.write('}')
