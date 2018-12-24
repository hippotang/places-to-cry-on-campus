var fs = require('fs');

var rooms = [];
var room_objects = []

////////////////////////////////////
// LOAD JSON OBJECTS
/////////////////////////////////////

function populateRoomObjects() {
  rooms = fs.readdirSync('./rooms');

  for(var i = 0; i<rooms.length; i++) {
    try {
      var text = fs.readFileSync('./rooms/' + rooms[i] + '/week_calendar.txt','utf8')
      room_objects[i] = JSON.parse(text)
    }
    catch {
      console.log(rooms[i] + " isn't correctly formatted")
    }
  }
}

///////////////
// GETTING ROOMS THAT ARE AVAILABLE
/////////////

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

function getAvailableRooms(building,day,time,interval) {
  available_rooms = [];
  for (var i = 0; i<room_objects.length; i++) {
    room = room_objects[i];
    schedule = room[day];
    //console.log(room['room_name']);
    console.log(room['room_name'] + ": " + room['room_name'].indexOf(building))
    if (room['room_name'].indexOf(building)>=0 && isFree(schedule, time, interval)) {
      available_rooms.push(room['room_name']);
      console.log(room['room_name'])
    }
  }
  return available_rooms;
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

