# ai_chat_support/forms.py
from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type a message...', 'class': 'form-control'}))
