var geoip = [];
var points = [];

jQuery.ajax({
    url: "localhost:5000/",
    type: "GET",

    contentType: 'application/json; charset=utf-8',
    success: function(resultData) {
        geoip = resultData;
    },
    error: function(jqXHR, textStatus, errorThrown) {},

    timeout: 120000,
});

var mymap = L.map('map');

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(mymap);

source = geoip[0]
if (source != null) {
  mymap.setView([source.latitude, source.longitude], 5);
} else {
  mymap.setView([15.0, 0.0], 3);
}

for (i = 0; i < geoip.length; i++) {
    current_geoip = geoip[i];
    domain = current_geoip.domain;
    lat = current_geoip.latitude;
    long = current_geoip.longitude;
    var point = L.marker([lat, long]).addTo(mymap)
        .bindPopup(domain);
    points.push(point);
}

var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap);
}

mymap.on('click', onMapClick);
