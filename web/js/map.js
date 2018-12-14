document.addEventListener('DOMContentLoaded', function() {
    createMap();
	loadTiff('raster0.tiff')
}, false);

var mymap = null;
var layer = null;

function createMap() {
	mymap = L.map('mapid').setView([49.372288, 17.101004], 7);
	 
	 var mainLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: 'pk.eyJ1IjoidmlkbyIsImEiOiJjam9kMnhrY2swdHU4M3FuMnRtMmZtZXkzIn0.0eihDz33xkCGLhdWOvDi3Q'
	}).addTo(mymap);
}


function loadTiff(url, colorScale) {
	
	
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
	
	layerTmp = L.leafletGeotiff(url=url, options=options).addTo(mymap);
	if(layer != null) mymap.removeLayer(layer);
	layer = layerTmp;
}

function reloadTiff(hour , colorScale) {
    console.log("reloadTiff")
//	selection = document.getElementById('selectHour');
//	hour = selection.options[selection.selectedIndex].text;
	url = 'raster' + hour + '.tiff';
	console.log(url);
	loadTiff(url, colorScale);
}
