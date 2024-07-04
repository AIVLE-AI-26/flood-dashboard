# views.py

import os
import json
from django.shortcuts import render, redirect
from django.conf import settings

# 임시로 데이터를 저장할 리스트
posts = []

def board_write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        file = request.FILES.get('file')

        # 데이터 저장
        data = {
            'title': title,
            'content': content,
            'file_name': file.name if file else None,
        }

        # 파일 저장 경로 설정 및 디렉토리 생성
        board_dir = os.path.join(settings.BASE_DIR, 'board_data')
        os.makedirs(board_dir, exist_ok=True)  # 디렉토리 생성 (존재하지 않을 경우)

        # 파일 저장
        if file:
            file_path = os.path.join(board_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # 콘솔에 데이터 출력 (디버깅용)
        print(f"제목: {title}, 내용: {content}")

        # JSON 파일로 게시글 정보 저장 -> 임시로 기능 구현중...
        file_name = f'{len(os.listdir(board_dir)) + 1}.json' 
        file_path = os.path.join(board_dir, file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f)

        # 글쓰기 완료 후 리스트 페이지로 이동
        return redirect('board_list')

    return render(request, 'board/write.html')

def board_list(request):
    # 여기서는 실제로 저장된 데이터를 불러와서 context에 담아줘야 함
    board_dir = os.path.join(settings.BASE_DIR, 'board_data')
    posts = []

    # 디렉토리 안의 모든 JSON 파일을 읽어서 posts에 추가
    for filename in os.listdir(board_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(board_dir, filename)
            with open(file_path, 'r') as f:
                post_data = json.load(f)
                posts.append(post_data)

    context = {
        'posts': posts,
    }
    return render(request, 'board/list.html', context)
