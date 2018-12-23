# places-to-cry-on-campus
Uses the UCLA Grid Search service to find empty classrooms from 9am to 5pm, Monday through Friday

# Running the Web Scraper
Make sure Chromedriver is installed and is in PATH for scrape.py to run

# Data
scrape.py writes the time intervals (in military time!) that each classroom is occupied in as a json object, which is stored in week-calendar.txt in each folder.
example (week_calendar.txt)

{
"room_name": "BOELTER_1567",
"m": [],
"t": [[1000, 1250],[100, 150]],
"w": [],
"r": [[1000, 1250]],
"f": []
}

Here is the file structure for the output:
+ rooms
  | BOELTER_####         // <building-name>_<room-number>
    | html_data.txt
    | week_calendar.txt
  
  
