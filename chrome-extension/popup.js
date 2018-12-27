window.onload = init();

var inputTime;
var inputBuilding;
var inputDuration;
var buttonSubmit;

var building;
var time;
var day;
var duration;

var room_data;
var rooms;

function init() {
    inputTime = document.getElementById("time")
    inputBuilding = document.getElementById("building")
    inputDuration = document.getElementById("duration")
    buttonSubmit = document.getElementById("submit");

    chrome.storage.local.get(['room_data'],function(data) {
        room_data = data.room_data;
        console.log(data.room_data);
    });

    var days = ['m', 't', 'w', 'r', 'f', 'm', 'm'];
    var d = new Date();
    day = days[d.getDay()];

    buttonSubmit.onclick = function() {
        building = inputBuilding.value;
        time = formatTime(inputTime.value);
        duration = inputDuration.value;

        rooms = getAvailableRooms(building, day, time, duration)
        var results = document.getElementById('results');
        var tempString = "Any of these rooms should be free right now: <br><br>";
        for (room in rooms) {
            tempString += rooms[room] + '<br>';
        }
        results.innerHTML = tempString;
    }
    
    /*('room_data', function(obj) {
        room_data = obj;
        console.log(obj);
    });*/
   
}

function formatTime(timeString) {
    return parseInt(timeString.substring(0,2) + timeString.substring(3,5));
}

function addTime(time, minutes) {
    var hour1, min1;
    if ((time + minutes)%100 > 59) {
      hour1 = Math.floor(time/100);
      min1 = time%100;
      dh = Math.floor((min1+minutes)/60);
      hour1 += dh;
      min1 = (min1+minutes)-60*dh;
      var temp = (100*hour1+min1);
      if (temp > 2359) {
        temp = temp-2400;
      }
      return temp;
    }
    else {
      return time + minutes;
    }
  }

  
  function getAvailableRooms(building,day,time,interval) {
      console.log('entered the function: ' + building + ', ' + day + ', ' + time + ', ' + interval)
      console.log(room_data);
    available_rooms = [];
    for (room in room_data) {
        //console.log(room_data[room][day]);
        //console.log(day);
        schedule = room_data[room][day];
        //console.log(schedule);
        //console.log(room['room_name']);
        console.log(room_data[room]["room_name"] + ": " + room_data[room]['room_name'].indexOf(building))
        if (room_data[room]['room_name'].indexOf(building)>=0 && isFree(schedule, time, interval)) {
            available_rooms.push(room_data[room]['room_name']);
            console.log(room_data[room]['room_name'])
        }
    }
    return available_rooms;
  }

  function isFree(schedule, time, interval) {
    //console.log('schedule is ' + schedule);
    for(var i = 0; i<schedule.length; i++) {
      tpl = schedule[i];
      //console.log(tpl[0] + ',' + tpl[1]);
      if (time > tpl[0] && time < tpl[1]) {
        console.log('false at: ' + time + 'because it is between ' + tpl[0] + 'and ' + tpl[1]);
        return false;
      }
      var temp = time;
      for (var t = 1; t <= interval; t++) {
        temp = addTime(temp, 1);
        //console.log(temp);
        if (temp > tpl[0] && temp < tpl[1]) {
          console.log('false at: ' + time + 'because it is between ' + tpl[0] + 'and ' + tpl[1]);
          return false;
        }
      }
    }
    return true;
  }