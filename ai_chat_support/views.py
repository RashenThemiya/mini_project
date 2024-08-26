# ai_chat_support/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ChatForm
from .models import ChatMessage
import openai
from django.conf import settings

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def chat_view(request):
    form = ChatForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user_message = form.cleaned_data['message']
        
        try:
            # Use OpenAI API to get a response
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini  ",
                messages=[{"role": "user", "content": user_message}]
            )
            bot_response = response['choices'][0]['message']['content']

            # Save messages to the database
            ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)
            
            # Log the response to debug
            print(f"Bot Response: {bot_response}")

            # Ensure the response is returned as JSON
            return JsonResponse({'response': bot_response})
        
        except openai.error.OpenAIError as e:
            # Print the error message to the console
            print(f"OpenAI API Error: {str(e)}")
            return JsonResponse({'response': 'An error occurred while fetching the response.'}, status=500)
        
        except Exception as e:
            # Print any other errors to the console
            print(f"Error: {str(e)}")
            return JsonResponse({'response': 'An unexpected error occurred.'}, status=500)
    
    return render(request, 'chat.html', {'form': form})
