ymaps.ready(init);

function init() {
    var map;
    var objectManager = new ymaps.ObjectManager();

    createMap({
        center: [53.90228, 27.561831],
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
