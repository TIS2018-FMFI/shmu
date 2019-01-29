var mymap = null;
var layer = null;
var tiffArr = new Array(24);
var stationsArr = null;
var legend = null;

document.addEventListener('DOMContentLoaded', function() {
	createMap();
	rasterForDay('0000-00-00');
	loadHttpJSON('stations.json', loadStations);
}, false);

function rasterForDay(date) {
	showLoading(true);
	setServerRasterDateHTTP(date);
} 

function rasterForPollutant(pollutant) {
	showLoading(true);
	setServerPollutantHTTP(pollutant);
}

function setServerRasterDateHTTP(date) {
	 var request = new XMLHttpRequest();  
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
				if(request.response != 'false') {
					loadTiffsHTTP();
					loadHttpJSON('stations.json', loadStations);
				}
				else {
					setInfoSpan("Pre tento dátum a emisiu nie sú dáta!");
				}
				
            }
        };
		var url = 'setDate';
		var params = "date=" + date;
        request.open("GET", url+"?"+params, true, true);
        request.send();
}

function setServerPollutantHTTP(pollutant) {
	var request = new XMLHttpRequest();  
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
				if(request.response != 'false') {	
					rasterForDay('0000-00-00');
				}
				else {
					setInfoSpan("Pre túto emisiu nie sú dáta!");
				}
				
            }
        };
		var url = 'setPollutant';
		var params = "pollutant=" + pollutant;
        request.open("GET", url+"?"+params, true, true);
        request.send();
}


function loadTiffsHTTP() {
	for(i=0;i<24;i++) {
		url = 'raster' + i + '.tiff'
		loadTiffHTTP(url,i);
	}
}

function loadTiffHTTP(url,i) {
	 var request = new XMLHttpRequest();  
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
				tiffArr[i] = request.response;
				if(i == 23) {						//loaded all tiffs
					showFirst();
					showLoading(false);
				}
            }
        };
		var params = "tiff=true";
        request.open("GET", url+"?"+params, true, true);
        request.responseType = "arraybuffer";
        request.send();
}

function showFirst() {
	colorscale = document.getElementById("colorScale").value;
	showTiff(0, colorscale);
}


function createMap() {
	mymap = L.map('mapid').setView([49.372288, 17.101004], 6);
	 
	 var mainLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: 'pk.eyJ1IjoidmlkbyIsImEiOiJjam9kMnhrY2swdHU4M3FuMnRtMmZtZXkzIn0.0eihDz33xkCGLhdWOvDi3Q'
	}).addTo(mymap);
	
	mymap.on('click', function(e) {
		conc = layerTmp.getValueAtLatLng(e.latlng.lat, e.latlng.lng);
		var popLocation= new L.LatLng(e.latlng.lat,e.latlng.lng);
		mymap.on('click', function(e) {
			if (conc === undefined){
				return;
			}
			var popLocation= e.latlng;
			var popup = L.popup()
				.setLatLng(popLocation)
				.setContent('<p>'+ Math.round(conc*100)/100 +'</p>'+"<img src='http://joshuafrazier.info/images/maptime.gif' alt='maptime logo gif' width='90px'/>")
				.openOn(mymap);
    	});
	});
}

function loadStations(stations) {
	stationsArr = stations;
	showStations(0);
}


function showStations(hour) {
	if(stationsArr == null) return;
	console.log('stanice ' + hour);
	console.log(stationsArr);
	
	L.icon = function (options) {
    return new L.Icon(options);
};

	var LeafIcon = L.Icon.extend({
    options: {
        iconSize:     [30, 30],
        iconAnchor:   [15, 30],
		popupAnchor:  [0, -30]

    }
});
	
	
	var numStations = stationsArr["cnt"];
	var justStations = stationsArr["stations"];
	var yellowIcon = new LeafIcon({iconUrl: 'markerYellow.png'}),
		redIcon = new LeafIcon({iconUrl: 'markerRed.png'}),
		greenIcon = new LeafIcon({iconUrl: 'markerGreen.png'});
		

	for (i=0; i<numStations; i++) {
		
		var seenVal;
		var icon;
		var measuredValues = stationsArr["stations"][i]["measured"];
		
		if(measuredValues == null) {
			icon = yellowIcon;
			seenVal = 'Not measuring';
		}
		else {
			var measuredValue = stationsArr["stations"][i]["measured"][hour];
		}
	
		
		if ( measuredValue < 0) {				// -1, station is not active
			icon = redIcon;
			seenVal = 'Not active';
		}else if ( measuredValue == null) {			// station was never measuring in that time or that pollutant
			icon = yellowIcon;
			seenVal = 'Not measuring';
		} else {
			seenVal = Math.round(measuredValue*100)/100;
			icon = greenIcon;
		}
		
		var html = '<p><b>' + justStations[i]["name"]+ '</b>' +
			'<br>location: '+justStations[i]["y"]+', '+justStations[i]["x"]+
			'<br>station type: '+ justStations[i]["type"]+
			'<br>location type: '+justStations[i]["loctype"]+
			'<br>measured: '+seenVal+'</p>';
			
		var marker = L.marker([	justStations[i]["y"],
								justStations[i]["x"]], {icon: icon})
								.addTo(mymap)
								.bindPopup(html);	
	}
}



function showTiff(index, colorScale = 'rainbow') {
	
	
	var options = {
				band: 0,
				displayMin: 0,
				displayMax: 30,
				name: 'Wind speed',
				colorScale: colorScale,
				clampLow: false,
				clampHigh: true,
				//vector:true,
				arrowSize: 20,
				crossorigin:null,
				opacity:0.5,				
	};
	
	tiff = tiffArr[index];
	tmpTiff = index;
	
	layerTmp = L.leafletGeotiff(tiff=tiff, options=options);
	if(layer != null) mymap.removeLayer(layer);
	mymap.addLayer(layerTmp);
	layer = layerTmp;
	
	if (!legend){
		createLegend();
	} else {
		updateLegend();
	}
}

function setContainer(div){
	var parent = document.createElement("DIV");
	var leftmin = document.createElement("DIV");
	var rightmax = document.createElement("DIV");
	parent.setAttribute("class", "minmaxLegend");
	leftmin.setAttribute("class", "minLegend");
	rightmax.setAttribute("class", "maxLegend");
	parent.appendChild(leftmin);
	parent.appendChild(rightmax);
	leftmin.innerText = "Min: " + Math.round(Math.min.apply(Math,layer.raster.data)*100)/100;
	rightmax.innerText = "Max: " + Math.round(Math.max.apply(Math,layer.raster.data)*100)/100;
	var colorImg = document.createElement("IMG");
	colorImg.src = layer.colorScaleData;
	colorImg.style.height = '10px';
	colorImg.style.width = '200px';
	div.appendChild(colorImg);
	div.appendChild(parent);
	return div;
}

 function createLegend() {
	legend = L.control({ position: "bottomright" });
	legend.onAdd = function(map) {
  		var div = L.DomUtil.create("div", "legend");
	  	return setContainer(div);
	};
	legend.addTo(mymap);
}

 function updateLegend(){
	div = legend.getContainer();
	div.innerHTML = "";
	setContainer(div);

 }