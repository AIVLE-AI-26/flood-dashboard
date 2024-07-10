import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
import joblib
import os

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

# model_path = r'C:\Users\User\Documents\KT-BIGP\flood-dashboard\service\ToDoList\data\model1.joblib'
# model = joblib.load(model_path)

# def get_coordinates(request):
#     value = request.GET.get('value', None)
#     if value is not None:
#         value = float(value)  # 입력값을 실수로 변환
#         # 기존 데이터를 복사하여 새로운 데이터 생성
#         new_data = 광주.copy()
#         new_data["강수량"] = value  # 임의의 강수량 설정

    

#         # 예측 수행
#         y_pred_new = model.predict(new_data)

#         # 예측 결과를 데이터프레임에 추가
#         new_data['예측 침수여부'] = y_pred_new[:len(new_data)]  # 길이 맞추기

#         # 예측된 침수 여부가 높은 지역 필터링 (예: 0.8 이상인 지역)
#         flood_prone_areas = new_data[new_data['예측 침수여부'] >= 0.8]

#         # 필터링된 지역의 위도와 경도 값을 추출
#         locations = flood_prone_areas[['Latitude', 'Longitude']].dropna().to_dict(orient='records')
#         locations = [{'lat': loc['Latitude'], 'lng': loc['Longitude']} for loc in locations]

#         return JsonResponse({'locations': locations})
#     return JsonResponse({'error': 'No value provided'}, status=400)


def get_geojson_data():
    # 엑셀 파일 경로
    # excel_file_name = '광주광역시-침수피해현황_20231018.xlsx'
    
    csv_file_name3 = 'df.csv'
    excel_file_name2 = '광주광역시_대피소.xlsx'
    # excel_file_path = os.path.join(settings.DATA_DIR, excel_file_name)
    
    csv_file_path3 = os.path.join(settings.DATA_DIR, csv_file_name3)
    excel_file_path2 = os.path.join(settings.DATA_DIR, excel_file_name2)
    
    # 엑셀 파일을 읽어 데이터프레임으로 변환
    
    df2 = pd.read_excel(excel_file_path2) 
    df= pd.read_csv(csv_file_path3)


    
    # 위도와 경도가 포함된 열 이름을 정확히 확인하고 수정
    lat_column = 'Latitude'
    lng_column = 'Longitude'
    shelter_name_column = '대피소 명칭'  # 대피소 명칭 컬럼명
    address_column = '주소'  # 주소 컬럼명
    capacity_column = '최대 수용 인원'  # 최대 수용 인원 컬럼명
    region_column = '구'  # 구 컬럼명
    
    # GeoJSON 형식의 데이터 초기화
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # 각 행을 반복하여 GeoJSON 형식으로 변환 (df1)
    for index, row in df.iterrows():
        lat = row[lat_column]
        lng = row[lng_column]
        if pd.notnull(lat) and pd.notnull(lng):
            # 각 지점을 중심으로 하는 사각형 다각형 생성
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
                    "fillColor": "#0000FF",
                    "fillOpacity": 0.2,
                    "strokeColor": "#0000FF",
                    "strokeOpacity": 0,
                    "strokeWeight": 2
                }
            }
            geojson["features"].append(feature)
    
    # 각 행을 반복하여 GeoJSON 형식으로 변환 (df2)
    for index, row in df2.iterrows():
        lat = row[lat_column]
        lng = row[lng_column]
        shelter_name = row[shelter_name_column]
        address = row[address_column]
        capacity = row[capacity_column]
        region = row[region_column]
        if pd.notnull(lat) and pd.notnull(lng):
            # 마커 생성
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "properties": {
                    "markerColor": "#FF0000",
                    "markerSize": "medium",
                    "markerSymbol": "circle",
                    "title": shelter_name,  # 대피소 명칭 설정
                    "address": address,  # 주소 설정
                    "capacity": capacity,  # 최대 수용 인원 설정
                    "region": region  # 구 설정
                }
            }
            geojson["features"].append(feature)
    
    return geojson

def map_data_view(request):
    geojson_data = get_geojson_data()
    return JsonResponse(geojson_data)

def map_view(request):
    return render(request, 'main/base.html')

def handle_button(request):
    csv_file_name = 'df.csv'
    csv_file_name2 = '광주_도로명.csv'
    csv_file_path = os.path.join(settings.DATA_DIR, csv_file_name)
    csv_file_path2 = os.path.join(settings.DATA_DIR, csv_file_name2)
    road_csv = pd.read_csv(csv_file_path2)
    model_name = 'model.pkl'
    model_path = os.path.join(settings.DATA_DIR, model_name)
    model = joblib.load(model_path)
    if request.method == 'POST':
        button_value = request.POST.get('button_value')
        road_csv['강수량'] = int(button_value) 
        road_csv = road_csv.drop('침수피해여부',axis=1)
        pred = model.predict(road_csv)
        y_score = (pred > 0.9).astype(int)
        df = road_csv['Latitude'][y_score.astype(bool)],road_csv['Longitude'][y_score.astype(bool)]
        df = pd.DataFrame(df)
        df=df.T
        df.to_csv(csv_file_path,index=False)
        return render(request, 'main/base.html')

