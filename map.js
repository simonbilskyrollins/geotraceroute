var mymap = L.map('map').setView([15.0, 0.0], 3);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery &copy; <a href="http://mapbox.com">Mapbox</a>' + '<br/>' +
    'This product includes GeoLite2 data created by MaxMind, available from ' +
    '<a href="http://www.maxmind.com">http://www.maxmind.com</a>.',
  id: 'mapbox.streets'
}).addTo(mymap);

var geoip = [];
var routes = [];

jQuery.ajax({
  url: "http://localhost:5000/traceroute",
  type: "GET",
  contentType: 'application/json; charset=utf-8',
  success: function(resultData) {
    addPoints(resultData);
  },
  error: function(jqXHR, textStatus, errorThrown) {
    console.log(errorThrown);
  },
  timeout: 120000,
});

function addPoints(geoip) {
  source = geoip[0];
  if (source != null) {
    mymap.setView([source.latitude, source.longitude], 4);
  }

  var route = new L.layerGroup();
  var latLngs = [];
  for (i = 0; i < geoip.length; i++) {
    current_geoip = geoip[i];
    hop = current_geoip.hop;
    domain = current_geoip.domain;
    latLng = L.latLng(current_geoip.latitude, current_geoip.longitude);
    point = L.marker(latLng).addTo(route)
      .bindPopup(domain);
    latLngs.push(latLng);
  }
  L.polyline(latLngs).addTo(route);
  route.addTo(mymap);
  routes.push(route);
}

var popup = L.popup();

function onMapClick(e) {
  popup
    .openOn(mymap);
}

mymap.on('click', onMapClick);
