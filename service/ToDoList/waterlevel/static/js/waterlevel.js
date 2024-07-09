document.addEventListener('DOMContentLoaded', function() {
    var mapContainer = document.getElementById('map');
    var infoContainer = document.getElementById('waterlevel-info');

    // 관측소의 위치와 수위를 표시할 데이터 (중앙으로 모이도록 설정)
    var observatories = [
        { name: '담양군(담양댐)', x: 500, y: 300, wl: '0.00' },
        { name: '담양군(금월교)', x: 520, y: 320, wl: '0.11' },
        { name: '담양군(중방4교)', x: 480, y: 340, wl: '0.09' },
        { name: '담양군(장천교)', x: 500, y: 360, wl: '0.24' },
        { name: '담양군(덕용교)', x: 520, y: 380, wl: '0.06' },
        { name: '담양군(삼지교)', x: 500, y: 400, wl: '0.30' },
        { name: '담양군(양지교)', x: 520, y: 420, wl: '0.30' },
        { name: '담양군(광주댐)', x: 500, y: 440, wl: '0.00' },
        { name: '광주광역시(용산교)', x: 520, y: 460, wl: '0.11' },
        { name: '광주광역시(첨단대교)', x: 500, y: 480, wl: '0.47' },
    ];

    // 전체 수위 데이터를 오른쪽 패널에 표시
    observatories.forEach(function(obs) {
        var listItem = document.createElement('div');
        listItem.className = 'info-item';
        listItem.setAttribute('data-name', obs.name);
        listItem.innerHTML = `<b>${obs.name}</b><br>현재 수위: ${obs.wl}m`;
        infoContainer.appendChild(listItem);
    });

    // 지도에 마커 표시
    observatories.forEach(function(obs) {
        var marker = document.createElement('div');
        marker.className = 'map-marker';
        marker.style.left = obs.x + 'px';
        marker.style.top = obs.y + 'px';
        marker.setAttribute('data-name', obs.name);
        marker.setAttribute('data-wl', obs.wl);
        mapContainer.appendChild(marker);

        marker.addEventListener('click', function() {
            // 오른쪽 패널에서 해당 관측소 정보 강조
            var items = document.querySelectorAll('.info-item');
            items.forEach(function(item) {
                item.classList.remove('highlight');
                if (item.getAttribute('data-name') === obs.name) {
                    item.classList.add('highlight');
                }
            });
            // 알림 창으로도 정보 표시
            alert(`${obs.name}\n현재 수위: ${obs.wl}m`);
        });
    });

    // 수위 데이터를 갱신하는 함수
    function fetchWaterLevelData() {
        $.ajax({
            url: "/waterlevel/data/",
            method: "GET",
            success: function(data) {
                data.forEach(function(station) {
                    var marker = document.querySelector(`.map-marker[data-name="${station.obsnm}"]`);
                    if (marker) {
                        marker.setAttribute('data-wl', station.wl);
                    }
                    var item = document.querySelector(`.info-item[data-name="${station.obsnm}"]`);
                    if (item) {
                        item.innerHTML = `<b>${station.obsnm}</b><br>현재 수위: ${station.wl}m`;
                    }
                });
            }
        });
    }

    // 초기 데이터 로드
    fetchWaterLevelData();
    // 1분마다 데이터 갱신
    setInterval(fetchWaterLevelData, 60000);
});
