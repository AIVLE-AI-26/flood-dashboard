import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
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


def get_geojson_data():
    # 엑셀 파일 경로
    excel_file_name = '광주광역시-침수피해현황_20231018.xlsx'
    excel_file_name2 = '광주광역시_대피소.xlsx'
    excel_file_path = os.path.join(settings.DATA_DIR, excel_file_name)
    excel_file_path2 = os.path.join(settings.DATA_DIR, excel_file_name2)
    
    # 엑셀 파일을 읽어 데이터프레임으로 변환
    df = pd.read_excel(excel_file_path)
    df2 = pd.read_excel(excel_file_path2)
    
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