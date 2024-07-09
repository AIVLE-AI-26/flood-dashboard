from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime

# 관측소 코드와 이름, 위도 및 경도 매핑
observatories = {
    '5001610': {'name': '담양군(담양댐)', 'lat': 35.3850845, 'lng': 127.0134309},
    '5001615': {'name': '담양군(금월교)', 'lat': 35.33291639999999, 'lng': 127.0174978},
    '5001616': {'name': '담양군(중방4교)', 'lat': 35.340398, 'lng': 126.938938},
    '5001618': {'name': '담양군(장천교)', 'lat': 35.3649505556594, 'lng': 126.987491335017},
    '5001620': {'name': '담양군(덕용교)', 'lat': 35.2891998, 'lng': 127.0391635},
    '5001625': {'name': '담양군(삼지교)', 'lat': 35.2706447, 'lng': 126.9386735},
    '5001627': {'name': '담양군(양지교)', 'lat': 35.2552822561945, 'lng': 126.945531914757},
    '5001630': {'name': '담양군(광주댐)', 'lat': 35.1893218064162, 'lng': 126.98387745098},
    '5001640': {'name': '광주광역시(용산교)', 'lat': 35.2405799574413, 'lng': 126.888496612547},
    '5001645': {'name': '광주광역시(첨단대교)', 'lat': 35.2266477, 'lng': 126.8484706},
}

def fetch_water_level_data(obscd):
    url = "http://www.wamis.go.kr:8080/wamis/openapi/wkw/wl_hrdata"
    today = datetime.today().strftime('%Y%m%d')  # 오늘 날짜를 'YYYYMMDD' 형식으로 가져옴
    params = {
        'obscd': obscd,
        'startdt': today,  # 오늘 날짜로 설정
        'enddt': today,    # 오늘 날짜로 설정
        'output': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('list', [])
    else:
        return []

def waterlevel(request):
    return render(request, 'waterlevel/waterlevel.html')

def get_waterlevel_data(request):
    all_data = []
    for code, info in observatories.items():
        data = fetch_water_level_data(code)
        if data:
            latest_data = data[-1]  # 리스트에서 최신 데이터 선택
            latest_data['obsnm'] = info['name']  # 관측소 이름을 데이터에 추가
            latest_data['lat'] = info['lat']  # 관측소의 위도
            latest_data['lng'] = info['lng']  # 관측소의 경도
            all_data.append(latest_data)
    return JsonResponse(all_data, safe=False)