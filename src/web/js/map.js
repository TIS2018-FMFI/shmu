var mymap = null;
var layer = null;
var tiffArr = new Array(24);

document.addEventListener('DOMContentLoaded', function() {
	createMap();
	rasterForDay('0000-00-00');
}, false);

function rasterForDay(date) {
	showLoading(true);
	loadTiffsHTTP(date);
	loadStations();
	showLoading(false);
} 


function loadTiffsHTTP(date) {
	for(i=0;i<24;i++) {
		url = 'raster' + i + '.tiff'
		loadTiffHTTP(url,i, date);
	}
}

function loadTiffHTTP(url,i, date) {
	 var request = new XMLHttpRequest();  
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
				tiffArr[i] = request.response;
				console.log("loaded " + i);
				if(i == 23) {						//loaded all tiffs
					showFirst();
				}
            }
        };
		var params = "tiff=true&date=" + date;
        request.open("GET", url+"?"+params, true, true);
        request.responseType = "arraybuffer";
        request.send();
}

function showFirst() {
	showTiff(0);
}


function createMap() {
	mymap = L.map('mapid').setView([49.372288, 17.101004], 6);
	 
	 var mainLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: 'pk.eyJ1IjoidmlkbyIsImEiOiJjam9kMnhrY2swdHU4M3FuMnRtMmZtZXkzIn0.0eihDz33xkCGLhdWOvDi3Q'
	}).addTo(mymap);
}

function loadStations() {
	console.log('Vytvaram stanice');
	loadHttpJSON('stations.json', showStations);
}



function showStations(arrStations, hour=0) {
	L.icon = function (options) {
    return new L.Icon(options);
};

	var LeafIcon = L.Icon.extend({
    options: {
        iconSize:     [30, 30],
        iconAnchor:   [15, 30],

    }
});
	
	
	var numStations = arrStations["cnt"];
	var justStations = arrStations["stations"];
	var yellowIcon = new LeafIcon({iconUrl: 'markerYellow.png'}),
		redIcon = new LeafIcon({iconUrl: 'markerRed.png'}),
		greenIcon = new LeafIcon({iconUrl: 'markerGreen.png'});
		

	for (i=0; i<numStations; i++) {
		
		var measuredValue = arrStations["stations"][i]["measured"];
		var seenVal = measuredValue;
		var icon = greenIcon;
		
		if ( measuredValue < 0) {				// -1, station was not measuring
			icon = yellowIcon;
			seenVal = 'N/A';
		}
		
		if ( measuredValue == null) {			// station is out of order
			icon = redIcon;
			seenVal = 'N/A'; 
		}
		
		var html = '<p><b>' + justStations[i]["name"]+ '</b>' +
			'<br>location:'+justStations[i]["y"]+','+justStations[i]["x"]+
			'<br>station type: '+ justStations[i]["type"]+
			'<br>location type:'+justStations[i]["loctype"]+
			'<br>measured:'+seenVal+'</p>';
			
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
	
	layerTmp = L.leafletGeotiff(tiff=tiff, options=options);
	if(layer != null) mymap.removeLayer(layer);
	mymap.addLayer(layerTmp);
	layer = layerTmp;
	
	/*if (layerTmp.getElement() && layerTmp.getElement().complete) {
		console.log('ano');
		if(layer != null) mymap.removeLayer(layer);
		layer = layerTmp;
	} 
	else {
		console.log('else');
		layerTmp.once('load', function() {
			sleep(1000);
			console.log('ano2');
			if(layer != null) mymap.removeLayer(layer);
			layer = layerTmp;
		});
	}*/
}

function reloadTiff(hour , colorScale) {
    console.log("reloadTiff")
	/*url = 'raster' + hour + '.tiff';
	console.log(url);
	loadTiff(url, colorScale);*/
}