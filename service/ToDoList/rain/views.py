from django.shortcuts import render
from django.http import JsonResponse
import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta
from django.core.cache import cache
import time

service_key = 'nz2fwU3ROAjPxqq2gPGhnUPe6+ZWmxvhXIyUBW/qUrPl0T0za05as1fDc4AiuY/6R2jfQE0JQBr4MKDZ7MPC6w=='

async def fetch_rainfall_data(request):
    cached_data = cache.get('rainfall_data')
    if cached_data:
        return JsonResponse(cached_data, safe=False)
    
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    
    # 현재 시간 기준으로 6시간 전의 시간 계산
    now = datetime.now() - timedelta(hours=5)
    base_date = now.strftime('%Y%m%d')
    base_time = now.strftime('%H00')  # 'HHMM' 형식으로 시간 설정, 분은 00으로 설정

    common_params = {
        'serviceKey': service_key, 
        'pageNo': '1', 
        'numOfRows': '1000', 
        'dataType': 'XML', 
        'base_date': base_date, 
        'base_time': base_time
    }

    locations = {
        '광주광역시': (58, 74),
        '동구': (60, 74),
        '서구': (59, 74),
        '남구': (59, 73),
        '북구': (59, 75),
        '광산구': (57, 74)
    }

    async def fetch_location_data(location_name, nx, ny):
        params = common_params.copy()
        params['nx'] = nx
        params['ny'] = ny
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    print(f"API 요청 성공: {location_name}")
                    root = ET.fromstring(await response.text())
                    location_data = []
                    
                    for item in root.findall('.//item'):
                        category = item.find('category').text if item.find('category') is not None else ''
                        
                        if category == 'RN1':
                            base_date = item.find('baseDate').text if item.find('baseDate') is not None else ''
                            fcst_date = item.find('fcstDate').text if item.find('fcstDate') is not None else ''
                            fcst_time = item.find('fcstTime').text if item.find('fcstTime') is not None else ''
                            fcst_value = item.find('fcstValue').text if item.find('fcstValue') is not None else ''
                            
                            location_data.append({
                                'location': location_name,
                                'base_date': base_date,
                                'fcst_date': fcst_date,
                                'fcst_time': fcst_time,
                                'fcst_value': fcst_value
                            })
                    return location_data
                else:
                    print(f"Error: {response.status}, location: {location_name}")
                    return []

    all_data = []
    
    start_time = time.time()
    
    tasks = [fetch_location_data(location_name, nx, ny) for location_name, (nx, ny) in locations.items()]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        all_data.extend(result)

    end_time = time.time()
    print(f"비동기 방식 로딩 시간: {end_time - start_time}초")

    df = pd.DataFrame(all_data)

    def clean_fcst_value(value):
        if value == '강수없음':
            return 0.0
        if value == '1mm 미만':
            return 1.0
        if value == '30.0~50.0mm':
            return 30.0
        if value == '50.0mm 이상':
            return 50.0
        if 'mm' in value:
            return float(value.replace('mm', ''))
        return value
    df['fcst_value'] = df['fcst_value'].apply(clean_fcst_value)
    
    today = datetime.now().strftime('%Y%m%d')
    filtered_data = df[df['fcst_date'] == today]
    
    current_time = datetime.now().strftime('%H00')
    current_data = {}
    for location in locations.keys():
        current_data[location] = filtered_data[(filtered_data['location'] == location) & (filtered_data['fcst_time'] == current_time)].to_dict(orient='records')
    
    cache.set('rainfall_data', {'all_data': filtered_data.to_dict(orient='records'), 'current_data': current_data}, timeout=600)
    
    return JsonResponse({
        'all_data': filtered_data.to_dict(orient='records'),
        'current_data': current_data
    }, safe=False)

def rain_view(request):
    return render(request, 'rain/rain.html')

def fetch_rainfall_data_view(request):
    return asyncio.run(fetch_rainfall_data(request))
