let map;

async function initMap() {
    const {Map} = await google.maps.importLibrary("maps");

    map = new Map(document.getElementById("map"), {
        center: {lat: 53.90228, lng: 27.561831},
        zoom: 12,
    });

    let data = JSON.parse(document.getElementById('events-data').textContent)
    let features = data['features']
    for (let i = 0; i < features.length; i++) {
        let marker = new google.maps.Marker({
            position: new google.maps.LatLng(features[i]['geometry']['coordinates'][0], features[i]['geometry']['coordinates'][1]),
            title: features[i]['properties']['name']
        });

        marker.setMap(map);
    }
}

initMap();
