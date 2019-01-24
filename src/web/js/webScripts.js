var timer = null;

// metod that start metods which setting components
function startSetMethods(){
	setTime();
	loadPollutantsNames();
	loadDateBorders();
	

}

//load JSON file from server and call callback with response as param
function loadHttpJSON(url, callbackFunction) {
	
	var request = new XMLHttpRequest();  
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
				var response = JSON.parse(this.responseText);
				callbackFunction(response);
            } 
        };
        request.open("GET", url, true);
        request.send();
		
}
	
function loadPollutantsNames() {
	loadHttpJSON('pollutantNames.json', setPollutantsNames);
}

function setPollutantsNames(pollutantsNames){
	
    var select = document.getElementById("substanceSelect");
	names = pollutantsNames['pollutants'];

    for (index in names){
        var option = document.createElement("option");
        option.text = names[index];
        select.add(option);
    }
}

function loadDateBorders() {
	loadHttpJSON('dates.json', setDateBorders);
}

function setDateBorders(dates) {
	minDate = removeHoursFromDate(dates['min']);
	maxDate = removeHoursFromDate(dates['max']);
	setDate(minDate, maxDate);
}

function removeHoursFromDate(dateWithHours) {
	return dateWithHours.split(" ")[0];	
}

//setting time label when application starts
function setTime() {
	document.getElementById("time").innerHTML = "time : " + document.getElementById("time_picker").value + " : 00" ;
}

//changing label for picked time, function is called when timeline panel is changed.
// calling reloadTiff which change raster on current hour and colorScale
function changeTime() {
	setTime();
	actualizeTiff();
}

//read hour and colorscale from inputs and show right tiff
function actualizeTiff() {
	var hour = document.getElementById("time_picker").value;
	var colorscale = document.getElementById("colorScale").value;
	showTiff(hour, colorscale);
}



// function setting calendar, format of parameters is "2015-01-01"
// WARNING! function is called in startSetMethods()
function setDate(minDate,maxDate){
	document.getElementById("calendar_input").min = minDate;
	document.getElementById("calendar_input").max = maxDate;
	document.getElementById("calendar_input").value = minDate;

}


// changing data to picked date
// function is called when date is changed
// parameter is actual date format is "2015-01-01"
function changedDate(date){

    x = date.split("-");
    year = x[0];
    month = x [1];
    day = x[2];
    
	
}

// function is called when substance is changed
//parameter is actual substance
function changedPollutant(value){
    console.log(value);
        
}


//changing  color scale, function is called when select box is changed
// calling reloadTiff which change raster on current colorScale and hour
function changeColorScale(){
	actualizeTiff();
}

function rasterNextHour() {

	time_picker = document.getElementById("time_picker");
	var old_time = Number(time_picker.value);
	var new_time = (old_time + 1) % 24;
	time_picker.value = new_time;
	setTime();
	colorScale = document.getElementById("colorScale").value;
	showTiff(new_time,colorScale);	
	
}

function playAnimation(){
	
	if(timer != null) {
		return;
	}
    console.log("animate2");
	
	rasterNextHour();							//first "tick", otherwise it will wait first second withou changing raster after starting animation
	timer = setInterval(rasterNextHour, 1000);
}

function stopAnimation(){
	if(timer != null) {
		clearInterval(timer);
		timer = null;
	}
}

function showLoading(shown) {
	var elem = document.getElementById("loadingDataSpan");
	if(shown) {
		elem.style.display = "block";
	}
	else {
		elem.style.display = "none";
	}
} 














