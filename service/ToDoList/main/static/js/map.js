document.addEventListener('DOMContentLoaded', (event) => {
    // const apiKey = 'AIzaSyD2WVmbg5rwpXUBfhH3CYLWQv8STSAKAW0';  // Google Maps API 키를 여기에 직접 삽입
    const mapScript = document.createElement('script');
    mapScript.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`;
    mapScript.async = true;
    document.head.appendChild(mapScript);

    const markerClustererScript = document.createElement('script');
    markerClustererScript.src = 'https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js';
    markerClustererScript.async = true;
    document.head.appendChild(markerClustererScript);
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

let markerCluster;

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

            // 클러스터 스타일 설정
            const clusterStyles = [
                {
                    textColor: 'white',
                    url: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m1.png',
                    height: 46,
                    width: 46
                },
                {
                    textColor: 'white',
                    url: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m2.png',
                    height: 50,
                    width: 50
                },
                {
                    textColor: 'white',
                    url: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m3.png',
                    height: 56,
                    width: 56
                }
            ];

            // MarkerClusterer 초기화
            markerCluster = new markerClusterer.MarkerClusterer({
                map: map,
                markers: [],
                gridSize: 80, // 기본 클러스터링 범위
                styles: clusterStyles,
                renderer: {
                    render: ({ count, position }) => {
                        const index = count < 10 ? 0 : count < 100 ? 1 : 2;
                        const style = clusterStyles[index];

                        return new google.maps.Marker({
                            position,
                            icon: {
                                url: style.url,
                                size: new google.maps.Size(style.width, style.height),
                                anchor: new google.maps.Point(style.width / 2, style.height / 2)
                            },
                            label: {
                                text: String(count),
                                color: style.textColor,
                                fontSize: '16px',
                                fontWeight: 'bold'
                            }
                        });
                    }
                }
            });

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
                toggleRegionMarkers('광주 전체', 'all');
            });
            document.getElementById('donggu').addEventListener('click', () => {
                toggleRegionMarkers('동구', 'donggu');
            });
            document.getElementById('seogu').addEventListener('click', () => {
                toggleRegionMarkers('서구', 'seogu');
            });
            document.getElementById('namgu').addEventListener('click', () => {
                toggleRegionMarkers('남구', 'namgu');
            });
            document.getElementById('bukgu').addEventListener('click', () => {
                toggleRegionMarkers('북구', 'bukgu');
            });
            document.getElementById('gwangsangu').addEventListener('click', () => {
                toggleRegionMarkers('광산구', 'gwangsangu');
            });

            // 줌 레벨 변경 시 이벤트 리스너 추가
            map.addListener('zoom_changed', () => {
                updateMarkersByZoom();
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

    // 클러스터러에 마커 추가
    if (markerCluster) {
        markerCluster.addMarkers(shelterMarkers['광주 전체']);
    }
}

function toggleRegionMarkers(region, buttonId) {
    const button = document.getElementById(buttonId);

    if (region === '광주 전체') {
        if (regionStates[region]) {
            // "광주 전체"가 이미 활성화된 경우 모든 마커 숨기기
            if (markerCluster) markerCluster.clearMarkers();
            Object.keys(regionStates).forEach(r => {
                regionStates[r] = false;
                const btn = document.getElementById(getButtonId(r));
                if (btn) {
                    btn.classList.remove('active');
                }
            });
        } else {
            // "광주 전체"가 비활성화된 경우 모든 마커 보이기
            if (markerCluster) markerCluster.addMarkers(shelterMarkers['광주 전체']);
            Object.keys(regionStates).forEach(r => {
                regionStates[r] = true;
                const btn = document.getElementById(getButtonId(r));
                if (btn) {
                    btn.classList.add('active');
                }
            });
        }
    } else {
        // 다른 구역 버튼을 눌렀을 때 "광주 전체"를 비활성화
        if (regionStates['광주 전체']) {
            if (markerCluster) markerCluster.clearMarkers();
            regionStates['광주 전체'] = false;
            const allButton = document.getElementById('all');
            if (allButton) {
                allButton.classList.remove('active');
            }
        }

        if (regionStates[region]) {
            if (markerCluster) markerCluster.removeMarkers(shelterMarkers[region]);
            regionStates[region] = false;
            button.classList.remove('active');
        } else {
            if (markerCluster) markerCluster.addMarkers(shelterMarkers[region]);
            regionStates[region] = true;
            button.classList.add('active');
        }
    }

    // 줌 레벨에 따른 마커 표시 업데이트
    updateMarkersByZoom();
}

function updateMarkersByZoom() {
    const zoomLevel = map.getZoom();
    const markerVisibility = (marker, visibility) => marker.setMap(visibility ? map : null);

    Object.keys(regionStates).forEach(region => {
        shelterMarkers[region].forEach(marker => {
            if (regionStates[region]) {
                if (zoomLevel >= 14 || region === '광주 전체') {
                    markerVisibility(marker, true);
                } else {
                    markerVisibility(marker, false);
                }
            } else {
                markerVisibility(marker, false);
            }
        });
    });
}

function getButtonId(region) {
    switch(region) {
        case '동구': return 'donggu';
        case '서구': return 'seogu';
        case '남구': return 'namgu';
        case '북구': return 'bukgu';
        case '광산구': return 'gwangsangu';
        case '광주 전체': return 'all';
        default: return '';
    }
}