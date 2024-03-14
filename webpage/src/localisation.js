import {path} from "./welcome";

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

        const campusBounds = L.latLngBounds([
            [50.8125, 4.3785],
            [50.8145, 4.3823]
        ]);

        var testing_latlngs = [
            [50.81377,4.38416], // 158
            [50.81362,4.38368], // 144
            [50.81347,4.38314], // 98
            [50.81329,4.38260], // 58
            [50.81312,4.38205], // 57
            [50.81302,4.38168], // 56
            [50.81286,4.38140], // 69
            [50.81232,4.38182], // 114
            [50.81234,4.38188] // eU_5
        ];
        var polyline = L.polyline(testing_latlngs, {color: 'red'}).addTo(map);


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