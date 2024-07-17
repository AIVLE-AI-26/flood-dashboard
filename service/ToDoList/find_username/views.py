# find_username/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import FindUsernameForm

def find_username(request):
    usernames = []
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                usernames = [user.username for user in users]
            else:
                messages.error(request, 'No user is associated with this email address.')
    else:
        form = FindUsernameForm()

    return render(request, 'find_username/find_username.html', {'form': form, 'usernames': usernames})