var timer = null;

// metod that start metods which setting components
function startSetMethods(){
	actualizeTimeLabel();
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
function actualizeTimeLabel() {
	document.getElementById("time").innerHTML = "time : " + getActualTime() + " : 00" ;
}

//changing label for picked time, function is called when timeline panel is changed.
// calling reloadTiff which change raster on current hour and colorScale
function changedTime() {
	actualizeTimeLabel();
	actualizeTiff();
	showStations(getActualTime());
}

//read hour and colorscale from inputs and show right tiff
function actualizeTiff() {
	var hour = getActualTime();
	var colorscale = document.getElementById("colorScale").value;
	showTiff(hour, colorscale);
}



// function setting calendar, format of parameters is "2015-01-01"
// WARNING! function is called in startSetMethods()
function setDate(minDate,maxDate){
	calendarInput = document.getElementById("calendar_input");
	calendarInput.min = minDate;
	calendarInput.max = maxDate;
	calendarInput.value = minDate;

}


// changing data to picked date
// function is called when date is changed
// parameter is actual date format is "2015-01-01"
function changedDate(date){
	setInfoSpan('');
	calendarInput = document.getElementById("calendar_input");
	minDate = new Date(calendarInput.min);
	maxDate = new Date(calendarInput.max);
	actualDate = new Date(date);
	
	if(minDate.getTime() > actualDate.getTime() || maxDate.getTime() < actualDate.getTime()) {
		setInfoSpan('Pre tento dátum a emisiu nie sú dáta!');
		return;
	}
	//console.log(, calendarInput.max, date);
	console.log(date);
	rasterForDay(date);
	resetTimePicker();
	stopAnimation(); 
}

// function is called when substance is changed
//parameter is actual substance
function changedPollutant(newPollutant){
    console.log(newPollutant);
	rasterForPollutant(newPollutant);
	loadDateBorders();
	resetTimePicker();
	stopAnimation(); 
        
}


//changing  color scale, function is called when select box is changed
// calling reloadTiff which change raster on current colorScale and hour
function changeColorScale(){
	actualizeTiff();
}

function resetTimePicker() {
	document.getElementById("time_picker").value = 0;
	actualizeTimeLabel();
}

function getActualTime() {
	return Number(document.getElementById("time_picker").value);
}

function rasterNextHour() {

	/*time_picker = document.getElementById("time_picker");
	var old_time = Number(time_picker.value);
	var new_time = (old_time + 1) % 24;
	time_picker.value = new_time;
	actualizeTimeLabel();
	colorScale = document.getElementById("colorScale").value;
	showTiff(new_time,colorScale);	*/
	
	time_picker = document.getElementById("time_picker");
	var old_time = Number(time_picker.value);
	var new_time = (old_time + 1) % 24;
	time_picker.value = new_time;
	changedTime();
	
}

function playAnimation(){
	
	if(timer != null) {
		return;
	}
	
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
	
	if(shown) {
		setInfoSpan("Načítavam dáta...");
	}
	else {
		setInfoSpan("");
	}
} 

function setInfoSpan(msg) {
	var elem = document.getElementById("infoSpan");
	elem.innerHTML = msg;
	elem.style.display = "block";
	if(msg == "") {
		elem.style.display = "none";
	}
	
}














