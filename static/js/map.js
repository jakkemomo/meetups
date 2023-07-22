ymaps.ready(init);

function init() {
    var map;
    var objectManager = new ymaps.ObjectManager();

    ymaps.geolocation.get().then(function (res) {
        createMap({
            center: [53.90228, 27.561831],
            zoom: 12
        });
        res.geoObjects.options.set('preset', 'islands#blueCircleIcon');
        map.geoObjects.add(res.geoObjects);
    }, function (e) {
        // Если местоположение невозможно получить, то просто создаем карту.
        createMap({
            center: [53.90228, 27.561831],
            zoom: 2
        });
    });

    function createMap(state) {
        map = new ymaps.Map('map', state);
        map.geoObjects.add(objectManager);
        let data = JSON.parse(document.getElementById('events-data').textContent)
        console.log(data);
        objectManager.add(data);
    }

}
