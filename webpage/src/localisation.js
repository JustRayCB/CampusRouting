if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        let userLat = position.coords.latitude;
        let userLng = position.coords.longitude;
        var map = L.map('map', {
            dragging: true
        }).setView([50.8133, 4.3804], 17);
        map.setMaxBounds(map.getBounds());
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            minZoom: 17,
        }).addTo(map);
         // Retrieve the path from the session storage
        const path = JSON.parse(sessionStorage.getItem('path'));

        // Create the polyline using the path
        var greenIcon = new L.Icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });
        const redIcon = new L.Icon({
          iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });
        var antPath = L.polyline.antPath(path, {
            "delay": 1000,
            "dashArray": [10, 20],
            "weight": 5,
            "color": "#F000FF",
            "pulseColor": "#FFFFFF"
        }).addTo(map);
        var marker = L.marker(path[0], {icon:greenIcon}).addTo(map);
        var marker2 = L.marker(path[path.length - 1], {icon:redIcon}).addTo(map);


        // // USER POSITION
        // // Checks if the user is within the bounds of the campus // Call this part of the code peroiodically (?)
        // if (campusBounds.contains([userLat, userLng])) {
        //     var marker = L.marker([userLat, userLng]).addTo(map);
        //     marker.bindPopup("<b>You</b>").openPopup();

        //     // PATH CREATION
        //     // create a red polyline from an array of LatLng points // Here we would have the points of the python script
        //     // var latlngs = [
        //     //     [userLat, userLong],
        //     //     [50.8125, 4.3785],
        //     //     [50.8145, 4.3823]
        //     // ];
        //     var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
        // } else {
        //     alert("You are not on campus");
        // }
    });
} else {
    alert("Geolocation is not supported by this browser.");
}
