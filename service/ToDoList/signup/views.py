from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .forms import SignUpForm
import re

def signup_view(request):
    if not request.session.get('agreed_to_terms'):
        return redirect('terms')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(f"Received POST data: {request.POST}")  # 디버깅 프린트 추가
        if form.is_valid():
            print("Form is valid.")  # 디버깅 프린트 추가
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('user_role')

            user.email = email
            
            if role == 'admin' and not email.endswith('@aivle.co.kr'):
                print("Admin email validation failed.")  # 디버깅 프린트 추가
                form.add_error('email', '관리자는 @aivle.co.kr 이메일만 사용할 수 있습니다.')
                return render(request, 'signup/signup.html', {'form': form})
            else:
                user.save()
                print(f"User {user.username} saved successfully.")  # 디버깅 프린트 추가

                # 사용자를 로그인시키기 전에 backend 설정
                backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user, backend=backend)

                return redirect('home')  # 회원가입 성공 시 메인 페이지로 이동
        else:
            birth_date_error = form.errors.get('birth_date')
            if birth_date_error:
                birth_date = request.POST.get('birth_date', '')
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date):
                    form.errors['birth_date'] = form.error_class(['생년월일은 yyyy-mm-dd 형식이어야 합니다.'])
            
            print("Form is not valid.")  # 디버깅 프린트 추가
            print(f"Form errors: {form.errors}")  # 디버깅 프린트 추가
            return render(request, 'signup/signup.html', {'form': form})
    else:
        form = SignUpForm()
        print("GET request - rendering form.")  # 디버깅 프린트 추가
    
    return render(request, 'signup/signup.html', {'form': form})
