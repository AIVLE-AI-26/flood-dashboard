from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime

# 관측소 코드와 이름, 위도 및 경도 매핑
observatories = {
    '5001630': {'name': '담양군(광주댐)', 'lat': 35.1893218064162, 'lng': 126.98387745098},
    '5001640': {'name': '광주광역시(용산교)', 'lat': 35.2405799574413, 'lng': 126.888496612547},
    '5001645': {'name': '광주광역시(첨단대교)', 'lat': 35.2175, 'lng': 126.856944},
    '5001650': {'name': '광주광역시(유촌교)', 'lat': 35.167116, 'lng': 126.856710},
    '5001655': {'name': '광주광역시(풍영정천2교)', 'lat': 35.171876, 'lng': 126.813981},
    '5001660': {'name': '광주광역시(어등대교)', 'lat': 35.16, 'lng': 126.82305555555556},
    '5001676': {'name': '광주광역시(신운교)', 'lat': 35.16861111111111, 'lng': 126.89083333333333},
    '5001669': {'name': '광주광역시(우제교)', 'lat': 35.13138888888889, 'lng': 126.94250000000001},  # 여기가 어디?
    '5001670': {'name': '광주광역시(설월교)', 'lat': 35.129444444444445, 'lng': 126.92750000000001},
    '5001682': {'name': '광주광역시(벽진동)', 'lat': 35.13, 'lng': 126.845},  # 금호동
    '5002690': {'name': '광주광역시(장록교)', 'lat': 35.134166666666665, 'lng': 126.785},  
    '5002677': {'name': '광주광역시(평림교)', 'lat': 35.165277777777774, 'lng': 126.69},
    '5001673': {'name': '광주광역시(천교)', 'lat': 35.151111111111106, 'lng': 126.90722222222223},
    '5002660': {'name': '광주광역시(용진교)', 'lat': 35.21527777777778, 'lng': 126.74666666666667},
    '5004620': {'name': '광주광역시(승용교)', 'lat': 35.071111111111115, 'lng': 126.77222222222223},
    '5001680': {'name': '광주광역시(극락교)', 'lat': 35.13583333333333, 'lng': 126.82583333333334},
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