# places-to-cry-on-campus
Uses the UCLA Grid Search service to find empty classrooms from 9am to 5pm, Monday through Friday

# Running the Web Scraper
Make sure Chromedriver is installed and is in PATH for scrape.py to run

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
  | BOELTER_####         // <building-name>_<room-number><br/>
    | html_data.txt<br/>
    | week_calendar.txt<br/>
  
  
