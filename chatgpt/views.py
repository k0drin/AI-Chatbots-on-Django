from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

import os
import openai
import json


@csrf_exempt
def chatgpt_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        client = OpenAI(
            api_key = os.getenv('OPENAI_API_KEY')
        )

        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )

        bot_message = completion.choices[0].message.content.strip()

        return JsonResponse({
            'bot_message': bot_message
        })

    return render(request, 'chatgpt.html')
