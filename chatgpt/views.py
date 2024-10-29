import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from textblob import TextBlob 

def analyze_sentiment(message):
    blob = TextBlob(message)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

@csrf_exempt
def chatgpt_view(request):
    """
    Handles requests to interact with the ChatGPT API for user messages.

    This view processes incoming POST requests containing a user's message,
    sends the message to the OpenAI ChatGPT API, and returns the generated
    response. If the request method is not POST, it renders the 'chatgpt.html'
    template for user interaction.
    """

    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        sentiment = analyze_sentiment(user_message)

        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )

        bot_message = completion.choices[0].message.content.strip()

        if sentiment == 'positive':
            bot_message += " 😊"
        elif sentiment == 'negative':
            bot_message += " 😔"
        else:
            bot_message += " 😐"

        return JsonResponse({
            'bot_message': bot_message
        })

    return render(request, 'chatgpt.html')
