document.addEventListener('DOMContentLoaded', function() {
    var infoContainer = document.getElementById('waterlevel-info');
    var dataContainer = document.getElementById('data-container');
    var intervalId = false;
    var isWaterLevelInfo = false;
    var wlmarkers = {};
    var markers = [];
    var observatories = [
        // {name: '담양군(광주댐)', 'lat': 35.1893218064162, 'lng': 126.98387745098, wl: '0.00' ,fl : '0', '홍수주의보' : 7.5,'홍수경보':8.5},
        {'name': '광주광역시(용산교)', 'lat': 35.2405799574413, 'lng': 126.888496612547, 'wl': '0.00' ,fl : '0', '홍수주의보' : 3.4,'홍수경보':3.9},
        {'name': '광주광역시(첨단대교)', 'lat': 35.2175, 'lng': 126.856944, 'wl': '0.00' ,fl : '0', '홍수주의보' : 2.7,'홍수경보':3.4},
        {'name': '광주광역시(유촌교)', 'lat': 35.167116, 'lng': 126.856710, 'wl': '0.00' ,fl : '0', '홍수주의보' : 4.0,'홍수경보':5.0},
        {'name': '광주광역시(풍영정천2교)', 'lat': 35.171876, 'lng': 126.813981, 'wl': '0.00' ,fl : '0', '홍수주의보' : 4.1,'홍수경보':4.9},
        {'name': '광주광역시(어등대교)', 'lat': 35.16, 'lng': 126.82305555555556, 'wl': '0.00' ,fl : '0', '홍수주의보' : 4.7,'홍수경보':5.9},
        // {name: '광주광역시(신운교)', 'lat': 35.16861111111111, 'lng': 126.89083333333333, wl: '0.00' ,fl : '0', '홍수주의보' : 7.5,'홍수경보':8.5},
        // {name: '광주광역시(우제교)', 'lat': 35.13138888888889, 'lng': 126.94250000000001, wl: '0.00' ,fl : '0', '홍수주의보' : 7.5,'홍수경보':8.5},
        {'name': '광주광역시(설월교)', 'lat': 35.129444444444445, 'lng': 126.92750000000001, 'wl': '0.00' ,fl : '0', '홍수주의보' : 3.3,'홍수경보':3.8},
        // {name: '광주광역시(벽진동)', 'lat': 35.13, 'lng': 126.845, wl: '0.00' ,fl : '0', '홍수주의보' : 7.5,'홍수경보':8.5},
        {'name': '광주광역시(장록교)', 'lat': 35.134166666666665, 'lng': 126.785, 'wl': '0.00' ,fl : '0', '홍수주의보' : 5.6,'홍수경보':6.1},  
        {'name': '광주광역시(평림교)', 'lat': 35.165277777777774, 'lng': 126.69, 'wl': '0.00' ,fl : '0', '홍수주의보' : 4.3,'홍수경보':5.1},
        {'name': '광주광역시(천교)', 'lat': 35.151111111111106, 'lng': 126.90722222222223, 'wl': '0.00' ,fl : '0', '홍수주의보' : 2.9,'홍수경보':3.4},
        {'name': '광주광역시(용진교)', 'lat': 35.21527777777778, 'lng': 126.74666666666667, 'wl': '0.00' ,fl : '0', '홍수주의보' : 4.3,'홍수경보':5.3},
        {'name': '광주광역시(승용교)', 'lat': 35.071111111111115, 'lng': 126.77222222222223, 'wl': '0.00' ,fl : '0', '홍수주의보' : 5.6,'홍수경보': 6.9},
        {'name': '광주광역시(극락교)', 'lat': 35.13583333333333, 'lng': 126.82583333333334, 'wl': '0.00' ,fl : '0', '홍수주의보' : 7.5,'홍수경보':8.5},
    ];

    function getDataFromUrl() {
        var urlParams = new URLSearchParams(window.location.search);
        var data = urlParams.get('button');
        return data;
    }

    window.onload = function() {
        var data = getDataFromUrl();
        if (data == "wl-button") {
            waterlevelButton.click();
        } 
    };

    document.getElementById('waterlevelButton').addEventListener('click', function(event) {
        dataContainer.classList.toggle('visible');
        toggleWaterLevelInfo();
    });

    document.querySelector('.waterlevelbar-close').addEventListener('click', function(event) {
        console.log('closebar')
        document.getElementById('waterlevelButton').click();
    });

    // toggleWaterLevelInfo에 맞춰 수정하기
    function toggleWaterLevelInfo() {
        if (isWaterLevelInfo) {
            // 마커 지우기, 갱신 중단
            clearMarkers();
            clearInterval(intervalId); // interval 정지
            isWaterLevelInfo = false;
            console.log('isWaterLevelInfo after:', isWaterLevelInfo);
            return;
        } 
        else {
            addWaterLevelMarkers();
            
            // 전체 수위 데이터를 오른쪽 패널에 표시
            observatories.forEach(function(obs) {
                var listItem = document.createElement('div');
                listItem.className = 'info-item';
                listItem.setAttribute('data-name', obs.name);
                listItem.innerHTML = `<b>${obs.name}</b><br>현재 수위: ${obs.wl}m<br>홍수확률: ${obs.fl}%
                <br>주의: 0.0m    경보: 0.0m<br>`; // 기존 코드에 홍수확률(fl) 추가
                infoContainer.appendChild(listItem);
            });
        }
        fetchWaterLevelData();

        intervalId = setInterval(fetchWaterLevelData, 100000);
        isWaterLevelInfo = true;
    }

    // 지도에 마커 표시
    function addWaterLevelMarkers() {
        observatories.forEach(function(obs) {
            var marker = new google.maps.Marker({
                position: { lat: obs.lat, lng: obs.lng },
                map: map,
                title: obs.name,
                customInfo: {
                    name: obs.name,
                    wl: obs.wl
                }
            });

            markers.push(marker); // 마커를 배열에 추가
            wlmarkers[obs.name] =  marker;

            marker.addListener('click', function() {
                const waterlevelcontent = 
                    `<div style="color: black;">
                        <h2 style="margin: 0;">${obs.name}</h2>
                        <p><strong>현재 수위:</strong> ${marker.customInfo.wl}m</p>
                    </div>`;
                infoWindow.setContent(waterlevelcontent);
                infoWindow.open(map, marker);

                var items = document.querySelectorAll('.info-item');
                items.forEach(function(item) {
                    item.classList.remove('highlight');
                    if (item.getAttribute('data-name') === obs.name) {
                        item.classList.add('highlight');
                        // 해당 개체로 스크롤
                        item.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                });
            });
        });
    }

    function clearMarkers() {
        markers.forEach(function(marker) {
            marker.setMap(null); // 각 마커의 지도 맵을 null로 설정하여 제거
        });
        markers = []; // 배열 비우기
    }

    function fetchWaterLevelData() {
        $.ajax({
            url: "/waterlevel/data/",
            method: "GET",
            success: function(data) {
                data.forEach(function(station) {
                    var wl = station.wl.toString();
                    if (wl.startsWith('.')) {
                        wl = '0' + wl;
                    }
                    
                    var marker = wlmarkers[station.obsnm];
                    if (marker) {
                        marker.customInfo.wl = wl;
                    }

                    var item = document.querySelector(`.info-item[data-name="${station.obsnm}"]`);
                    if (item) {
                        item.innerHTML = `<b>${station.obsnm}</b><br>현재 수위: ${wl}m<br>홍수확률: ${station.홍수확률}%
                        <br>주의: ${station.홍수주의보}m    경보: ${station.홍수경보}m<br>`;
                    }
                });
                // alert("데이터 갱신");  // 데이터 갱신 확인용
            },
            error: function() {
                alert("데이터를 불러오는데 실패했습니다.");
            }
        });
    }
});
