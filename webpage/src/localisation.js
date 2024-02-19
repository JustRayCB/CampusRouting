if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var userLat = position.coords.latitude;
        var userLng = position.coords.longitude;
        var map = L.map('map', {
            dragging: true
        }).setView([50.8133, 4.3804], 17);
        map.setMaxBounds(map.getBounds());
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            minZoom: 17,
        }).addTo(map);

        var campusBounds = L.latLngBounds([
            [50.8125, 4.3785],
            [50.8145, 4.3823]
        ]);


        // USER POSITION
        if (campusBounds.contains([userLat, userLng])) {
            var marker = L.marker([userLat, userLng]).addTo(map);
            marker.bindPopup("<b>You</b>").openPopup();
            // PATH CREATION 
            // create a red polyline from an array of LatLng points // Here we would have the points of the python script
            var latlngs = [
                [userLat, userLong],
                [50.8125, 4.3785],
                [50.8145, 4.3823]
            ];
            var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
        } else {
            alert("You are not on campus");
        }
    });
} else {
    alert("Geolocation is not supported by this browser.");
}