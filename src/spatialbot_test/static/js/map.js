let map =  L.map('map', {
    center: [23.7965, 90.4290],
    zoom: 12,
    // Hide text leaflet at bottom left
    attributionControl: false,
    zoomControl: false
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);



// Add sidebar to map
var sidebar = L.control.sidebar('sidebar').addTo(map);



