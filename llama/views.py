import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .llama3_model import generate_response


@csrf_exempt
def llama_view(request):
    """
    Handles POST requests for interacting with a chatbot model.

    This view processes incoming POST requests containing a user's message,
    generates a response using the `generate_response` function, and returns
    the response in JSON format. If the request method is not POST, it renders
    the 'llama.html' template for user interaction.
    """
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
