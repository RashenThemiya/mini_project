from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from .models import Chat
from django.utils import timezone
from groq import Groq
import os

# Load the Groq API key from environment variables
groq_api_key = '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'

# Instantiate the Groq client with the API key
client = Groq(api_key=groq_api_key)

def ask_groq(message):
 try:
    # Create a completion using the Groq API9+ooy   
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the streamed response
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    print("AI Response: ", response_text)
    return response_text
 

 except Exception as e:
        print(f"Error in ask_groq: {e}")
        return "Error in generating response"

def chatbot(request):
    
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_groq(message)

        

        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html')
