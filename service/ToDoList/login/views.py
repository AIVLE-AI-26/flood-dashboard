from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')  # 로그인 후 메인 페이지로 리디렉션
        else:
            messages.error(request, '아이디 혹은 비밀번호가 틀렸습니다.')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form, 'messages': messages.get_messages(request)})


def logout_view(request):
    logout(request)
    return redirect('home')  # 로그아웃 후 메인 페이지로 리디렉션
