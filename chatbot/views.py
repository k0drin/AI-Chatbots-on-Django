import json
import openai
import re
from django.shortcuts import render
from transformers import pipeline
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# OpenAI Start----------------------------------------------------------------------------------
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

    return render(request, 'chatbot/chatgpt.html')
# OpenAI Finish----------------------------------------------------------------------------------

sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english", 
    revision="714eb0f",
    device=0  # Set to CPU (-1) if GPU is not available
)

chat_memory = {
    'username': None,
    'interaction_count': 0,
}

greetings = ["hi", "hello", "hey"]
farewells = ["bye", "goodbye", "see you"]

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            chat_memory['interaction_count'] += 1

            bot_message = generate_response(user_message)

            # Reset memory after 3 interactions
            if chat_memory['interaction_count'] >= 3:
                bot_message += " How do you feel about our conversation so far?"
                chat_memory['interaction_count'] = 0

            return JsonResponse({'bot_message': bot_message})

        except Exception as e:
            return JsonResponse({'bot_message': "Sorry, there was an error processing your request."}, status=500)

    return render(request, 'chatbot/home.html')


def generate_response(user_message):
    user_message = user_message.lower()

    name_match = re.search(r"my name is ([a-zA-Z]+)", user_message) or re.search(r"i am ([a-zA-Z]+)", user_message)
    if name_match:
        chat_memory['username'] = name_match.group(1).capitalize()
        return f"Nice to meet you, {chat_memory['username']}! How can I help you today?"

    if "what is my name" in user_message:
        if chat_memory['username']:
            return f"Your name is {chat_memory['username']}!"
        else:
            return "I don't know your name yet. What's your name?"

    if any(greet in user_message for greet in greetings):
        return "Hello! How can I assist you today?"

    if any(farewell in user_message for farewell in farewells):
        return "Goodbye! Have a great day!"

    sentiment_result = sentiment_analyzer(user_message)[0]
    sentiment = sentiment_result['label']
    score = sentiment_result['score']
        
    print(f"Message : {user_message} Sentiment: {sentiment}, Confidence: {score:.2f}")

    if sentiment == 'POSITIVE':
        return "I'm glad to hear that! 😊"
    elif sentiment == 'NEGATIVE':
        return "I'm sorry you're having trouble. 😔 How can I assist further?"
    else:
        return "Okay! How can I help you today?"

    return "I'm not sure I understand. Can you rephrase?"
