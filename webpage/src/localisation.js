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

        var testing_latlngs = [
            // [4.2301, 50.4849] // testing if coordinates are inversed or not
            [50.8136, 4.3836], // 144
            [50.8133, 4.3830], // 98
            [50.8130555556, 4.3825], // 58
            [50.8130555556, 4.3819], // 57
            [50.8128, 4.3817], // 56
            [50.8128, 4.3808], // 75
            [50.8131, 4.3808], // 54
            [50.8133, 4.3808], // 52 
            [50.8133, 4.3806]  // 51
        ];

        var polyline = L.polyline(testing_latlngs, {color: 'red'}).addTo(map);
        alert("Should have added the polyline to the map.")
        console.log(map);


        // // USER POSITION
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


// Code function that suppose we receive a vector of coordinates and trace a path for it.
/**
 * Create a vector of coordinates
 * Iterate over the vector and trace lines between the points
 * enjoy
 */