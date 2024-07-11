from django.shortcuts import render
from django.http import JsonResponse
import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta
from django.core.cache import cache
import time

# 공공데이터포털에서 발급받은 인증키 (Encoding된 키 사용)
service_key = 'U5TMb2vWz5yYMTnePaPkAUBMk71makHiU1I1SjOcPC6MDSTQpVCygUlka/H5lFS97zg8esXtV6qKoUEPpox3EA=='

async def fetch_rainfall_data(request):
    # 캐시에서 데이터 가져오기
    cached_data = cache.get('rainfall_data')
    if cached_data:
        return JsonResponse(cached_data, safe=False)
    
    # API 엔드포인트
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    
    base_date = datetime.now() - timedelta(days=1)
    base_date = base_date.strftime('%Y%m%d') # 어제 23시 기준으로 3일치 강수량 데이터 호출

    # Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
    # 요청 파라미터 공통 부분
    common_params = {
        'serviceKey': service_key, 
        'pageNo': '1', 
        'numOfRows': '1000', 
        'dataType': 'XML', 
        'base_date': base_date, 
        'base_time': '2300'
    }

    # 각 지역별 (nx, ny) 좌표
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
                        
                        if category == 'PCP':
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
    
    start_time = time.time()  # 시작 시간 기록
    
    # 모든 요청을 비동기로 실행
    tasks = [fetch_location_data(location_name, nx, ny) for location_name, (nx, ny) in locations.items()]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        all_data.extend(result)

    end_time = time.time()  # 종료 시간 기록
    print(f"비동기 방식 로딩 시간: {end_time - start_time}초")  # 로딩 시간 출력

    # 데이터프레임으로 변환
    df = pd.DataFrame(all_data)

    # 'fcst_value' 컬럼의 값 수정
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
    
    # 현재 시간과 일치하는 데이터
    current_time = datetime.now().strftime('%H00')
    current_data = {}
    for location in locations.keys():
        current_data[location] = filtered_data[(filtered_data['location'] == location) & (filtered_data['fcst_time'] == current_time)].to_dict(orient='records')
    
    # 캐시에 데이터 저장 (예: 10분 동안 캐시)    
    cache.set('rainfall_data', {'all_data': filtered_data.to_dict(orient='records'), 'current_data': current_data}, timeout=600)
    
    # JSON 응답으로 데이터 반환
    return JsonResponse({
        'all_data': filtered_data.to_dict(orient='records'),
        'current_data': current_data
    }, safe=False)

def rain_view(request):
    return render(request, 'rain/rain.html')

# Django view에서 비동기 함수를 실행할 수 있게 수정
def fetch_rainfall_data_view(request):
    return asyncio.run(fetch_rainfall_data(request))
