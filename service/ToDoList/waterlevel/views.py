from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta
import joblib
import json
from django.conf import settings
import os
import numpy as np


# 관측소 코드와 이름, 위도 및 경도 매핑
observatories = {
    # '5001630': {'name': '담양군(광주댐)', 'lat': 35.1893218064162, 'lng': 126.98387745098,'홍수주의보' : 7.5,'홍수경보':8.5},
    '5001640': {'name': '광주광역시(용산교)', 'lat': 35.2405799574413, 'lng': 126.888496612547,'홍수주의보' : 3.4,'홍수경보':3.9},
    '5001645': {'name': '광주광역시(첨단대교)', 'lat': 35.2175, 'lng': 126.856944,'홍수주의보' : 2.7,'홍수경보':3.4},
    '5001650': {'name': '광주광역시(유촌교)', 'lat': 35.167116, 'lng': 126.856710,'홍수주의보' : 4.0,'홍수경보':5.0},
    '5001655': {'name': '광주광역시(풍영정천2교)', 'lat': 35.171876, 'lng': 126.813981,'홍수주의보' : 4.1,'홍수경보':4.9},
    '5001660': {'name': '광주광역시(어등대교)', 'lat': 35.16, 'lng': 126.82305555555556,'홍수주의보' : 4.7,'홍수경보':5.9},
    # '5001676': {'name': '광주광역시(신운교)', 'lat': 35.16861111111111, 'lng': 126.89083333333333,'홍수주의보' : 7.5,'홍수경보':8.5},
    # '5001669': {'name': '광주광역시(우제교)', 'lat': 35.13138888888889, 'lng': 126.94250000000001,'홍수주의보' : 7.5,'홍수경보':8.5},  # 여기가 어디?
    '5001670': {'name': '광주광역시(설월교)', 'lat': 35.129444444444445, 'lng': 126.92750000000001,'홍수주의보' : 3.3,'홍수경보':3.8},
    # '5001682': {'name': '광주광역시(벽진동)', 'lat': 35.13, 'lng': 126.845,'홍수주의보' : 7.5,'홍수경보':8.5},  # 금호동
    '5002690': {'name': '광주광역시(장록교)', 'lat': 35.134166666666665, 'lng': 126.785,'홍수주의보' : 5.6,'홍수경보':6.1},  
    '5002677': {'name': '광주광역시(평림교)', 'lat': 35.165277777777774, 'lng': 126.69,'홍수주의보' : 4.3,'홍수경보':5.1},
    '5001673': {'name': '광주광역시(천교)', 'lat': 35.151111111111106, 'lng': 126.90722222222223,'홍수주의보' : 2.9,'홍수경보':3.4},
    '5002660': {'name': '광주광역시(용진교)', 'lat': 35.21527777777778, 'lng': 126.74666666666667,'홍수주의보' : 4.3,'홍수경보':5.3},
    '5004620': {'name': '광주광역시(승용교)', 'lat': 35.071111111111115, 'lng': 126.77222222222223,'홍수주의보' : 5.6,'홍수경보': 6.9},
    '5001680': {'name': '광주광역시(극락교)', 'lat': 35.13583333333333, 'lng': 126.82583333333334,'홍수주의보' : 7.5,'홍수경보':8.5},
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
            latest_data['obscd'] = code
            latest_data['obsnm'] = info['name']  # 관측소 이름을 데이터에 추가
            latest_data['lat'] = info['lat']  # 관측소의 위도
            latest_data['lng'] = info['lng']  # 관측소의 경도
            latest_data['홍수주의보'] = info['홍수주의보'] 
            latest_data['홍수경보'] = info['홍수경보']
            all_data.append(latest_data)
    service_key = 'nz2fwU3ROAjPxqq2gPGhnUPe6+ZWmxvhXIyUBW/qUrPl0T0za05as1fDc4AiuY/6R2jfQE0JQBr4MKDZ7MPC6w=='

    # API 엔드포인트
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    
    now = datetime.now() - timedelta(hours=5)
    base_date = now.strftime('%Y%m%d')
    base_time = now.strftime('%H00') 
    # Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
    # 요청 파라미터 공통 부분
    common_params = {
        'serviceKey': service_key, 
        'pageNo': '1', 
        'numOfRows': '1000', 
        'dataType': 'XML', 
        'base_date': base_date, 
        'base_time': base_time
    }

    # 각 지역별 (nx, ny) 좌표
    locations = {
        '광주광역시': (58, 74),
        # '동구': (60, 74),
        # '서구': (59, 74),
        # '남구': (59, 73),
        # '북구': (59, 75),
        # '광산구': (57, 74)
    }

    # 데이터를 저장할 리스트 초기화
    all_data1= []

    # 각 지역에 대해 API 요청 보내기
    for location_name, (nx, ny) in locations.items():
        params = common_params.copy()
        params['nx'] = nx
        params['ny'] = ny
        
        # GET 요청 보내기
        response = requests.get(url, params=params)
        
        # 응답 확인
        if response.status_code == 200:
            print(f"API 요청 성공: {location_name}")
            # XML 응답 파싱
            root = ET.fromstring(response.content)
            
            # XML 데이터 파싱
            for item in root.findall('.//item'):
                category = item.find('category').text if item.find('category') is not None else ''
                
                # category가 'PCP'인 경우에만 데이터를 추가 (PCP : 1시간 강수량)
                if category == 'RN1':
                    # base_date = item.find('baseDate').text if item.find('baseDate') is not None else '' # baseDate : 발표일자
                    # base_time = item.find('baseTime').text if item.find('baseTime') is not None else '' # baseDate : 발표시각
                    fcst_date = item.find('fcstDate').text if item.find('fcstDate') is not None else '' # fcstDate : 예보일자
                    fcst_time = item.find('fcstTime').text if item.find('fcstTime') is not None else '' # fcstTime : 예보시각
                    fcst_value = item.find('fcstValue').text if item.find('fcstValue') is not None else '' # fcstValue : 예보 값
                    
                    all_data1.append({
                        # 'location': location_name,
                        # 'base_date': base_date,
                        #'base_time': base_time,
                        'fcst_date': fcst_date,
                        'fcst_time': fcst_time,
                        #'nx': nx,
                        #'ny': ny,
                        'fcst_value': fcst_value
                    })
        else:
            print(f"Error: {response.status_code}, location: {location_name}")

    # 데이터프레임으로 변환
    rainfall_data = pd.DataFrame(all_data1)
    # df['fcst_value'] = df['fcst_value'].apply(clean_fcst_value)
    # df[df['fcst_date'] == '20240711']
    all_df = pd.DataFrame(all_data)
    all_df['wl'] = all_df['wl'].astype(float)
    all_df['홍수주의보'] = all_df['홍수주의보'].astype(float)
    all_df['홍수경보'] = all_df['홍수경보'].astype(float)
    rainfall_data['date'] = rainfall_data['fcst_date']+ rainfall_data['fcst_time']
    # merged_data['year'] = merged_data['ymdh'].astype(str).str[:4]
    
    # df['time'] = df['fcst_time'].str[:2]
    
    df1 = rainfall_data[['fcst_value',   'date']]
    df1 = pd.DataFrame(df1)
    all = pd.DataFrame(all_data)
    merged_data = pd.merge(all,df1,left_on='ymdh',right_on='date',how='left')
    merged_data = merged_data[['ymdh', 'wl', 'obscd', '홍수주의보', '홍수경보', 'fcst_value']]
    # model_path = os.path.join(settings.DATA_DIR, 'model_wl.pkl')
    # model_info = joblib.load(model_path)
    # model_wl = model_info['model']
    # model_columns = model_info['columns']
    # data = data.rename(columns={'홍수주의보':'주의보초과', '홍수경보':'경보초과', 'fcst_value':'rf'})
    # pred = model_wl.predict(data)
    def predict_real_time(models, merged_data):
        merged_data['wl'] = pd.to_numeric(merged_data['wl'], errors='coerce')
        merged_data['홍수주의보'] = pd.to_numeric(merged_data['홍수주의보'], errors='coerce')
        merged_data['주의보초과'] = merged_data.apply(lambda row: 1 if row['wl'] > row['홍수주의보'] else 0, axis=1)
        merged_data['경보초과'] = merged_data.apply(lambda row: 1 if row['wl'] > row['홍수경보'] else 0, axis=1)
        
        predictions = {}

        for obscd in observatories.keys():
            data_for_prediction = merged_data[merged_data['obscd'] == obscd]

            if obscd in models:
                model = models[obscd]

                X_new = data_for_prediction[['fcst_value','wl' ,'주의보초과', '경보초과']]
                X_new = pd.DataFrame(X_new)
                X_new = X_new.rename(columns={'fcst_value':'강수량'})
                X_new = X_new.fillna(0)
                y_pred_proba_new = model.predict_proba(X_new)
                # y_pred_class_new = (y_pred_proba_new > 0.8).astype(int)

                data_for_prediction['홍수확률'] = y_pred_proba_new[:, 1]

                
                # 각 obscd와 예측 값을 사전에 추가합니다.
                predictions[obscd] = float(y_pred_proba_new[:, 1])

                # print(f"Predicted Flood Probability for obscd {obscd}: {y_pred_proba_new[0]}")
                # print(f"Predicted Class for obscd {obscd}: {y_pred_class_new[0]}")
                # print(data_for_prediction["wl"])
            else:
                print(f"No model found for obscd {obscd}")

        return predictions
    
    models = {}
    for obscd in observatories.keys():
        try:
            model_path = os.path.join(settings.DATA_DIR, f'./model_wl/model_{obscd}.pkl') 
            models[obscd] = joblib.load(model_path)
        except FileNotFoundError:
            print(f"No model file found for obscd {obscd}")

    # 실시간 데이터 예측
    predictions = predict_real_time(models, merged_data)
    
    all_data=[]
    i = 0
    for code, info in observatories.items():
        data = fetch_water_level_data(code)
        if data:
            
            latest_data = data[-1]  # 리스트에서 최신 데이터 선택
            latest_data['obsnm'] = info['name']  # 관측소 이름을 데이터에 추가
            latest_data['obscd'] = code
            latest_data['lat'] = info['lat']  # 관측소의 위도
            latest_data['lng'] = info['lng']  # 관측소의 경도
            latest_data['홍수주의보'] = info['홍수주의보'] 
            latest_data['홍수경보'] = info['홍수경보']
            latest_data['홍수확률']= round(predictions[code] * 100, 2)
            all_data.append(latest_data)
            i +=1
    return JsonResponse(all_data, safe=False)

def clean_fcst_value(value):
    if np.isnan(value):
        return 0.0
    # null, '-', '강수없음'인 경우 0.0으로 변환
    if value == '강수없음':
        return 0.0
    # '1 미만'인 경우 1.0으로 변환
    if value == '1mm 미만':
        return 1.0
    # '30.0~50.0mm' 범주인 경우 30.0으로 변환
    if value == '30.0~50.0mm':
        return 30.0
    # '50.0mm 이상' 범주인 경우 50.0으로 변환
    if value == '50.0mm 이상':
        return 50.0
    # 'mm'를 제거하고 숫자로 변환
    if 'mm' in value:
        return float(value.replace('mm', ''))