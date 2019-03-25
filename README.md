# places-to-cry-on-campus
Uses the UCLA Grid Search service to find empty classrooms from 8am to 5pm, Monday through Friday <br>
<br>

# Chrome-Extension
This hasn't been published yet, so for now, download the chrome-extension folder and load it with the "Load Unpacked" feature in chrome://extensions/ <br>
The data for all classrooms is merged into a single json file titled "giant_json.json"

# Running the Web Scraper
Download "src" and its contents into an empty folder --> in terminal navigate to that folder, and type "python scrape.py"
Make sure Chromedriver is installed and is in PATH for scrape.py to run (Download link: http://chromedriver.chromium.org/downloads)

# Data
scrape.py writes the time intervals (in military time!) that each classroom is occupied in as a json object, which is stored in week-calendar.txt in each folder.<br/>
example (week_calendar.txt)<br/>

{<br/>
"room_name": "BOELTER_1567",<br/>
"m": [],<br/>
"t": [[1000, 1250],[100, 150]],<br/>
"w": [],<br/>
"r": [[1000, 1250]],<br/>
"f": []<br/>
}<br/>

Here is the file structure for the output:<br/>
+ rooms<br/>
  | BOELTER_####  // format: building-name_room-number<br/>
    | html_data.txt<br/>
    | week_calendar.txt<br/>
  
  
