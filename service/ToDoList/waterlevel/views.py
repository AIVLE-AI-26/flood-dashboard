from django.shortcuts import render

def waterlevel_view(request):
    return render(request, 'waterlevel/waterlevel.html')