document.addEventListener('DOMContentLoaded', function() {
    var mapContainer = document.getElementById('map');
    var infoContainer = document.getElementById('waterlevel-info');

    // 관측소의 위치와 수위를 표시할 데이터 (중앙으로 모이도록 설정)
    var observatories = [
        { name: '담양군(광주댐)', x: 711, y: 278, wl: '0.00' },
        { name: '광주광역시(용산교)', x: 512, y: 171, wl: '0.00' },
        { name: '광주광역시(첨단대교)', x: 447, y: 219, wl: '0.00' },
        { name: '광주광역시(유촌교)', x: 447, y: 324, wl: '0.00' },
        { name: '광주광역시(풍영정천2교)', x: 357, y: 314, wl: '0.00' },
        { name: '광주광역시(어등대교)', x: 376, y: 338, wl: '0.00' },
        { name: '광주광역시(신운교)', x: 517, y: 320, wl: '0.00' },
        { name: '광주광역시(우제교)', x: 625, y: 399, wl: '0.00' },
        { name: '광주광역시(설월교)', x: 593, y: 402, wl: '0.00' },
        { name: '광주광역시(벽진동)', x: 422, y: 401, wl: '0.00' },
        { name: '광주광역시(장록교)', x: 298, y: 392, wl: '0.00' },
        { name: '광주광역시(평림교)', x: 100, y: 327, wl: '0.00' },
        { name: '광주광역시(천교)', x: 551, y: 358, wl: '0.00' },
        { name: '광주광역시(용진교)', x: 218, y: 224, wl: '0.00' },
        { name: '광주광역시(승용교)', x: 271, y: 523, wl: '0.00' },
        { name: '광주광역시(극락교)', x: 382, y: 389, wl: '0.00' },
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
