var path = 'rooms';
var file_name = 'week_calendar.txt';
var giant_json_path = 'giant_json.json';
var giant_json = {};

chrome.runtime.onInstalled.addListener(function () {
    function loadJSON(callback) {   
        var xobj = new XMLHttpRequest();
            xobj.overrideMimeType("application/json");
        xobj.open('GET', 'giant_json.json', true); // Replace 'my_data' with the path to your file
        xobj.onreadystatechange = function () {
              if (xobj.readyState == 4 && xobj.status == "200") {
                // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
                callback(xobj.responseText);
              }
        };
        xobj.send(null);  
    }
    
    function init() {
        loadJSON(function(response) {
         // Parse JSON string into object
           giant_json = JSON.parse(response);
           chrome.storage.local.set({'room_data': giant_json}, function() {
               console.log('giant_json set in background: ' + JSON.stringify(giant_json));
           });
        });
    }

    init();

    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
        chrome.declarativeContent.onPageChanged.addRules([{
                conditions: [new chrome.declarativeContent.PageStateMatcher({
                    pageUrl: { schemes: ['https'] },
                })
            ],
                actions: [new chrome.declarativeContent.ShowPageAction()]
            }
        ]);
    })

})