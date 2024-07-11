from django.shortcuts import render, redirect
from .forms import TermsForm

def terms_view(request):
    if request.method == 'POST':
        form = TermsForm(request.POST)
        if form.is_valid():
            # 약관 동의 상태를 세션에 저장
            request.session['agreed_to_terms'] = True
            # 회원가입 페이지로 이동
            return redirect('signup')
    else:
        form = TermsForm()
    return render(request, 'terms/terms.html', {'form': form})