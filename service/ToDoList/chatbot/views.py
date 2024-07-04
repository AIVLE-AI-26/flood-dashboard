from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .baseline import response  # Import the response function from baseline.py

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        system_prompt = "당신은 도움이 되는 비서입니다."  # 한글 시스템 프롬프트 추가
        response_text, _ = response(prompt, [], system_prompt)
        return JsonResponse({'response': response_text})
    return render(request, 'chatbot/chatbot.html')