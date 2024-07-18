from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.contrib import messages
from signup.models import CustomUser  # CustomUser 모델을 signup 앱에서 가져옴

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            print(f"Attempting to authenticate user: {username} with password: {raw_password}")
            
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                print(f"Authentication successful for user: {username}")
                login(request, user)
                print(f"User {username} logged in successfully.")
                return redirect('home')  # 로그인 후 메인 페이지로 리디렉션
            else:
                print(f"Authentication failed for user: {username}")
                messages.error(request, '아이디 혹은 비밀번호가 틀렸습니다.')
        else:
            print("Form is not valid")
            print(form.errors)  # 폼 에러 메시지 출력
    else:
        form = LoginForm()
        print("Rendering login form")
        
    return render(request, 'login/login.html', {'form': form, 'messages': messages.get_messages(request)})

def logout_view(request):
    print(f"User {request.user.username} is logging out.")
    logout(request)
    print("User logged out successfully.")
    return redirect('home')  # 로그아웃 후 메인 페이지로 리디렉션
