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
from usoup import isError
from usoup import get_error_message

import schedule
from schedule import Schedule

from enum import Enum

ROOT_DIR = '..'
html_file_name = 'html_data.txt'
json_file_name = 'info.txt'
rooms_folder = 'rooms'

class Results(Enum):
    NO_ERROR_MESSAGE = 0
    ERROR_MESSAGE_FOUND = 1
    CALENDAR_FOUND = 2


# returns false if the room does not have its own calendar
def scrape(parent_folder, term, building, room_number, html_file_name, json_file_name, delay):
    folder_name = initRoomFolder(parent_folder, building, room_number)
    path_to_room_folder = ROOT_DIR + '/' + parent_folder + '/' + folder_name 
    html_file_path = path_to_room_folder + '/' + html_file_name
    print(html_file_path)
    result = writeHTMLData(toUrl(term, building, room_number), path_to_room_folder, html_file_name, delay)
    createJSONFile(path_to_room_folder, folder_name, html_file_name, json_file_name, result)

def toUrl(term, building, room_number):
    return ("https://www.registrar.ucla.edu/Faculty-Staff/Classrooms-and-Scheduling/Classroom-Grid-Search/Classroom-Details?class=" 
    + str(building) + "%20%7C%20%200" + str(room_number) + "%20%20&term=" + str(term))

# creates a folder with the name <building>_<room_number> and populates it with
# html_data.txt and info.txt
# returns name of this folder (e.g. "BOELTER_5741")
def initRoomFolder(parent_folder, building, room_number):
    if (not (os.path.exists(ROOT_DIR + '/' + parent_folder))):
        os.mkdir(ROOT_DIR + '/' + parent_folder)
    path_to_room_folder = ROOT_DIR + '/' + parent_folder + '/' + (building + '_' + str(room_number))
    try:
        os.mkdir(path_to_room_folder)
    except:
        # folder already exists
        pass
    return (building + '_' + str(room_number))

# writes html data of a given url to "path_to_room_folder/html_file_name" 
# returns an enum from Results 
def writeHTMLData(url, path_to_room_folder, html_file_name, delay):
    html_file_path = path_to_room_folder + '/' + html_file_name
    browser = webdriver.Chrome()
    browser.get(url)

    try: element = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "fc-view-container")))
    except: element = False

    if element != False:
        f = open(html_file_path, 'w')
        f.write(browser.page_source)
        browser.close()
        print("Results.CALENDAR_FOUND")
        return Results.CALENDAR_FOUND

    try: error_element = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "lblErr")))
    except: error_element = False

    if error_element != False:
        f = open(html_file_path, 'w')
        f.write(browser.page_source)
        browser.close()
        print("Results.ERROR_MESSAGE_FOUND")
        return Results.ERROR_MESSAGE_FOUND
    else:
        f = open(html_file_path, 'w')
        f.write(browser.page_source)
        browser.close()
        print("Results.NO_ERROR_MESSAGE")
        return Results.NO_ERROR_MESSAGE

# call this only after html data is written into each folder
def createJSONFile(path_to_room_folder, folder_name, html_file_name, json_file_name, result):
    html_file_path = path_to_room_folder + '/' + html_file_name
    json_file_path = path_to_room_folder + '/' + json_file_name
    isError = (result == Results.NO_ERROR_MESSAGE or result == Results.ERROR_MESSAGE_FOUND)

    f = open(json_file_path, 'w')
    f = open(json_file_path, 'r+')
    f.write('{' + '\n')
    f.write(' "room_name": "' + folder_name + '",\n ')
    f.write(' "error": ' + str(isError).lower() + ',\n')

    if (isError):
        f.write(' "error_message": " ' + get_error_message(html_file_path) + ' ",\n ')  
    else:
        print('writing days')
        days = ['m','t','w','r','f']
        temp_week_schedule = get_week_schedule(html_file_path)
        for day in days:
            temp_string = temp_week_schedule[day]['schedule'].string_schedule()
            temp_string = removeAndReturnLastCharacter(temp_string)
            temp_string = '[' + temp_string + '],'
            f.write("\"" + day + "\": " + temp_string + '\n')

    #close JSON with a bracket
    f.seek(0, 2)
    pos = f.tell()
    f.seek(pos-2)
    f.write('\n')
    f.write('}')
    f.close()

# combines all jsons into a giant json in a specified folder path   
def makeGiantJSON(path_to_rooms, path_to_folder):
    folders = os.listdir(path_to_rooms)
    print(folders)
    giant_json = open(path_to_folder + '/giant_json.json', 'w+')
    #giant_json = open(path_to_folder + '/giant_json.txt', 'a')
    giant_json.write('{' + '\n')
    index = 0
    for folder in folders:
        giant_json.write('\n"' + str(index) + '": ')
        tempfile = open(path_to_rooms + '/' + folder + '/' + str(json_file_name))
        giant_json.write(tempfile.read() + ',')
        index = index + 1
    #move to the end of the file
    giant_json.seek(0, 2)
    pos = giant_json.tell()
    giant_json.seek(pos-1)
    giant_json.write('\n}')
    giant_json.close()
    print('wrote giant json')

def removeAndReturnLastCharacter(a):
    #c = a[-1]
    a = a[:-1]
    return a

#test
if __name__ == "__main__":  
    print(ROOT_DIR + '/' + rooms_folder)
    if (os.path.exists(ROOT_DIR + '/' + rooms_folder)):
        shutil.rmtree(ROOT_DIR + '/' + rooms_folder)
    delay = 10 # in seconds
    term = '19W'
    building = 'BOELTER'
    
    #room_numbers = [3400,3424,3436,3564,3704,3760,4275,4283,4404,4413,5249,5252,5264,5272,5273,5280,5419,5420,5422,5436,5440,5513,5514,5273]
    room_numbers = [5249,5273,5252,5264,5272,5273,5280,5419,5420,5422,5436,5440,5513,5514]
    
    for i in room_numbers:
        scrape(rooms_folder, term, building, i, html_file_name, json_file_name, delay)

    makeGiantJSON("../rooms", "..")
