ymaps.ready(init);

function init() {
    var map;
    var objectManager = new ymaps.ObjectManager();

    let center_lat = 53.90228;
    let center_lng = 27.561831;

    let center_lat_element = document.getElementById('center_lat');
    let center_lng_element = document.getElementById('center_lng');

    if (center_lat_element){
        center_lat = JSON.parse(center_lat_element.textContent);
    }
    if (center_lng_element){
        center_lng = JSON.parse(center_lng_element.textContent);
    }

    createMap({
        center: [center_lat, center_lng],
        zoom: 12
    });

    function createMap(state) {
        map = new ymaps.Map('map', state);
        map.geoObjects.add(objectManager);
        let data = JSON.parse(document.getElementById('events-data').textContent)
        console.log(data);
        objectManager.add(data);
    }

}
