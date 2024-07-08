document.addEventListener('DOMContentLoaded', (event) => {
    // const apiKey = 'AIzaSyClithh9PS0DjOql1fbCszrEfPQcYtl0gU';  // Google Maps API 키를 여기에 직접 삽입
    const mapScript = document.createElement('script');
    mapScript.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`;
    mapScript.async = true;
    document.head.appendChild(mapScript);
});

let map;
let isFloodVisible = false;
let infoWindow;
let geojsonData;
let floodFeatures = [];
let shelterMarkers = {
    '광주 전체': [],
    '동구': [],
    '서구': [],
    '남구': [],
    '북구': [],
    '광산구': []
};

let regionStates = {
    '광주 전체': false,
    '동구': false,
    '서구': false,
    '남구': false,
    '북구': false,
    '광산구': false
};

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: { lat: 35.1595, lng: 126.8526 },
        styles: [
            {
                featureType: "poi",
                elementType: "labels",
                stylers: [{ visibility: "off" }]
            }
        ]
    });

    infoWindow = new google.maps.InfoWindow();

    fetch('/map/data/')
        .then(response => response.json())
        .then(data => {
            geojsonData = data;
            console.log("GeoJSON Data:", geojsonData);
            addShelterMarkers(geojsonData.features);

            document.getElementById('toggleButton').addEventListener('click', () => {
                toggleFloodAreas(geojsonData);
            });

            document.getElementById('shelterButton').addEventListener('click', () => {
                const regionSelection = document.getElementById('regionSelection');
                if (regionSelection.style.display === 'none' || regionSelection.style.display === '') {
                    regionSelection.style.display = 'block';
                } else {
                    regionSelection.style.display = 'none';
                }
            });

            document.getElementById('all').addEventListener('click', () => {
                toggleRegionMarkers('광주 전체');
            });
            document.getElementById('donggu').addEventListener('click', () => {
                toggleRegionMarkers('동구');
            });
            document.getElementById('seogu').addEventListener('click', () => {
                toggleRegionMarkers('서구');
            });
            document.getElementById('namgu').addEventListener('click', () => {
                toggleRegionMarkers('남구');
            });
            document.getElementById('bukgu').addEventListener('click', () => {
                toggleRegionMarkers('북구');
            });
            document.getElementById('gwangsangu').addEventListener('click', () => {
                toggleRegionMarkers('광산구');
            });
        });
}

function toggleFloodAreas(geojsonData) {
    if (isFloodVisible) {
        floodFeatures.forEach(feature => map.data.remove(feature));
        floodFeatures = [];
        document.getElementById('toggleButton').textContent = '침수예상 지역';
    } else {
        geojsonData.features.forEach(feature => {
            if (feature.geometry.type === "Polygon") {
                const floodFeature = map.data.addGeoJson(feature);
                floodFeatures.push(floodFeature[0]);
            }
        });
        map.data.setStyle(feature => ({
            fillColor: feature.getProperty('fillColor'),
            fillOpacity: feature.getProperty('fillOpacity'),
            strokeColor: feature.getProperty('strokeColor'),
            strokeOpacity: feature.getProperty('strokeOpacity'),
            strokeWeight: feature.getProperty('strokeWeight')
        }));
        document.getElementById('toggleButton').textContent = '침수예상 지역 숨기기';
    }
    isFloodVisible = !isFloodVisible;
}

function addShelterMarkers(features) {
    features.forEach(feature => {
        if (feature.geometry.type === "Point") {
            const marker = new google.maps.Marker({
                position: {
                    lat: feature.geometry.coordinates[1],
                    lng: feature.geometry.coordinates[0]
                },
                map: null,
                title: feature.properties.title
            });

            marker.addListener('click', () => {
                const contentString = `
                    <div>
                        <h2>${feature.properties.title}</h2>
                        <p><strong>주소:</strong> ${feature.properties.address}</p>
                        <p><strong>최대 수용 인원:</strong> ${feature.properties.capacity}</p>
                    </div>`;
                infoWindow.setContent(contentString);
                infoWindow.open(map, marker);
            });

            shelterMarkers['광주 전체'].push(marker);
            if (feature.properties.region) {
                shelterMarkers[feature.properties.region].push(marker);
            }
        }
    });
}

function toggleRegionMarkers(region) {
    if (regionStates[region]) {
        shelterMarkers[region].forEach(marker => marker.setMap(null));
        regionStates[region] = false;
    } else {
        shelterMarkers[region].forEach(marker => marker.setMap(map));
        regionStates[region] = true;
    }
}
