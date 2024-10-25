from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import openai
import json


@csrf_exempt
def chatgpt_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )

        bot_message = response['choices'][0]['message']['content']

        return JsonResponse({
            'bot_message': bot_message
        })

    return render(request, 'chatgpt.html')
