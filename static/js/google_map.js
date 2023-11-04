let map;

async function initMap() {
    const {Map, InfoWindow} = await google.maps.importLibrary("maps");
    const {AdvancedMarkerElement, PinElement} = await google.maps.importLibrary(
        "marker"
    );

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

    map = new Map(document.getElementById("map"), {
        center: {lat: center_lat, lng: center_lng},
        zoom: 12,
        mapId: "eca99e8abfe1a0d8",
        styles: stylesArray
    });

    let data = JSON.parse(document.getElementById('events-data').textContent)
    let features = data['features']

    const infoWindow = new InfoWindow();

    for (let i = 0; i < features.length; i++) {
        // A marker using a Font Awesome icon for the glyph.
        let icon = document.createElement("div");
        icon.innerHTML = '<i class="fa fa-pizza-slice fa-lg"></i>';
        let faPin = new PinElement({
            scale: 1.3,
            glyph: icon,
            glyphColor: "#ff8300",
            background: "#FFD514",
            borderColor: "#ff8300",
        });
        let pos = {lat: features[i]['geometry']['coordinates'][0], lng: features[i]['geometry']['coordinates'][1]};
        let event_pk = features[i]['properties']['pk'];
        let event_name = features[i]['properties']['name'];
        let start_date = features[i]['properties']['start_date'];
        let event_image = features[i]['properties']['image'];
        // Create marker for each event with clickable links
        let marker = new AdvancedMarkerElement({
            position: pos,
            map,
            title: `<a href="/api/v1/events/${event_pk}">${event_name}<a/><br/><span>${start_date}</span><br/><a href="/api/v1/events/${event_pk}"><img className="img-responsive" src="/media/${event_image}" width="250px" height="250px"></a>`,
            content: faPin.element,
        });

        // Add a click listener for each marker, and set up the info window.
        marker.addListener("click", ({domEvent, latLng}) => {
            infoWindow.close();
            infoWindow.setContent(marker.title);
            infoWindow.open(marker.map, marker);
        });

    }
}

let stylesArray = [
    {
        "featureType": "all",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "saturation": 36
            },
            {
                "color": "#000000"
            },
            {
                "lightness": 40
            }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#000000"
            },
            {
                "lightness": 16
            }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 17
            },
            {
                "weight": 1.2
            }
        ]
    },
    {
        "featureType": "administrative.province",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#e3b141"
            }
        ]
    },
    {
        "featureType": "administrative.locality",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#e0a64b"
            }
        ]
    },
    {
        "featureType": "administrative.locality",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#0e0d0a"
            }
        ]
    },
    {
        "featureType": "administrative.neighborhood",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#d1b995"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 21
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#12120f"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "lightness": "-77"
            },
            {
                "gamma": "4.48"
            },
            {
                "saturation": "24"
            },
            {
                "weight": "0.65"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "lightness": 29
            },
            {
                "weight": 0.2
            }
        ]
    },
    {
        "featureType": "road.highway.controlled_access",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#f6b044"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#4f4e49"
            },
            {
                "weight": "0.36"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#c4ac87"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#262307"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#a4875a"
            },
            {
                "lightness": 16
            },
            {
                "weight": "0.16"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#deb483"
            }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 19
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#0f252e"
            },
            {
                "lightness": 17
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#080808"
            },
            {
                "gamma": "3.14"
            },
            {
                "weight": "1.07"
            }
        ]
    }
];

initMap();
