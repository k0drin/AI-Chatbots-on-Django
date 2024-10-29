from django.http import JsonResponse
from .llama3_model import generate_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

@csrf_exempt 
def llama_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if user_message:
                bot_response = generate_response(user_message)
                return JsonResponse({"bot_message": bot_response})

            return JsonResponse({"error": "No message provided"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return render(request, "llama.html")
