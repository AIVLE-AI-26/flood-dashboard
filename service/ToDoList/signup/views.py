from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup_view(request):
    # 세션에 약관 동의 여부를 확인
    if not request.session.get('agreed_to_terms'):
        return redirect('terms')  # 약관 동의하지 않았다면 약관 동의 페이지로 리디렉션

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # 회원가입 후 메인 페이지로 리디렉션
    else:
        form = UserCreationForm()
    return render(request, 'signup/signup.html', {'form': form})