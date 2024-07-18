from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import FindUsernameForm

CustomUser = get_user_model()

def find_username(request):
    usernames = []
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email=email)
            if users.exists():
                usernames = [user.username for user in users]
            else:
                messages.error(request, 'No user is associated with this email address.')
    else:
        form = FindUsernameForm()

    return render(request, 'find_username/find_username.html', {'form': form, 'usernames': usernames})
