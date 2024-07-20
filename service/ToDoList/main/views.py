import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
import joblib
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from signup.forms import SignUpForm, EditProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.shortcuts import render
from django.http import JsonResponse
import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta
from django.core.cache import cache
import time

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

def contact(request):
    return render(request, 'main/contact.html') 

def waterlevel(request):
    return render(request, 'waterlevel/waterlevel.html') 

def detect(request):
    return render(request, 'detect/home.html') 

def create_geojson(features):
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson

def create_polygon_feature(lat, lng, fill_color, fill_opacity=0.2, stroke_color=None, stroke_opacity=0, stroke_weight=2):
    if stroke_color is None:
        stroke_color = fill_color
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [lng - 0.001, lat - 0.001],
                [lng - 0.001, lat + 0.001],
                [lng + 0.001, lat + 0.001],
                [lng + 0.001, lat - 0.001],
                [lng - 0.001, lat - 0.001]
            ]]
        },
        "properties": {
            "fillColor": fill_color,
            "fillOpacity": fill_opacity,
            "strokeColor": stroke_color,
            "strokeOpacity": stroke_opacity,
            "strokeWeight": stroke_weight
        }
    }
    return feature

def create_point_feature(lat, lng, title, address, capacity, region, marker_color="#FF0000"):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lng, lat]
        },
        "properties": {
            "markerColor": marker_color,
            "markerSize": "medium",
            "markerSymbol": "circle",
            "title": title,
            "address": address,
            "capacity": capacity,
            "region": region
        }
    }
    return feature

def get_geojson_data():
    csv_file_name3 = 'df.csv'
    excel_file_name = '광주광역시-침수피해현황_20231018.xlsx'
    excel_file_name2 = '광주광역시_대피소.xlsx'
    
    csv_file_path3 = os.path.join(settings.DATA_DIR, csv_file_name3)
    excel_file_path = os.path.join(settings.DATA_DIR, excel_file_name)
    excel_file_path2 = os.path.join(settings.DATA_DIR, excel_file_name2)
    
    df3 = pd.read_excel(excel_file_path) 
    df2 = pd.read_excel(excel_file_path2) 
    df = pd.read_csv(csv_file_path3)

    lat_column = 'Latitude'
    lng_column = 'Longitude'
    shelter_name_column = '대피소 명칭'
    address_column = '주소'
    capacity_column = '최대 수용 인원'
    region_column = '구'
    
    features = []
    
    for index, row in df3.iterrows():
        lat = row[lat_column]
        lng = row[lng_column]
        if pd.notnull(lat) and pd.notnull(lng):
            features.append(create_polygon_feature(lat, lng, fill_color="#FF0000"))
    
    for index, row in df.iterrows():
        lat = row[lat_column]
        lng = row[lng_column]
        if pd.notnull(lat) and pd.notnull(lng):
            features.append(create_polygon_feature(lat, lng, fill_color="#0000FF"))

    for index, row in df2.iterrows():
        lat = row[lat_column]
        lng = row[lng_column]
        shelter_name = row[shelter_name_column]
        address = row[address_column]
        capacity = row[capacity_column]
        region = row[region_column]
        if pd.notnull(lat) and pd.notnull(lng):
            features.append(create_point_feature(lat, lng, shelter_name, address, capacity, region))
            
    return create_geojson(features)

def map_data_view(request):
    geojson_data = get_geojson_data()
    return JsonResponse(geojson_data)

def map_view(request):
    return render(request, 'main/base.html')

def handle_button(request):
    button_value = request.GET.get('button_value')
    if button_value is not None:
        model_path = os.path.join(settings.DATA_DIR, 'final_model.pkl')

        road_csv_path = os.path.join(settings.DATA_DIR, '쿠우쿵1.csv')
        
        model = joblib.load(model_path)
        
        road_csv = pd.read_csv(road_csv_path)
        road_csv['강수량'] = int(button_value)
        # road_csv1 = road_csv.drop(['시도시군구'], axis=1)
        road_csv1 = road_csv[['강수량','Latitude', 'Longitude' ,'elevation' , '펌프대수(대)',  '불투수면 비율(%)',  '불투수면 면적(㎢)',  '행정구역면적(㎢)']]
        # print(road_csv)
        pred = model.predict(road_csv1)
        y_score = (pred > 0.8).astype(int)
        df = road_csv[['Latitude', 'Longitude']][y_score.astype(bool)]
        print(df)
        features = []
        
        for _, row in df.iterrows():
            lat = row['Latitude']
            lng = row['Longitude']
            if pd.notnull(lat) and pd.notnull(lng):
                features.append(create_polygon_feature(lat, lng, fill_color="#0000FF"))
        
        return JsonResponse(create_geojson(features))
    
    return JsonResponse({'error': 'No value provided'}, status=400)

@login_required
def profile(request):
    return render(request, 'main/profile.html')

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # 비밀번호 변경 후 세션 유지
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'main/edit_profile.html', {'form': form})


service_key = 'nz2fwU3ROAjPxqq2gPGhnUPe6+ZWmxvhXIyUBW/qUrPl0T0za05as1fDc4AiuY/6R2jfQE0JQBr4MKDZ7MPC6w=='

async def fetch_weather_data(request):
    cached_data = cache.get('weather_data')
    if cached_data:
        return JsonResponse(cached_data, safe=False)
    
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    
    now = datetime.now() - timedelta(hours=5)
    base_date = now.strftime('%Y%m%d')
    base_time = now.strftime('%H00')

    common_params = {
        'serviceKey': service_key, 
        'pageNo': '1', 
        'numOfRows': '1000', 
        'dataType': 'XML', 
        'base_date': base_date, 
        'base_time': base_time,
        'nx': '58',  
        'ny': '74'
    }

    async def fetch_data():
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=common_params) as response:
                if response.status == 200:
                    print(f"API 요청 성공: 광주광역시")
                    root = ET.fromstring(await response.text())
                    data = []
                    
                    for item in root.findall('.//item'):
                        category = item.find('category').text if item.find('category') is not None else ''
                        
                        if category in ['RN1', 'T1H', 'SKY']: 
                            base_date = item.find('baseDate').text if item.find('baseDate') is not None else ''
                            fcst_date = item.find('fcstDate').text if item.find('fcstDate') is not None else ''
                            fcst_time = item.find('fcstTime').text if item.find('fcstTime') is not None else ''
                            fcst_value = item.find('fcstValue').text if item.find('fcstValue') is not None else ''
                            
                            data.append({
                                'category': category,
                                'base_date': base_date,
                                'fcst_date': fcst_date,
                                'fcst_time': fcst_time,
                                'fcst_value': fcst_value
                            })
                    return data
                else:
                    print(f"Error: {response.status}")
                    return []

    start_time = time.time()
    
    data = await fetch_data()

    end_time = time.time()
    print(f"비동기 방식 로딩 시간: {end_time - start_time}초")

    df = pd.DataFrame(data)

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
        return float(value)
    
    df['fcst_value'] = df['fcst_value'].apply(clean_fcst_value)
    
    today = datetime.now().strftime('%Y%m%d')
    current_time = datetime.now().strftime('%H00')
    
    filtered_data = df[(df['fcst_date'] == today) & (df['fcst_time'] == current_time)]
    current_data = filtered_data.to_dict(orient='records')
    
    cache.set('weather_data', current_data, timeout=600)
    
    return JsonResponse(current_data, safe=False)

def weather_view(request):
    return render(request, 'weather/weather.html')

def fetch_weather_data_view(request):
    return asyncio.run(fetch_weather_data(request))
