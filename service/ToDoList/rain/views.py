from django.shortcuts import render

def rain_view(request):
    return render(request, 'rain/rain.html')