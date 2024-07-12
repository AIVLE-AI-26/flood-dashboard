from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
def signup_view(request):
    # 세션에 약관 동의 여부를 확인
    if not request.session.get('agreed_to_terms'):
        return redirect('terms')  # 약관 동의하지 않았다면 약관 동의 페이지로 리디렉션

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('role')
            
            # 이메일과 역할을 user 객체에 설정
            user.email = email
            
            if role == 'admin' and not email.endswith('@aivle.co.kr'):
                form.add_error('email', '관리자는 에이블 이메일로만 가입할 수 있습니다.') #'관리자는 @aivle.co.kr 이메일만 사용할 수 있습니다.
                return render(request, 'signup/signup.html', {'form': form})
            else:
                user.save()
                login(request, user)
                return redirect('home')  # 회원가입 후 메인 페이지로 리디렉션
    else:
        form = SignUpForm()
    
    return render(request, 'signup/signup.html', {'form': form})