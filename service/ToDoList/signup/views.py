from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup_view(request):
    if not request.session.get('agreed_to_terms'):
        return redirect('terms')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('role')

            user.email = email
            
            if role == 'admin' and not email.endswith('@aivle.co.kr'):
                form.add_error('email', '관리자는 @aivle.co.kr 이메일만 사용할 수 있습니다.')
                return render(request, 'signup/signup.html', {'form': form})
            else:
                user.save()
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'signup/signup.html', {'form': form})
    else:
        form = SignUpForm()
    
    return render(request, 'signup/signup.html', {'form': form})
