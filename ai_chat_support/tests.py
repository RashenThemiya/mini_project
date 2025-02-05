from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model  # Use get_user_model to avoid hardcoding
from ai_chat_support.models import Chat
from unittest.mock import patch

class ChatbotTestCase(TestCase):

    def setUp(self):
        # Use the get_user_model() method to create a user (it will point to your CustomUser model)
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com',  # Add email field here
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')  # Log in the user

    def test_ask_groq_error_handling(self):
        """Test the ask_groq function with an error."""
        with patch('ai_chat_support.views.client.chat.completions.create') as mock_create:
            mock_create.side_effect = Exception("Test error")
            response = self.client.post(reverse('ai_chat_support_index'), {'message': 'Hello'})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Error in generating response")  # Check for error message

    def test_chatbot_view_get(self):
        """Test the chatbot view with a GET request."""
        response = self.client.get(reverse('ai_chat_support_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatbot.html')  # Ensure the correct template is used

    def test_chatbot_view_post(self):
        """Test the chatbot view with a POST request and check AI response."""
        response = self.client.post(reverse('ai_chat_support_index'), {'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'message')
        self.assertContains(response, 'response')

    def test_chat_model(self):
        """Test saving chat messages and responses in the database."""
        chat = Chat.objects.create(user=self.user, message="Hello", response="Hi there!")
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(chat.user.username, "testuser")
        self.assertEqual(chat.message, "Hello")
        self.assertEqual(chat.response, "Hi there!")

